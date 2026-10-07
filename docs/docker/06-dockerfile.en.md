# Part VI — Dockerfile

## Chapter 16: Dockerfile

### Syntax

A Dockerfile is a sequence of instructions, each on one line, executed **sequentially** by the builder to produce an image, layer by layer.

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Structure

Each instruction that modifies the filesystem (`RUN`, `COPY`, `ADD`) creates a **new layer**. Metadata instructions (`ENV`, `LABEL`, `EXPOSE`, `CMD`, `ENTRYPOINT`) do not create a filesystem layer but update the image configuration.

### Build Context

```bash
docker build -t mon-app:1.0 .
```

The final `.` is the **build context**: the set of files sent to the Docker daemon to build the image. Everything in this directory is transferred (except what is excluded via `.dockerignore`), even files not used by the Dockerfile.

```
# .dockerignore
.git
node_modules
*.log
.env
```

!!! danger "Interview Trap"
    A build context that is too large (e.g. forgetting to exclude `.git` or `node_modules`) greatly slows down the build and may leak secrets into image layers if a sensitive file is copied by mistake (`COPY . .`). Always maintain a strict `.dockerignore`.

### Cache

Docker caches each layer. If the instruction and its context (copied files, checksum) have not changed since the last build, the layer is **reused** without re-execution.

```dockerfile
# Mauvais ordre : invalide le cache pip à chaque changement de code
COPY . .
RUN pip install -r requirements.txt

# Bon ordre : le cache pip survit tant que requirements.txt ne change pas
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

!!! danger "Classic Interview Trap"
    The order of instructions in a Dockerfile has a direct impact on build speed. General rule: place first what changes **least often** (dependencies) and last what changes **most often** (application source code), to maximize cache reuse.

---

## Chapter 17: All Dockerfile Instructions

| Instruction | Role |
|---|---|
| `FROM` | Base image |
| `RUN` | Executes a command at build time (new layer) |
| `CMD` | Default command executed at startup (overridable) |
| `ENTRYPOINT` | Fixed entry point (not overridable without `--entrypoint`) |
| `COPY` | Copies files from the build context into the image |
| `ADD` | Like `COPY`, with archive extraction and URL support |
| `WORKDIR` | Sets the current working directory |
| `ENV` | Defines an environment variable (persists in the container) |
| `ARG` | Variable available only at build time |
| `LABEL` | Adds metadata (key/value) to the image |
| `EXPOSE` | Documents the port used (does not actually open anything) |
| `USER` | Defines the user for subsequent instructions and the container |
| `SHELL` | Changes the shell used for shell-form `RUN` instructions |
| `HEALTHCHECK` | Defines a health check command |
| `STOPSIGNAL` | Changes the signal sent by `docker stop` (default SIGTERM) |
| `ONBUILD` | Triggers an instruction in **child** images that inherit from this one |
| `VOLUME` | Declares a mount point as an anonymous volume |

### CMD vs ENTRYPOINT

```dockerfile
# CMD seul : entièrement surchargeable
CMD ["nginx", "-g", "daemon off;"]
# docker run mon-image echo hello   -> exécute "echo hello", ignore CMD

# ENTRYPOINT seul : les arguments de "docker run" s'ajoutent à la suite
ENTRYPOINT ["python", "app.py"]
# docker run mon-image --debug   -> exécute "python app.py --debug"

