# 11 - Production Triage: P95/P99 Latency, 5xx Codes & Network

During a production incident, a DevOps engineer should not panic. He must act like an emergency doctor: contain the hemorrhage, identify the failing organ, restore service and analyze the root cause cold. This chapter details the mapping of HTTP 5xx error codes and the mathematical method to deconstruct latency degradations.

---

## 1. The HTTP 5xx Error Compass

When a user receives a 5xx error, the framework tells you precisely at which level of the stack the break occurred:

```mermaid
flowchart TD
    Client["Client Web / Mobile"] --> Ingress["Ingress / AWS ALB (Reverse Proxy)"]
    Ingress --> ServiceK8s["Service Kubernetes (Endpoints)"]
    ServiceK8s --> PodApp["Pod Applicatif (Backend)"]
    PodApp --> External["Base de Données / API Tiers"]

    Ingress -.->|"Erreur 502 Bad Gateway"| Ingress
    Ingress -.->|"Erreur 504 Gateway Timeout"| Ingress
    PodApp -.->|"Erreur 500 Internal Error"| PodApp
    ServiceK8s -.->|"Erreur 503 Service Unavailable"| ServiceK8s
```

### Typology and Operational Responsibilities

| Code HTTP | Nom | Where is the fault located? | Common Root Cause |
|---|---|---|---|
| **500** | Internal Server Error | **In the application code** | Unhandled exception (`NullPointerException`, script crash, invalid SQL syntax). |
| **502** | Bad Gateway | **At the Reverse Proxy level (ALB/NGINX)** | The pod abruptly closed the TCP connection, crashed during the request, or is not listening on the expected port. |
| **503** | Service Unavailable | **Kubernetes network routing** | Zero pods ready to receive traffic (all pods have failed Readiness Probe or the Service has no endpoints). |
| **504** | Gateway Timeout | **At the Reverse Proxy level (ALB/NGINX)** | The application took longer to respond than the `timeout` configured on the Ingress/ALB (SQL query too slow, external API frozen). |

---

## 2. Deconstructing Latency: Why Average is an Illusion

One of the biggest mistakes in observability is monitoring **average latency**.

```mermaid
flowchart TD
    subgraph Population["Échantillon de 100 Requêtes Utilisateurs"]
        Fast["95 Requêtes traitées en 20ms"]
        Slow["5 Requêtes bloquées pendant 10 000ms (10s)"]
    end

    Population ==> Moyenne["Moyenne arithmétique = 519ms ('Acceptable' selon un dashboard naïf)"]
    Population ==> P95["Percentile P95 = 20ms"]
    Population ==> P99["Percentile P99 = 10 000ms (Catastrophe sur 5% des utilisateurs)"]

    style Slow fill:#d32f2f,stroke:#9a0007,color:#fff
    style P99 fill:#b71c1c,stroke:#7f0000,color:#fff
```

### The Role of Percentiles:
* **P50 (Median):** The typical user's experience in the middle of distribution.
* **P95:** 95% of queries run faster than this value. Used for standard navigation SLOs.
* **P99:** 1% of slowest requests (*Long-Tail Latency*). This is often where large customer basket requests, complex synchronizations or thread blockages hide.

### PromQL query to supervise P99:```promql
histogram_quantile(
  0.99,
  sum by (le, service) (rate(http_request_duration_seconds_bucket[5m]))
)
```

---

## 3. Bottleneck Location Matrix

If P99 explodes on an API route, how do we know which link in the chain is responsible?

```mermaid
flowchart LR
    subgraph LatenceTotale["Latence Totale Perçue par le Client"]
        direction TB
        L1["1. Latence Réseau (DNS + TCP / TLS Handshake)"]
        L2["2. File d'attente Ingress / Proxy Queue"]
        L3["3. Temps de Traitement CPU Applicatif"]
        L4["4. Temps d'Attente I/O (Database Queries / Cache Miss)"]
    end
```

### Elimination diagnostic protocol:

1. **Check AWS ALB Metrics:**
   * Inspect `TargetResponseTime`: if the time increases, the problem is with the Kubernetes backend. If `TargetResponseTime` is low but the client is waiting, the problem is in the network or TLS termination.
2. **Check the saturation of Workers (Pods):**
   *Are the pods running out of threads? Monitor the application metric of active threads (e.g. `jvm_threads_live_threads` or the Node.js worker pool).
3. **Check the persistence layer:**
   * Is the application waiting for the database? Look at the AWS RDS metrics (`ReadLatency`, `WriteLatency`, `DatabaseConnections`).

---

## 4. Playbook d'Incident Response en 4 Phases

In the event of a critical alert (`P1 / Sev-1`), apply this operational protocol:

```mermaid
flowchart TD
    P1["Phase 1 : Triage & Confinement (Stop the Bleeding)"]
    P2["Phase 2 : Investigation (Root Cause Analysis)"]
    P3["Phase 3 : Résolution & Déploiement du Correctif"]
    P4["Phase 4 : Post-Mortem Blameless"]

    P1 --> P2 --> P3 --> P4

    style P1 fill:#e53935,stroke:#b71c1c,color:#fff
    style P2 fill:#fb8c00,stroke:#e65100,color:#fff
    style P3 fill:#43a047,stroke:#1b5e20,color:#fff
    style P4 fill:#1e88e5,stroke:#0d47a1,color:#fff
```

### Phase 1: Triage and Containment
* **Objective:** Restore the service immediately for users, even if it means temporarily degrading certain secondary functionalities.
* **Typical actions:** 
  * Do a GitOps rollback to the previous stable commit.
  * Manually increase the number of service replicas (`kubectl scale`).
  * Activate a circuit breaker or deactivate a non-essential feature flag.

### Phase 2: Investigation (Do not erase the evidence!)
* Capture the state of failing pods before destroying them:```bash
  kubectl describe pod <pod-name> > crash-pod-describe.txt
  kubectl logs <pod-name> --previous > crash-pod-logs.txt
  ```* Extract the faulty distributed trace in Grafana Tempo / Jaeger via `TraceID`.

### Phase 3: Resolution
* Apply the patch as Infrastructure as Code (Terraform) or GitOps commit (ArgoCD). Zero manual manipulation on the production cluster.

### Phase 4: Blameless Post-Mortem
* Document the incident chronologically:
  1. *When did the incident start?*
  2. *When was it detected and by what alert?*
  3. *What was the user impact (Error Budget consumption)?*
  4. *What preventive actions (action items) will be taken so that this specific problem becomes impossible to reproduce?*

---

## 5. Frequently Asked Interview Questions

!!! question "Q: Your Ingress NGINX returns 502 errors randomly under heavy load. What is the most common cause?"
The classic cause is a **Keep-Alive Timeout** mismatch between Ingress and the backend application pod. If the backend closes the idle TCP connection after 60 seconds but the Ingress reuses the socket for 65 seconds, the Ingress sends a new request on a connection already closed by the pod, which instantly generates a 502 Bad Gateway error. To correct this, the backend's Keep-Alive Timeout must always be configured with a higher value than that of the Load Balancer / Ingress.

!!! question "Q: Your alerts indicate a global 503 error even though all your pods are in 'Running' status. How is this possible?"
A status `Running` only means that the container is running at the OS level. If the Readiness Probe of these pods fails (for example because the database is no longer responding and the application health check returns an error), Kubernetes immediately removes the IP from all the pods of the `Endpoints` of the Service. Ingress then no longer finds any healthy IP addresses to forward traffic to and responds with an `503 Service Unavailable` error.