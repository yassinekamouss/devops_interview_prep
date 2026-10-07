# Part XIII — Debugging

## Chapter 31

### Logs

```bash
docker logs mon-app
docker logs -f mon-app              # suivi en temps réel
docker logs --since 10m mon-app     # dernières 10 minutes
docker logs --tail 100 mon-app      # 100 dernières lignes
```

Docker captures only **stdout/stderr** of the PID 1 process. An application that writes its logs to a file inside the container (`/var/log/app.log`) will **not** appear in `docker logs` — reconfigure the app to log to stdout, or mount a volume and tail the file separately.

### docker inspect

```bash
docker inspect mon-app
docker inspect --format='{{.State.Status}}' mon-app
docker inspect --format='{{json .NetworkSettings.Networks}}' mon-app | jq
```

First command to run when facing unexpected behavior: state, exit code, mounts, network config, effective environment variables — everything is there.

### docker events

```bash
docker events
docker events --filter 'container=mon-app'
docker events --filter 'event=die'
```

Real-time stream of daemon events (creation, start, stop, OOM kill...) — useful to correlate a crash with an external action (deployment, `docker prune`, etc.) at the exact moment it occurs.

### docker stats

```bash
docker stats
docker stats --no-stream mon-app     # une seule mesure, sans rafraîchissement continu
```

Real-time view of CPU/RAM/network/I/O — first reflex to diagnose abnormal consumption or confirm an imminent `OOMKilled`.

### docker top

```bash
docker top mon-app
```

Lists the container's internal processes, seen from the host (real host PIDs) — useful to spot a zombie process or excessive forking.

### docker diff

See Part V, Chapter 14 — lists files modified since startup, useful to audit unexpected writes outside expected volumes.

### docker system df

```bash
docker system df
docker system df -v      # détail par image/conteneur/volume
```

Shows disk space used by images, containers, volumes and build cache — first reflex when the host disk is full.

### docker system prune

```bash
docker system prune                 # conteneurs arrêtés + réseaux inutilisés + images dangling + cache de build
docker system prune -a              # + toutes les images non utilisées par un conteneur actif
docker system prune -a --volumes    # + tous les volumes non utilisés (destructif, à utiliser avec prudence)
```

!!! danger "Interview Trap"
    `docker system prune -a --volumes` is **irreversible** and removes all data not explicitly attached to a currently running container. Never run it on a production host without first checking the affected volumes (`docker volume ls` + `docker inspect` of each active service).

### Typical Debugging Methodology

| Symptom | First command |
|---|---|
| Container does not start | `docker logs`, then `docker inspect --format='{{.State.Error}}'` |
| Container restarts in a loop | `docker inspect --format='{{.State.ExitCode}}'`, `docker logs --tail 50` |
| Container slow / consumes too much | `docker stats`, `docker top` |
| Container killed unexpectedly | `docker inspect --format='{{.State.OOMKilled}}'`, `docker events --filter event=oom` |
| Cannot reach another service | `docker network inspect`, internal DNS test (`docker exec ... nslookup`) |
| Host disk full | `docker system df -v` |

??? question "Interview Question: A container restarts in a loop (`CrashLoop`). Diagnostic approach?"
    1) `docker logs mon-app --tail 50` to see the application error before the crash. 2) `docker inspect --format='{{.State.ExitCode}}' mon-app` — code 137 suggests SIGKILL (often OOM), code 1 a handled application error. 3) Check `OOMKilled` in `docker inspect`. 4) Check the current `restart policy` (`on-failure` may hide a real problem by restarting indefinitely). 5) If the app depends on another service (DB), verify that `healthcheck`/`depends_on` is correctly configured (see Part X).

??? question "Interview Question: Why can `docker logs` be empty even though the application visibly writes logs?"
    Because the application writes to a file inside the container rather than to stdout/stderr. Docker only captures those two streams from the PID 1 process. Solution: reconfigure the application logger to stdout (best practice "12-factor app"), or mount the log file via a volume and inspect it directly.
