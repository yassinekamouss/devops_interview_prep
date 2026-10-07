# Part XVII — Oracle Interview Questions

!!! info "How to use this bank"
    🟢 Basic · 🟡 Intermediate · 🔴 Advanced/tricky. Answer out loud before reading the answer — it's the best preparation for an oral interview.

## Tricky Questions

1. 🟢 **Docker and a VM, what is the fundamental difference?**
   A VM virtualizes hardware and embeds a complete kernel per instance; a container shares the host kernel and only isolates processes via namespaces/cgroups (Part I, Ch.2-3).

2. 🟡 **`docker stop` vs `docker kill`?**
   `stop` sends SIGTERM then waits for a grace period before SIGKILL; `kill` sends SIGKILL directly (or a custom signal), without delay (Part V, Ch.13).

3. 🔴 **`CMD` vs `ENTRYPOINT` — give an example where combining both changes behavior.**
   `ENTRYPOINT ["python","app.py"]` + `CMD ["--port","8080"]`: `docker run image` runs `python app.py --port 8080`; `docker run image --port 9090` runs `python app.py --port 9090` (CMD is replaced, not ENTRYPOINT) (Part VI, Ch.17).

4. 🔴 **Why is `latest` dangerous in production?**
   It is not guaranteed to be the most recent version semantically, the pointed digest can change between two pulls, and it breaks deployment reproducibility (Part IV, Ch.11).

5. 🟡 **`docker save` vs `docker export`?**
   `save` operates on an image and preserves layers/history; `export` operates on a container and flattens its filesystem into a single layer (Part IV, Ch.12).

6. 🔴 **Can container A reach a service in container B via `localhost`?**
   No, unless they are in the same Kubernetes pod (shared network namespace). In standalone Docker, each container has its own `localhost` — you must go through the container name on a custom Docker network (Part VII, Ch.21).

7. 🟡 **Does `EXPOSE` in a Dockerfile open a port?**
   No, it is purely documentary. Only `-p`/`-P` at `docker run` actually publishes a port (Part VII, Ch.21).

8. 🟢 **What happens to a removed container's writable layer?**
   It is destroyed with the container — any data not persisted via volume/bind mount is lost (Part VIII, Ch.22).

9. 🟡 **Does `docker compose down` remove volumes?**
   No, by default. You need `docker compose down -v` explicitly (Part X, Ch.28).

10. 🔴 **What does `--privileged` do and why is it risky?**
     It disables almost all security restrictions (capabilities, device access, seccomp/AppArmor) — almost equivalent to full root access to the host (Part XII, Ch.30).

11. 🟡 **Does the `docker` group give implicit root access?**
     Yes — a user in the `docker` group can mount the host's `/` inside a container and gain full access (Part III, Ch.9).

12. 🔴 **Why avoid `ARG` for a build secret?**
     Its value remains visible in `docker history` and the build cache, even if removed in a later layer (Part IX, Ch.25).

## Design Questions

13. 🟡 **How to structure a Dockerfile to maximize build cache?**
     Put first what changes least often (dependencies), copy source code last (Part VI, Ch.16).

14. 🔴 **Design a multi-stage Dockerfile for a statically compiled Go app.**
     `builder` stage with full `golang` to compile (`CGO_ENABLED=0 go build`), final stage `FROM scratch` copying only the binary — final image of a few MB (Part VI, Ch.18).

15. 🟡 **How to organize Docker networks for an app + DB + cache stack?**
     `frontend` network (exposed app) and isolated `backend` network (DB, cache); the app is connected to both, the DB/cache only to `backend` (Part VII, Ch.20).

16. 🔴 **Design the healthcheck strategy for a Compose stack with strict app → DB dependency.**
     `healthcheck` on the DB service (`pg_isready`), `depends_on: db: condition: service_healthy` on the app — the app only starts when the DB actually responds (Part X, Ch.27).

17. 🟡 **How to handle different dev/staging/prod configurations with Compose?**
     Base file `compose.yaml` + override files (`compose.override.yaml`, `compose.prod.yaml`) merged via `-f`, or distinct `.env` files per environment.

18. 🔴 **Design the image pipeline to guarantee zero secrets in the final image.**
     `RUN --mount=type=secret` (BuildKit) for any secret access during build, never `ARG`/`ENV`; scan (Trivy/Docker Scout) before push; inject runtime secrets via an external manager, never in the image (Part IX, Ch.25 + Part XII, Ch.30).

19. 🟡 **How to limit the attack surface of a production image?**
     Minimal base (distroless/alpine), non-root `USER`, `--cap-drop=ALL` + minimal capabilities, systematic scanning, no shell if possible (Part XII, Ch.30).

20. 🔴 **Design a logging strategy for 50 containers on 5 hosts.**
     Centralized log driver (`gelf`/`fluentd`) or collection sidecar (Fluent Bit) on each host, aggregation to a common backend (ELK/Loki), rotation configured on the local driver as fallback (Part XIV, Ch.32).

## Production Questions

21. 🟢 **A container shows `OOMKilled: true`. What do you do?**
     Check `docker stats`/historical metrics to distinguish a real memory leak vs `--memory` limit too low for a legitimate spike, before adjusting (Part V, Ch.15).

22. 🟡 **How to deploy without service interruption (zero-downtime)?**
     Reliable healthcheck + rolling update or blue-green driven by an orchestrator/reverse proxy that only routes to `healthy` instances (Part XIV, Ch.32).

23. 🔴 **The production host disk is 100% full due to Docker. Approach?**
     `docker system df -v` to identify the source (images, containers, volumes, build cache), then targeted `docker system prune` — never `-a --volumes` without first checking active volumes (Part XIII, Ch.31).

