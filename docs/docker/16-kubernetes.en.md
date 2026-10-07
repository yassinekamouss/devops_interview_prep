# Part XVI — Docker and Kubernetes

## Chapter 34

### Why Kubernetes

Docker (standalone or Compose) handles **one host** well. As soon as you need to distribute containers across multiple machines, handle a node failure, automatically scale based on load, or perform large-scale progressive deployment without interruption, you need an **orchestrator**. Kubernetes has become the de facto industry standard for this role.

### Limitations of Docker Alone

| Limitation of standalone Docker/Compose | Kubernetes answer |
|---|---|
| Single host | Multi-node cluster |
| No automatic rescheduling if a node fails | Automatic pod rescheduling |
| Manual scaling (`docker compose up --scale`) | Autoscaling (HPA) based on metrics |
| No native multi-host service discovery | Services + cluster-wide internal DNS |
| Basic rollout/rollback | Native deployment strategies (rolling update, revision history) |
| No declarative management of desired state at cluster scale | Permanent reconciliation loop (actual state converges to declared state) |

!!! danger "Interview Trap"
    Kubernetes **does not replace** Docker — since the deprecation of `dockershim` (Kubernetes 1.24+), clusters no longer use the Docker daemon directly but a **CRI**-compliant runtime (containerd, CRI-O). Images nevertheless remain built in **OCI** format, the same format produced by `docker build`. Docker therefore remains central for the *build* part, even if `dockerd` is no longer the runtime executor for containers in the cluster.

### Pods

The **pod** is the minimal deployment unit in Kubernetes — not the container. A pod encapsulates one or more containers that share the same network namespace (same IP, same port space) and can share volumes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mon-app
spec:
  containers:
    - name: app
      image: registry.exemple.com/mon-app:1.0
      ports:
        - containerPort: 8080
    - name: sidecar-logs
      image: fluent-bit:latest
```

!!! danger "Frequent Interview Trap"
    Confusing pod and container is a classic interview mistake. A pod can contain **multiple containers** (sidecar pattern: main container + log agent, proxy, etc.), which share the network (`localhost` works **between them**, unlike two isolated Docker containers — see Part VII, Chapter 21) but remain isolated at the filesystem level except for explicitly shared volumes.

### Images

Kubernetes directly consumes images built by `docker build` (or any tool producing an OCI-compliant image — Buildah, Kaniko, standalone BuildKit). No Dockerfile modification is needed to move from Docker to Kubernetes.

```yaml
spec:
  containers:
    - image: registry.exemple.com/mon-app:1.0
      imagePullPolicy: IfNotPresent   # Always | IfNotPresent | Never
```

!!! danger "Interview Trap: imagePullPolicy and latest"
    If the tag is `latest`, `imagePullPolicy` implicitly switches to `Always` even if not specified — each pod restart re-pulls the image, potentially breaking reproducibility and slowing restarts. Another reason to pin explicit version tags (see Part IV, Chapter 11).

### Registry

Kubernetes pulls images from any compatible registry (Docker Hub, private registry, OCIR — see Part XI). Authentication goes through a `Secret` of type `docker-registry`, referenced via `imagePullSecrets`:

```yaml
spec:
  imagePullSecrets:
    - name: mon-secret-registre
  containers:
    - image: <région>.ocir.io/<namespace>/mon-app:1.0
```

On Oracle Kubernetes Engine (OKE), IAM integration with OCIR can make this secret unnecessary if policies are correctly configured at the tenancy level (see Part XV).

### Deployment

A `Deployment` manages a set of identical pods (replicas), their progressive update, and their automatic rescheduling in case of failure.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mon-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: mon-app
  template:
    metadata:
      labels:
        app: mon-app
    spec:
      containers:
        - name: app
          image: registry.exemple.com/mon-app:1.0
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
```

The `readinessProbe` plays the same role as Docker's `HEALTHCHECK` (Part V): the pod only receives traffic once declared ready.

### Differences Docker vs Kubernetes

| | Docker (standalone/Compose) | Kubernetes |
|---|---|---|
| Scope | Single host | Multi-node cluster |
| Base unit | Container | Pod (1+ containers) |
| Inter-service network | Docker network internal DNS | Internal DNS (CoreDNS) + `Service` |
| Scaling | Manual (`--scale`) | Manual or automatic (HPA) |
| Self-healing | Local `restart policy` | Cluster-wide rescheduling |
| Declarative config | `compose.yaml` | YAML manifests (Deployment, Service, ConfigMap...) |
| Secrets | `.env`, Compose `secrets:` | `Secret` (dedicated API object, RBAC) |

??? question "Interview Question: Why does the image format remain compatible between Docker and Kubernetes despite the removal of dockershim?"
    Because Docker produces images in **OCI (Open Container Initiative)** format, a standard independent of the execution runtime. Kubernetes runs these images via a **CRI**-compliant runtime (containerd, CRI-O) that knows how to read this same OCI format — the deprecation of dockershim changed the runtime executor in the cluster, not the image format produced by `docker build`.

??? question "Interview Question: Can two containers in the same pod communicate via `localhost`?"
    Yes — this is a fundamental difference from two standalone Docker containers (Part VII, Chapter 21). Containers in the same pod share the **same network namespace**: they have the same IP and can reach each other via `localhost:PORT`. This is what enables the sidecar pattern (proxy, log agent, etc.).
