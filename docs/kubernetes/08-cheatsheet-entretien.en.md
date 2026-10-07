# 08 - R&D Interview Cheatsheet

This document is your ultimate safety net for technical interviews in software engineering, DevOps, Cloud and MLOps at Oracle R&D. It condenses architectural decision matrices, low-level internal mechanics and surgical investigation commands.

---

## 1. Architectural Comparisons & Decision Matrices (R&D Level)

| Comparison | Expected Explanation in an R&D Interview |
| :--- | :--- |
| **Docker Compose vs K8s** | Compose is for local dev (single host). K8s is for prod (multi-host, auto-healing, rolling updates, RBAC, SDN). |
| **Deployment vs StatefulSet** | Deployment for Stateless (APIs, web). StatefulSet for Stateful (Kafka, DBs) requiring a stable network identity (`ordinal`), strict ordering and attached persistent storage (`volumeClaimTemplates`). |
| **Service vs Ingress vs Gateway API** | - **Service:** Internal TCP/UDP load balancing (Layer 4).<br>- **Ingress:** External HTTP/HTTPS routing (Layer 7) based on host/URL, limited expressiveness.<br>- **Gateway API:** The modern K8s standard (SIG-Network) replacing Ingress: role-oriented architecture (Infra Provider vs App Developer), dynamic cross-namespace routing, native L4/L7 support and direct gRPC. |
| **HPA vs VPA vs Cluster Autoscaler** | - **HPA:** Adds Pod replicas (Horizontal).<br>- **VPA:** Adjusts Pod CPU/RAM size (Vertical - often requires restart).<br>- **Cluster Autoscaler / Karpenter:** Adds/removes physical nodes/VMs as soon as Pods go `Pending`. |
| **CNI: Calico vs Cilium vs OCI VCN-Native** | - **Calico:** Native BGP routing or VXLAN, classic iptables NetworkPolicies.<br>- **Cilium:** **eBPF** engine, bypass of host TCP/IP stack, L7 Hubble observability without sidecar, transparent WireGuard encryption.<br>- **OCI VCN-Native:** Zero encapsulation overhead, IP directly routable in the Oracle VCN, **RoCEv2** support for distributed GPU training. |

---

## 2. Survival Commands & Advanced Zsh CLI Arsenal

!!! success "The Essential Alias"
    At the start of a technical test, immediately configure your Zsh terminal:
    ```bash
    alias k=kubectl
    export do="--dry-run=client -o yaml"
    ```

### Fundamental Survival Commands
- `k describe pod <pod-name>` : The first command to type if a pod fails to start (check the `Events` section).
- `k logs <pod-name>` : Read container logs.
- `k logs <pod-name> --previous` : Read logs of the container before its last crash (vital for `CrashLoopBackOff`).
- `k exec -it <pod-name> -- /bin/sh` : Open a shell in a running pod to test internal networking (`curl`, `ping`).
- `k get nodes -o wide` : Check node status and IP.
- `k top pods` / `k top nodes` : Check CPU/RAM consumption (requires Metrics Server).
- `k get events --sort-by='.metadata.creationTimestamp'` : See everything happening in the cluster in real time.

### The 10 Essential R&D One-Liners (Zsh & JSONPath)

```bash
# 1. Lister tous les Pods qui ne sont PAS en statut Running sur l'ensemble du cluster
k get pods -A --field-selector status.phase!=Running

# 2. Détecter les Deployments dangereux en production : AUCUNE readinessProbe configurée
k get deploy -A -o jsonpath='{range .items[?(!.spec.template.spec.containers[0].readinessProbe)]}{.metadata.namespace}{"/"}{.metadata.name}{"\n"}{end}'

# 3. Détecter les Pods en classe QoS BestEffort (interdits en prod car premières cibles de l'OOM Killer)
k get pods -A -o jsonpath='{range .items[?(@.status.qosClass=="BestEffort")]}{.metadata.namespace}{"/"}{.metadata.name}{"\n"}{end}'

# 4. Extraire les conteneurs ayant redémarré avec leur exit code Linux exact (Exit 137 = OOMKilled)
k get pods -A -o jsonpath='{range .items[?(@.status.containerStatuses[*].restartCount>0)]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{range .status.containerStatuses[*]}{"Conteneur:"}{.name}{" Restarts:"}{.restartCount}{" ExitCode:"}{.lastState.terminated.exitCode}{end}{"\n"}{end}'

# 5. Déployer instantanément un conteneur éphémère de test réseau avec destruction automatique (--rm)
k run debug-probe --rm -it --image=nicolaka/netshoot -- /bin/bash

# 6. Auditer les permissions effectives d'un ServiceAccount (Impersonation)
k auth can-i delete pods --as=system:serviceaccount:production:cicd-sa -n production

# 7. Trouver tous les PVC orphelins non montés par des Pods
comm -23 <(k get pvc -A -o custom-columns=NAME:.metadata.name --no-headers | sort) \
         <(k get pods -A -o jsonpath='{.items[*].spec.volumes[*].persistentVolumeClaim.claimName}' | tr ' ' '\n' | sort -u)

# 8. Mesurer la latence DNS réelle depuis l'intérieur d'un pod vers CoreDNS
k run -it --rm dns-test --image=busybox -- time nslookup kubernetes.default

# 9. Supprimer d'urgence un Pod bloqué en Terminating (Attention aux VolumeAttachments !)
k delete pod <pod-name> --grace-period=0 --force

# 10. Afficher les événements d'erreur récents triés chronologiquement
k get events -A --field-selector type=Warning --sort-by='.lastTimestamp'
```

