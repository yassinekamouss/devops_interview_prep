# Part VIII — Volumes

## Chapter 22: Persistence

### Why Data Disappears

The writable layer of a container (Copy-on-Write, see Part II, Chapter 7) is tied to the **container lifecycle**. It is destroyed with `docker rm`. Any data written only in this layer is therefore lost when the container is removed.

### Lifecycle

| Storage | Survives `docker stop`/`start` | Survives `docker rm` |
|---|---|---|
| Container writable layer | ✅ | ❌ |
| Named volume | ✅ | ✅ |
| Bind mount | ✅ | ✅ |
| tmpfs | ✅ (as long as the container runs) | ❌ (never written to disk) |

---

## Chapter 23: Storage Types

### Volumes

Fully managed by Docker, stored in `/var/lib/docker/volumes/`. This is the **recommended** mechanism for persistence in production.

```bash
docker volume create mes-donnees
docker run -d -v mes-donnees:/var/lib/postgresql/data postgres
```

Advantages: managed via Docker CLI/API, portable across hosts (via `docker volume` network drivers — NFS, cloud), easier backup, no dependency on a specific host path.

### Bind Mount

Mounts an **existing host path** directly into the container.

```bash
docker run -d -v /home/user/app:/app mon-app
docker run -d --mount type=bind,source=/home/user/app,target=/app mon-app   # syntaxe explicite recommandée
```

Useful in development (hot reloading of source code), but couples the container to the host's file structure — less portable.

### tmpfs

Stores data **in RAM only**, never on disk.

```bash
docker run -d --tmpfs /app/cache:size=100m mon-app
```

Useful for sensitive temporary data (decrypted secrets, caches) that must never persist on disk.

!!! danger "Interview Trap"
    `-v` and `--mount` do not behave identically in one edge case: with `-v`, if the source path (bind mount) does not exist on the host, Docker **automatically creates it** (often by mistake, creating an empty folder instead of failing). With `--mount`, Docker **fails explicitly** if the source does not exist. `--mount` is the recommended syntax in production for this reason, in addition to being more readable.

---

## Chapter 24: Management

### docker volume

```bash
docker volume create mes-donnees
docker volume ls
docker volume inspect mes-donnees
docker volume rm mes-donnees
docker volume prune          # supprime tous les volumes non utilisés par un conteneur
```

### Backup

```bash
docker run --rm \
  -v mes-donnees:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .
```

Principle: run a temporary container (`--rm`) mounting the volume to back up and a host output directory, then archive.

### Restore

```bash
docker run --rm \
  -v mes-donnees:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

### Migration

To migrate a volume to another host: `backup` → transfer the `.tar.gz` (scp, S3...) → `restore` on the new host. For network volumes (NFS, cloud), use directly a compatible volume driver (`local-persist`, `rexray`, CSI in Kubernetes) pointing to the same shared storage backend.

??? question "Interview Question: Volume or bind mount for a database in production?"
    Named volume, without hesitation. It is managed by Docker (consistent permissions, better portability, no dependency on a specific host path), generally more performant under Docker Desktop (Mac/Windows), and suited to standard backup tools (`docker volume`). Bind mount remains preferable only for local development (live code editing).

??? question "Interview Question: What is the practical difference between an anonymous and a named volume?"
    An anonymous volume (`-v /data`, without source name) receives a randomly generated identifier and is automatically removed by `docker rm -v` — it is difficult to reuse across containers. A named volume (`-v mes-donnees:/data`) is explicit, reusable by multiple containers, and **never** automatically removed, even with `docker rm -v`.
