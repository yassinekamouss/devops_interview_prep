# 08 - Security & RBAC Essentials

In a company, not everyone should have administrator rights on ArgoCD. An intern or junior developer should be able to view their application's logs, but not delete the production database.

This chapter summarizes the essential security principles to know for a junior position.

---

## 1. The First Rule: Change the `admin` Password

When installing ArgoCD on a cluster, a temporary random password is generated in a Kubernetes Secret named `argocd-initial-admin-secret`:

```bash
# Récupérer le mot de passe initial
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Changer immédiatement le mot de passe
argocd account update-password
```

!!! danger "Security Best Practice"
    Once the password is changed or SSO is configured, you must **delete** this initial Secret so no default credential remains stored on the cluster.

---

## 2. Enterprise Authentication (SSO / OIDC)

In production, engineers do not log in with a shared local account. ArgoCD is connected to the company's identity provider (**Google Workspace**, **GitHub Enterprise**, **Okta**, or **Keycloak**) via the **OIDC** protocol.

The user clicks *"Log in via Okta"* or *"Log in via GitHub"* and accesses ArgoCD with their usual credentials.

---

## 3. Access Control (RBAC)

ArgoCD includes its own permission system managed in a ConfigMap named **`argocd-rbac-cm`**.

### The Two Default Roles:
1. **`role:admin`:** Full privileges (create, modify, delete, sync all applications and all clusters). Reserved for the DevOps / Infra team.
2. **`role:readonly`:** View-only. Developers can see pods, the application tree, and logs, but cannot break anything.

### Simple RBAC Policy Example (`argocd-rbac-cm`):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  # Par défaut, tout nouvel arrivant est en lecture seule
  policy.default: role:readonly

  policy.csv: |
    # Les développeurs ont le droit de déclencher un "sync" sur leurs applications
    p, role:developer, applications, sync, mon-projet/*, allow
    
    # Association d'un groupe d'entreprise au rôle
    g, "Equipe-DevOps", role:admin
    g, "Equipe-Backend", role:developer
```

!!! tip "Web Terminal Feature (`exec`)"
    ArgoCD lets you open an interactive terminal inside containers directly from the browser. In production, this feature is generally **disabled** to comply with security standards (PCI-DSS, ISO 27001).

---

## 4. Frequent Interview Questions (Entry-Level)

!!! question "Q: How are user permissions managed in ArgoCD?"
    Through ArgoCD's native RBAC system configured in the `argocd-rbac-cm` ConfigMap. You can assign predefined roles (`role:readonly` or `role:admin`) or create specific rules to allow, for example, a team to sync only its own applications.

!!! question "Q: What is the first security measure to take after installing ArgoCD?"
    Retrieve the temporary password from the `argocd-initial-admin-secret` secret, change it immediately, then delete that initial secret from the `argocd` namespace.

!!! question "Q: How do companies handle team authentication on ArgoCD?"
    They configure Single Sign-On (SSO) via the OIDC protocol (with Google, Okta, Azure AD, or GitHub) so engineers use their individual corporate accounts rather than a shared admin account.
