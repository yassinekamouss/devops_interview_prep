# 08 - Sécurité & RBAC Essentiel

En entreprise, tout le monde ne doit pas avoir les droits administrateur sur ArgoCD. Un stagiaire ou un développeur junior doit pouvoir consulter les logs de son application, mais pas supprimer la base de données de production.

Ce chapitre résume les principes de sécurité indispensables à connaître pour un poste débutant.

---

## 1. La Première Règle : Changer le mot de passe `admin`

Lors de l'installation d'ArgoCD sur un cluster, un mot de passe temporaire aléatoire est généré dans un Secret Kubernetes nommé `argocd-initial-admin-secret` :

```bash
# Récupérer le mot de passe initial
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Changer immédiatement le mot de passe
argocd account update-password
```

!!! danger "Bonne pratique de sécurité"
    Une fois le mot de passe changé ou le SSO configuré, il faut **supprimer** ce Secret initial pour qu'aucun identifiant par défaut ne reste stocké sur le cluster.

---

## 2. Authentification Entreprise (SSO / OIDC)

En production, les ingénieurs ne se connectent pas avec un compte local partagé. On connecte ArgoCD au fournisseur d'identité de l'entreprise (**Google Workspace**, **GitHub Enterprise**, **Okta**, ou **Keycloak**) via le protocole **OIDC**.

L'utilisateur clique sur *"Log in via Okta"* ou *"Log in via GitHub"* et accède à ArgoCD avec ses identifiants habituels.

---

## 3. Le Contrôle d'Accès (RBAC)

ArgoCD intègre son propre système de permissions géré dans une ConfigMap nommée **`argocd-rbac-cm`**.

### Les Deux Rôles par Défaut :
1. **`role:admin` :** Les pleins pouvoirs (créer, modifier, supprimer, synchroniser toutes les applications et tous les clusters). Réservé à l'équipe DevOps / Infra.
2. **`role:readonly` :** Consultation uniquement. Les développeurs peuvent voir les pods, l'arbre des applications et les logs, mais ne peuvent rien casser.

### Exemple simple de politique RBAC (`argocd-rbac-cm`) :

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

!!! tip "La fonctionnalité Terminal Web (`exec`)"
    ArgoCD permet d'ouvrir un terminal interactif dans les conteneurs directement depuis le navigateur. En production, cette fonctionnalité est généralement **désactivée** pour respecter les normes de sécurité (PCI-DSS, ISO 27001).

---

## 4. Questions d'Entretien Fréquentes (Niveau Entry-Level)

!!! question "Q: Comment gère-t-on les permissions des utilisateurs dans ArgoCD ?"
    On utilise le système de RBAC natif d'ArgoCD configuré dans la ConfigMap `argocd-rbac-cm`. On peut attribuer des rôles prédéfinis (`role:readonly` ou `role:admin`) ou créer des règles spécifiques pour autoriser par exemple une équipe à synchroniser uniquement ses propres applications.

!!! question "Q: Quelle est la première mesure de sécurité à prendre après avoir installé ArgoCD ?"
    Récupérer le mot de passe temporaire dans le secret `argocd-initial-admin-secret`, le changer immédiatement, puis supprimer ce secret initial du namespace `argocd`.

!!! question "Q: Comment les entreprises gèrent-elles l'authentification des équipes sur ArgoCD ?"
    Elles configurent le Single Sign-On (SSO) via le protocole OIDC (avec Google, Okta, Azure AD ou GitHub) afin que les ingénieurs utilisent leurs comptes d'entreprise individuels plutôt qu'un compte admin partagé.
