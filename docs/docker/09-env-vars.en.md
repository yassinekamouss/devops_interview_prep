# Part IX — Environment Variables

## Chapter 25

### ENV

Defined in the Dockerfile or via `docker run -e`, persists in the image (`ENV`) or only at runtime (`-e`).

```dockerfile
ENV NODE_ENV=production
```

```bash
docker run -e NODE_ENV=production mon-app
docker run --env-file .env mon-app
```

### ARG

Available **only during the build**, absent from the running container unless re-injected via `ENV` (see Part VI, Chapter 17).

```dockerfile
ARG BUILD_VERSION
ENV APP_VERSION=$BUILD_VERSION
```

### Secrets

!!! danger "Interview Trap"
    `ENV` and `ARG` are visible in plain text via `docker inspect` and `docker history` — **never** put a password, API key or token in these two mechanisms. Use instead:
    
    - Docker Compose: `secrets:` (mounted as a file, not a variable).
    - BuildKit: `RUN --mount=type=secret,id=mysecret` (secret available only during the `RUN` execution, never persisted in a layer).
    - In orchestration: Kubernetes Secrets, Vault, or cloud secret managers (AWS Secrets Manager, Oracle Vault).

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    curl -H "Authorization: Bearer $API_KEY" https://exemple.com
```

```bash
docker build --secret id=api_key,src=./api_key.txt .
```

### .env

File of variables automatically consumed by `docker compose` (not by `docker run`, which requires explicit `--env-file`).

```
# .env
DB_USER=admin
DB_PASSWORD=changeme
```

```yaml
services:
  db:
    environment:
      - POSTGRES_USER=${DB_USER}
```

!!! danger "Interview Trap"
    A `.env` file at the root of a Compose project is loaded **implicitly** by `docker compose` — but `docker run` never reads it without explicit `--env-file .env`. Frequent confusion between the two behaviors.

### Injection

Priority order (most priority last) for Compose: default Dockerfile values (`ENV`) < `.env` file < `environment:` in compose.yaml < shell variable exported at `docker compose up` time < `-e` on the command line for standalone `docker run`.

??? question "Interview Question: Why should you never store a secret in a Dockerfile ENV variable?"
    Because it is baked into an image layer, visible to anyone with access to the image (`docker history`, `docker inspect`), even after apparent removal of the file in a later layer (previous layers remain accessible). A secret must be injected **at runtime**, never at build time, except via the `--mount=type=secret` mechanism which does not persist in the final image.