---

## 3. Essential Production YAML Manifests

### A. Pod Security Standards (PSS) at Namespace Level

In modern production (Kubernetes 1.25+), `PodSecurityPolicies` (deprecated) are replaced by native **Pod Security Standards (PSS)** labels:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production-restricted
  labels:
    # Applique le profil de sécurité le plus strict (interdiction de root, de hostNetwork, etc.)
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    # Avertit les développeurs dans kubectl sans bloquer les pods en cas de non-conformité
    pod-security.kubernetes.io/warn: restricted
```

### B. Gateway API: HTTPRoute (The Ingress Replacement)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: payment-route
  namespace: production
spec:
  parentRefs:
  - name: internal-gateway
    namespace: infra-gateways
  hostnames:
  - "payment.oraclecloud.internal"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /v2/checkout
    backendRefs:
    - name: checkout-service
      port: 8080
      weight: 90
    - name: checkout-canary
      port: 8080
      weight: 10              # Split de trafic Canary natif sans plugin Ingress tiers
```

---

## 4. Top Interview Scenarios (Oracle R&D Situational Questions)

!!! question "Scenario: A deployment was just made, but users are getting 502/503 errors. What do you do?"
    **Action:** I check the Pod status (`k get pods`). If they are crashing, I read the logs. If they are *Running*, I check the *Readiness Probe* via `k describe pod`. If it fails, Pods are removed from the *Service*, so the *Ingress* has nowhere to send traffic.

!!! question "Scenario: You need to deploy a heavy Machine Learning model (10Gi RAM). How do you isolate it?"
    **Action:** I use *Taints* on specific nodes (e.g., RAM/GPU-optimized instances) and add a *Toleration* as well as a *NodeAffinity* in the model's Deployment to ensure it lands on the right machine without disrupting classic APIs.

!!! question "Oracle Interview Scenario: Cluster Completely Frozen Due to etcd Space Quota Saturation"
    **Examiner:** "No more modifications are possible on the cluster. All `kubectl apply` or `helm upgrade` commands return the fatal error: `etcdserver: mvcc: database space exceeded`. The API Server refuses any write. 
    1. What is the underlying cause of this blockage?
    2. Why is simply deleting old Deployments with `kubectl delete` impossible?
    3. What is the exact surgical procedure to restore the cluster?"

    **Structured Answer Expected from the Candidate:**

    1. **Underlying Cause:**
       - etcd has a default safety storage limit (`--quota-backend-bytes`, typically 2GB, expandable to 8GB max).
       - Due to the accumulation of old MVCC revisions (pod creations, cronjobs, secrets), the `bbolt` database has reached this quota. Once the quota is exceeded, etcd triggers a `NOSPACE` alarm and switches the entire cluster to strict read-only mode.

    2. **Impossibility of `kubectl delete`:**
       - Under etcd, a deletion is actually a **new MVCC write** (generating a *tombstone* record with a new incremented global revision). Attempting to delete an object requires additional disk space and therefore fails with the same error.

    3. **Surgical Unblocking Procedure:**
       - **Step 1: Get the current etcd revision**:
         `rev=$(etcdctl endpoint status --write-out="json" | jq .[0].Status.header.revision)`
       - **Step 2: Compact history up to the current revision**:
         `etcdctl compact $rev`
       - **Step 3: Defragment the bbolt file to return empty blocks to the OS**:
         `etcdctl defrag --endpoints=https://127.0.0.1:2379`
       - **Step 4: Disable the safety alarm**:
         `etcdctl alarm disarm`
       - **Step 5 (Long-term fix):** Configure `--auto-compaction-retention=1h` and increase `--quota-backend-bytes=8589934592` (8GB) in the static arguments of kube-apiserver/etcd.

!!! question "Oracle Interview Scenario: Pod Stuck Indefinitely in `Terminating` Status (Orphaned Finalizer)"
    **Examiner:** "An application Pod was deleted 3 hours ago but remains stuck in `Terminating` status. The Kubelet has already stopped the physical container on the host machine. What is blocking deletion in the Kubernetes API and how to unblock it cleanly?"

    **Structured Answer Expected from the Candidate:**

    1. **Root Cause (Finalizers):**
       - In Kubernetes, when an object has `.metadata.finalizers`, the API Server does not delete the etcd record on a `DELETE`. It merely sets a `deletionTimestamp`.
       - The object remains visible with `Terminating` status as long as a third-party controller (e.g., a storage operator, service mesh or backup controller) has not finalized its cleanup operations and removed its key from the finalizers list.
       - If the external controller is crashed or uninstalled, the Pod remains stuck forever.

    2. **Diagnosis & Resolution:**
       - Inspect the list of blocking finalizers:
         `kubectl get pod <pod-name> -o jsonpath='{.metadata.finalizers}'`
       - Emergency resolution: If the container is confirmed dead on the physical node and no data damage will occur, remove the blocking finalizer via hot JSON patch:
         `kubectl patch pod <pod-name> -p '{"metadata":{"finalizers":null}}' --type=merge`
       - The API Server immediately deletes the object from etcd without waiting.
