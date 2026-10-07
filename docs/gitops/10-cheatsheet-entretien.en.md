# 10 - GitOps & ArgoCD Interview Cheatsheet (Junior / Entry-Level)

This document summarizes everything you need to ace a DevOps technical interview on GitOps and ArgoCD.

---

## 1. The Perfect 2-Minute Pitch (Interview Introduction)

If the recruiter says: *"Tell me about your understanding of GitOps and ArgoCD"*:

> *"For me, GitOps is the natural evolution of CD on Kubernetes. Instead of using a CI pipeline that holds administrator privileges and pushes changes with `kubectl apply` (Push model), we use an operator like **ArgoCD** that runs inside the cluster (Pull model).*
> 
> *Git becomes the single source of truth: every infrastructure change goes through a Pull Request and a Git commit. ArgoCD watches this repository, applies changes automatically, and provides **Self-Healing**: if someone manually modifies the cluster with `kubectl`, ArgoCD corrects the drift to restore the state defined in Git.*
> 
> *This greatly improves security (no production password in CI) and enables instant rollbacks via a simple `git revert`."*

---

## 2. Key Comparison: Push vs Pull Model (GitOps)

| Criterion | Push Model (Jenkins, GitLab CI, GitHub Actions) | Pull Model (ArgoCD) |
| :--- | :--- | :--- |
| **Where are K8s credentials?** | On the CI server (admin `kubeconfig`). | **No credentials in CI**. ArgoCD uses its internal ServiceAccount. |
| **Network ports** | The cluster must expose port 6443 to the outside world. | The cluster opens **no inbound ports** (only outbound requests to Git). |
| **Manual modification** | Not detected (cluster drifts silently). | **Detected and automatically fixed** (*Self-Healing*). |
| **Rollback** | Re-run a full deployment pipeline. | Simple `git revert` of the last commit. |

---

## 3. The 10 Essential `argocd` Commands

```bash
# 1. Connexion au serveur ArgoCD
argocd login argocd.mon-entreprise.com --username admin

# 2. Lister toutes les applications et leur statut (Synced, Healthy)
argocd app list

# 3. Afficher les détails complets d'une application
argocd app get mon-app

# 4. Afficher le diff exact entre Git et le cluster
argocd app diff mon-app

# 5. Déclencher une synchronisation manuelle
argocd app sync mon-app

# 6. Synchroniser en forçant et en supprimant les ressources orphelines
argocd app sync mon-app --prune

# 7. Voir l'historique des déploiements passés
argocd app history mon-app

# 8. Revenir à une ancienne version saine (Rollback)
argocd app rollback mon-app 2

# 9. Désactiver temporairement l'auto-sync en cas d'intervention urgente
argocd app set mon-app --sync-policy manual

# 10. Forcer le rafraîchissement immédiat du cache Git
argocd app get mon-app --refresh
```

---

## 4. The 10 Must-Know Interview Questions

### 1. What is GitOps?
> A practice where the desired state of infrastructure and applications is fully described declaratively in a Git repository and automatically synchronized to the cluster by a software operator.

### 2. Why is the Pull model more secure than the Push model?
> Because the CI server no longer needs to access the cluster or store `kubeconfig` files with sensitive privileges. The operator (ArgoCD) resides inside the cluster and makes simple outbound requests to read Git.

### 3. What is Configuration Drift and how does ArgoCD solve it?
> Drift is the gap between the state described in Git and the actual state of the cluster (for example after a manual `kubectl edit` command). ArgoCD solves it with **Self-Healing**, which automatically reapplies the configuration declared in Git to undo the manual change.

### 4. What is the difference between `prune` and `selfHeal` in an ArgoCD Application?
> - `prune: true` deletes from the cluster objects that have been removed from Git.
> - `selfHeal: true` reverts manual changes made outside Git on the cluster.

### 5. How do you handle secrets in GitOps without committing them in plain text?
> Either via **Bitnami Sealed Secrets** (local asymmetric encryption via `kubeseal`, the encrypted secret can go to Git), or via **External Secrets Operator (ESO)** (Git contains only a reference to an external vault like AWS Secrets Manager or HashiCorp Vault).

### 6. What is a Sync Wave used for?
> To order the deployment of components in a precise sequence (e.g., run an SQL migration Job in wave 0 before starting new application pods in wave 1).

### 7. What is the difference between `OutOfSync` and `Degraded` status?
> `OutOfSync` indicates a divergence between the Git file text and Kubernetes objects. `Degraded` indicates a functional problem on the cluster (pod in `CrashLoopBackOff`, bad image or failing probe).

### 8. What is the ApplicationSet controller used for?
> To automatically generate dozens of ArgoCD applications from a template and a parameter list (e.g., deploying the same microservice to Dev, Staging, and Prod).

### 9. What is a Canary deployment with Argo Rollouts?
> It is a deployment strategy where a small portion of real traffic (e.g., 10%) is sent to the new version to verify its stability before switching 100% of traffic over.

### 10. Why separate the application code repository from the GitOps configuration repository?
> To avoid infinite build loops in CI, to restrict production access rights (only DevOps/Leads approve infra PRs), and to make rollbacks easier without recompiling the application.
