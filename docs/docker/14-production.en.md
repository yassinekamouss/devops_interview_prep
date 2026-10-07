# Part XIV — Docker in Production

## Chapter 32

### Best Practices

- Images explicitly versioned (never `latest`, see Part IV, Chapter 11).
- Resource limits defined on each container (Part V, Chapter 15).
- `HEALTHCHECK` defined and used by the orchestrator.
- Non-root user (Part XII).
- Logs sent to stdout/stderr, never to files inside the container.
- Configuration externalized (environment variables, secrets), never hard-coded in the image.
- Private registry with automated vulnerability scanning before each deployment.

### Monitoring

Container monitoring typically combines three levels:

| Level | Typical tools | What is measured |
|---|---|---|
| Host | Node Exporter, cAdvisor | Machine CPU/RAM/disk |
| Container | cAdvisor, `docker stats` | Resources per container (cgroups) |
| Application | Prometheus client, APM (Datadog, New Relic) | Business metrics, latency, error rate |

`cAdvisor` (Container Advisor, Google) is the reference for exposing per-container cgroup metrics in Prometheus format.

### Logging

In production, logs must **never** stay only in `docker logs` (default daemon rotation if misconfigured = loss of old logs). Two approaches:

- **Docker log driver**: configure `--log-driver` (json-file with rotation, `syslog`, `journald`, `awslogs`, `gelf` to Logstash/Graylog) to send logs to a centralized system directly from the daemon.
- **Collection sidecar**: an agent container (Fluentd, Filebeat, Vector) that reads logs and ships them to a backend (ELK, Loki, Splunk).

### Log Rotation

```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

!!! danger "Interview Trap"
    Without rotation configuration (`log-opts`), the default `json-file` driver has **no size limit** — a verbose container can fill the host disk with its logs alone until causing a complete outage (including the Docker daemon itself). This is a real and frequent cause of production incidents.

### High Availability

Docker alone (standalone mode) offers **no native multi-host high availability**: if the host goes down, all its containers go down with it. HA requires an orchestrator:

- **Docker Swarm**: service replication, automatic distribution across multiple nodes, rescheduling if a node fails.
- **Kubernetes**: richer equivalent, industry standard (see Part XVI).

### Update Strategies

| Strategy | Principle | Advantage | Disadvantage |
|---|---|---|---|
| Recreate | Full stop, then start of the new version | Simple | Service interruption |
| Rolling update | Progressive replacement instance by instance | No total interruption | Temporary coexistence of two versions |
| Blue-Green | Switch from one full environment to another at once | Instant rollback | Requires double resources during switch |
| Canary | Deployment to a small subset of traffic first | Early detection of regressions | Additional routing complexity |

### Rollback

```bash
# Docker Swarm
docker service update --rollback mon-service

# Compose (approche manuelle : redéployer le tag précédent)
docker compose up -d --no-deps app  # après avoir changé le tag d'image dans le compose.yaml
```

Rollback must be **tested before** you urgently need it — a previous image must remain available in the registry (appropriate retention policy), and the database must remain compatible with both application versions during the transition (beware of destructive schema migrations).

??? question "Interview Question: How to guarantee a zero-downtime deployment with Docker?"
    Combine: reliable `HEALTHCHECK`, rolling update or blue-green strategy driven by an orchestrator (Swarm/Kubernetes) or a reverse proxy (Traefik, Nginx) capable of removing an instance from the pool as long as it is not `healthy`, and `depends_on: condition: service_healthy` to route traffic only to truly ready instances.

??? question "Interview Question: What happens to logs if you do not configure `log-opts`?"
    The default `json-file` driver accumulates logs without size limit or automatic rotation — risk of host disk saturation in the medium/long term. Always define `max-size`/`max-file` explicitly, or delegate retention to a centralized collection system.
