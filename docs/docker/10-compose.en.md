# Part X — Docker Compose

## Chapter 26: Introduction

### Why Compose

`docker run` quickly becomes unmanageable as soon as an application comprises several linked containers (app + database + cache). Compose declares the entire stack in **a single YAML file**, versionable and reproducible.

### Use Cases

- Multi-service development environments (app + DB + Redis).
- Integration tests in CI (disposable full stack).
- Simple single-host deployments (small applications, no need for Kubernetes).

### Compose Specification

Since 2020, Compose follows the **Compose Specification**, an open standard (no longer tied to a single vendor) — hence the disappearance of the `version:` key in recent files (`docker compose` ignores the version and always applies the latest supported spec).

---

## Chapter 27: The compose.yaml File

```yaml
services:
  app:
    build: .
    ports:
      - "8080:80"
    environment:
      - DB_HOST=db
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - backend

  db:
    image: postgres:16
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

volumes:
  db-data:

networks:
  backend:
```

### services

Each key under `services:` defines a container (service name = internal DNS network name, like a custom `--network` under `docker run`).

### volumes

Declared at the root level (`volumes:`), referenced by name in services — equivalent to `docker volume create` + `-v name:/path`.

### networks

By default, Compose creates **a dedicated bridge network** for the project (all services connect to it automatically) — internal DNS available natively, without manual configuration.

### depends_on

```yaml
depends_on:
  db:
    condition: service_healthy
```

!!! danger "Classic Interview Trap"
    `depends_on` without `condition` only guarantees the **startup order** of containers, not that the dependent service is actually ready to receive requests (e.g. Postgres started but not yet accepting connections). Always combine with `condition: service_healthy` and a `healthcheck` defined on the service you depend on, for a real availability guarantee.

### restart

Same values as `docker run --restart` (Part V, Chapter 15): `no`, `always`, `on-failure`, `unless-stopped`.

### healthcheck

Same semantics as in Dockerfile (Part V, Chapter 15), defined here at the service level.

### build

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
      args:
        - VERSION=1.0
```

### image

```yaml
services:
  db:
    image: postgres:16
```

If both `build:` and `image:` are present, Compose builds the image and tags it with the name indicated in `image:`.

### environment

```yaml
environment:
  - DB_HOST=db
  - DB_PASSWORD=${DB_PASSWORD}   # substitution depuis .env ou variable shell
```

---

## Chapter 28: Compose Commands

| Command | Role |
|---|---|
| `docker compose up` | Creates and starts all services (`-d` for background) |
| `docker compose down` | Stops and removes containers + networks (keeps volumes except `-v`) |
| `docker compose stop` | Stops containers without removing them |
| `docker compose start` | Restarts stopped containers |
| `docker compose restart` | Restarts services |
| `docker compose logs` | Aggregated logs of all services (`-f` to follow live) |
| `docker compose exec` | Executes a command in a running service |
| `docker compose build` | (Re)builds images defined with `build:` |
| `docker compose pull` | Pulls images defined with `image:` |
| `docker compose ps` | Lists containers of the current Compose project |

```bash
docker compose up -d
docker compose logs -f app
docker compose exec app bash
docker compose down -v      # supprime aussi les volumes nommés
```

!!! danger "Interview Trap"
    `docker compose down` **does not remove** named volumes by default — intentional behavior to avoid accidental data loss. You must explicitly pass `-v` to remove them. Many candidates incorrectly think `down` does a full cleanup by default.

??? question "Interview Question: Is Compose suitable for a multi-host cluster in production?"
    No — Compose (in its `docker compose up` usage) targets **single-host** deployment. For multi-host, you need Docker Swarm (`docker stack deploy`, which partly reuses Compose syntax) or, in almost systematic practice today, Kubernetes (see Part XVI). Docker Compose nevertheless remains an excellent tool for local development and CI, even in a Kubernetes production environment.

??? question "Interview Question: How to force rebuilding an image without cache in Compose?"
    `docker compose build --no-cache`, followed by `docker compose up -d --force-recreate` if you also want to force replacement of existing containers (even if the configuration has not changed from Compose's point of view).