24. 🟡 **Why systematically configure `log-opts` (`max-size`, `max-file`)?**
     Without limit, the default `json-file` driver can fill the host disk with application logs alone (Part XIV, Ch.32).

25. 🔴 **How to audit security compliance of a production Docker host?**
     Run `docker/docker-bench-security` (CIS Docker Benchmark), scan images (Trivy), verify rootless/capabilities/SELinux-AppArmor active (Part XII, Ch.30).

26. 🟡 **How to back up data from a Docker volume in production?**
     Temporary container mounting the volume + a host directory, archiving with `tar` (Part VIII, Ch.24).

27. 🔴 **A rollback is needed after a failed deployment. Prerequisites for it to be safe?**
     Previous image available in the registry (appropriate retention policy), DB compatibility between both application versions (beware of destructive migrations) (Part XIV, Ch.32).

## Architecture Questions

28. 🟡 **Why Kubernetes rather than Docker Compose for a high-traffic application?**
     Compose is single-host; Kubernetes provides multi-node scaling, automatic rescheduling on failure, and metric-based autoscaling (Part XVI, Ch.34).

29. 🔴 **Pod vs container: what is the Kubernetes deployment unit and why does this distinction exist?**
     The pod, not the container — it enables the sidecar pattern (containers sharing network/volumes, e.g. proxy or log agent next to the main app) (Part XVI, Ch.34).

30. 🟡 **Does Docker still have a role in a 100% Kubernetes environment?**
     Yes for **build** (OCI image format produced by `docker build`) even though the cluster's execution runtime is no longer `dockerd` but containerd/CRI-O (Part XVI, Ch.34).

31. 🔴 **Design the network architecture for a microservices stack with an isolated database.**
     `edge` network (publicly exposed reverse proxy), `services` network (microservices, internal communication by DNS name), isolated `data` network (DB, not exposed), each service joining only the networks it needs (Part VII, Ch.20).

32. 🟡 **What is the architectural difference between `bridge` and `overlay`?**
     `bridge` connects containers on the **same host**; `overlay` connects containers on **different hosts** via VXLAN encapsulation (Part VII, Ch.19).

33. 🔴 **How to securely integrate OCIR and OKE in an Oracle Cloud architecture?**
     IAM policies scoped by compartment/tenancy allowing OKE to pull from OCIR without manual `imagePullSecrets`, dedicated auth token (never the account password) for CI pushes (Part XI, Ch.29 + Part XV, Ch.33).

## Reasoning Exercises

34. 🔴 **A `docker build` works locally but fails in CI with "no space left on device". Diagnosis?**
     Build cache accumulated on the CI runner (`docker system df -v`), often ephemeral runners poorly cleaned between jobs or a build context too large (missing `.dockerignore`) — check both (Part VI, Ch.16 + Part XIII, Ch.31).

35. 🔴 **Two containers on the same custom Docker network cannot reach each other by name. Three possible causes?**
     (1) default `bridge` network without internal DNS instead of a custom network; (2) the app listens on `127.0.0.1` instead of `0.0.0.0` in the target container; (3) application firewall rule blocking inter-container traffic (Part VII, Ch.21).

36. 🔴 **A 2 GB image needs to be reduced. Priority order of optimizations?**
     1) Multi-stage build (remove build tools); 2) lighter base (alpine/distroless); 3) merging `RUN` + cleaning package cache in the same layer; 4) strict `.dockerignore` (Part VI, Ch.18).

37. 🔴 **A container is `healthy` according to Docker but the application does not respond to real user requests. Possible explanation?**
     The `HEALTHCHECK` probably tests too superficial an endpoint (e.g. static `/ping`) that does not reflect the real state of critical dependencies (DB, cache) — the healthcheck must verify actual functional capability, not just that the process responds (Part V, Ch.15).

38. 🔴 **A Kubernetes rolling update deployment switches all traffic to the new version before it is ready. Probable cause?**
     Missing correctly configured `readinessProbe` — without it, Kubernetes considers a pod ready as soon as it starts, not when it can actually handle requests (Part XVI, Ch.34).

## Real-World Debugging Scenarios

39. 🔴 **Scenario: a production service restarts in a loop every 30 seconds since a recent deployment.**
     Approach: `docker logs --tail 50` for the application error → `docker inspect --format='{{.State.ExitCode}}'` (137 = likely SIGKILL/OOM, 1 = handled application error) → check `OOMKilled` → check if a dependency (DB) is not ready (`depends_on`/healthcheck) → compare with the previous deployment configuration that worked (Part XIII, Ch.31).

40. 🔴 **Scenario: after an accidental `docker system prune -a --volumes` in production, a service no longer restarts.**
     The named volume containing data was deleted (no container was using it at prune time). Restore from the latest backup (Part VIII, Ch.24) — lesson: never run this command in production without first auditing active volumes (Part XIII, Ch.31).

41. 🔴 **Scenario: an application's logs appear empty in `docker logs` while the app is visibly running.**
     The application probably writes to an internal file rather than to stdout/stderr — the only stream captured by `docker logs`. Reconfigure the logger to stdout or mount/inspect the file via volume (Part XIII, Ch.31).

42. 🔴 **Scenario: a Docker-in-Docker CI pipeline fails intermittently on a shared runner.**
     `dind` requires `--privileged`, a source of instability and conflicts on shared runners. Consider "Docker-outside-of-Docker" mode (host socket mount) evaluating the associated security trade-off, or a dedicated runner isolated per job (Part XV, Ch.33).

43. 🔴 **Scenario: an image passes tests locally but a CI security scan blocks deployment.**
     The scan (Trivy/Docker Scout) detected a CVE in the base image or a dependency — check the report, update the affected base/dependency version, or document a temporary exception if the risk is accepted and tracked (Part XII, Ch.30).