# Combinaison ENTRYPOINT + CMD : CMD fournit les arguments par défaut de ENTRYPOINT
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]
# docker run mon-image             -> python app.py --port 8080
# docker run mon-image --port 9090 -> python app.py --port 9090
```

!!! danger "Major Interview Trap"
    This is one of the most asked questions. Remember: `ENTRYPOINT` defines **the program executed**, `CMD` defines **the default arguments** for that program (or the full command if there is no `ENTRYPOINT`). `docker run image <args>` replaces `CMD` but appends to `ENTRYPOINT`.

### COPY vs ADD

!!! danger "Interview Trap"
    `ADD` can automatically extract local archives (`.tar.gz`) and download remote URLs — a "magic" behavior that leads to non-reproducible builds and security risks (unverified URL). The almost unanimous best practice: **always prefer `COPY`**, and only use `ADD` for the specific case of local archive extraction.

### ARG vs ENV

```dockerfile
ARG VERSION=1.0        # disponible uniquement pendant le build
ENV APP_VERSION=$VERSION   # persiste dans l'image et le conteneur en cours d'exécution
```

```bash
docker build --build-arg VERSION=2.0 -t mon-app .
```

!!! danger "Interview Trap: secrets in ARG"
    Never pass a secret via `ARG` (e.g. `ARG API_KEY`): its value remains visible in the image history (`docker history`) and in the build cache, even if it does not appear in the final `ENV`. Instead use `RUN --mount=type=secret` (BuildKit) or inject the secret only at runtime via `ENV`/volume, never at build time.

### USER

```dockerfile
RUN groupadd -r app && useradd -r -g app app
USER app
```

Running the container as non-root greatly reduces the impact of a potential compromise (see Part XII, Security).

### VOLUME

```dockerfile
VOLUME /data
```

Declares that `/data` should be a mount point external to the container's writable layer — Docker automatically creates an anonymous volume there if no explicit volume/bind mount is provided at `run`.

### ONBUILD

```dockerfile
# Dans une image de base "builder-python"
ONBUILD COPY . /app
ONBUILD RUN pip install -r /app/requirements.txt
```

Useful for creating generic base images ("templates") that other teams extend via `FROM builder-python`, without duplicating build logic.

---

## Chapter 18: Optimization

### Multi-stage Build

```dockerfile
# Étape 1 : build (contient compilateurs, outils lourds)
FROM golang:1.22 AS builder
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app

# Étape 2 : image finale (minimale)
FROM scratch
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
```

Only the necessary artifacts (`--from=builder /app`) are copied into the final image: build tools (compilers, dev dependencies) never end up there. Result: an image potentially going from several hundred MB to a few MB.

### Size Reduction

#### Alpine

Minimalist base image (~5 MB) based on `musl libc` rather than `glibc`. Beware: some libraries compiled for `glibc` may not work directly under Alpine (binary incompatibility) — a classic pitfall with some native Python/Node packages.

#### Distroless

Google images (`gcr.io/distroless/*`) that contain **only the necessary runtime** (e.g. just libc + the binary), without shell, package manager, or system tools.

!!! danger "Interview Trap: distroless and debugging"
    A distroless image has **no shell** (`/bin/sh` missing): `docker exec -it mon-app sh` fails. This is an intentional trade-off for security (minimal attack surface, nothing to exploit after compromise) — debugging must then go through external tools (debug sidecar, `kubectl debug` in Kubernetes) or logs/traces only.

### Cache

See Chapter 16 — order instructions from least volatile to most volatile to maximize build cache reuse.

### Best Practices

- Always pin a precise version of the base image (`FROM python:3.12.3-slim`, not `FROM python`).
- Merge logically related `RUN` instructions to limit the number of layers (`RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*`).
- Never run as `root` without reason (`USER app`).
- Use an exhaustive `.dockerignore`.
- Use `HEALTHCHECK` to allow the orchestrator to detect failing instances.
- Scan the image (Trivy, Docker Scout, Grype) before publishing (see Part XII).

??? question "Interview Question: Why can't a `scratch` image run a dynamically linked binary?"
    `scratch` is a **completely empty** image (0 bytes): no libc, no `/bin/sh`, nothing. A dynamically linked binary needs libc at runtime to resolve its symbols — absent in `scratch`, it cannot start. You must either compile statically (`CGO_ENABLED=0` in Go, for example), or use a minimal base containing libc (`distroless/base`, `alpine`).

??? question "Interview Question: Does a multi-stage build improve build speed, or only the final image size?"
    Primarily the **final size** and **security** (fewer tools = smaller attack surface). For speed, the effect depends on caching: intermediate stages are themselves cached independently, so if only the source code changes, the `builder` stage may be partially invalidated but the final stage remains fast to rebuild.
