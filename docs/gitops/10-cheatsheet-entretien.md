# 10 - Cheatsheet Entretien GitOps & ArgoCD (Niveau Junior / Entry-Level)

Ce document résume tout ce dont vous avez besoin pour réussir un entretien technique DevOps sur GitOps et ArgoCD.

---

## 1. Le Pitch Parfait de 2 Minutes (Introduction d'Entretien)

Si le recruteur vous dit : *"Parlez-moi de votre compréhension de GitOps et d'ArgoCD"* :

> *"Pour moi, le GitOps est l'évolution naturelle du CD sur Kubernetes. Au lieu d'utiliser un pipeline CI qui possède des droits administrateurs et qui pousse les changements avec `kubectl apply` (modèle Push), on utilise un opérateur comme **ArgoCD** qui s'exécute à l'intérieur du cluster (modèle Pull).*
> 
> *Git devient l'unique source de vérité : tout changement d'infrastructure passe par une Pull Request et un commit Git. ArgoCD surveille ce dépôt, applique les changements automatiquement, et offre du **Self-Healing** : si quelqu'un modifie manuellement le cluster avec `kubectl`, ArgoCD corrige la dérive pour rétablir l'état défini dans Git.*
> 
> *Cela améliore grandement la sécurité (aucun mot de passe de production dans le CI) et permet des rollbacks instantanés via un simple `git revert`."*

---

## 2. Comparatif Clé : Modèle Push vs Modèle Pull (GitOps)

| Critère | Modèle Push (Jenkins, GitLab CI, GitHub Actions) | Modèle Pull (ArgoCD) |
| :--- | :--- | :--- |
| **Où sont les clés K8s ?** | Dans le serveur CI (`kubeconfig` administrateur). | **Aucune clé dans le CI**. ArgoCD utilise son ServiceAccount interne. |
| **Ports réseau** | Le cluster doit ouvrir son port 6443 au monde extérieur. | Le cluster n'ouvre **aucun port entrant** (uniquement des requêtes sortantes vers Git). |
| **Modification manuelle** | Non détectée (le cluster dérive sans qu'on le sache). | **Détectée et corrigée automatiquement** (*Self-Healing*). |
| **Rollback** | Relancer un pipeline de déploiement complet. | Simple `git revert` du dernier commit. |

---

## 3. Les 10 Commandes `argocd` Indispensables

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

## 4. Les 10 Questions d'Entretien Incontournables

### 1. Qu'est-ce que le GitOps ?
> Une pratique d'exploitation où l'état désiré de l'infrastructure et des applications est entièrement décrit de façon déclarative dans un dépôt Git, et synchronisé automatiquement sur le cluster par un opérateur logiciel.

### 2. Pourquoi le modèle Pull est-il plus sécurisé que le modèle Push ?
> Parce que le serveur CI n'a plus besoin d'accéder au cluster ni de stocker des fichiers `kubeconfig` avec des droits sensibles. L'opérateur (ArgoCD) réside dans le cluster et fait de simples requêtes sortantes pour lire Git.

### 3. Qu'est-ce que le Configuration Drift et comment ArgoCD le résout-il ?
> Le drift est l'écart entre l'état décrit dans Git et l'état réel du cluster (par exemple suite à une commande `kubectl edit` manuelle). ArgoCD le résout grâce au **Self-Healing**, qui réapplique automatiquement la configuration déclarée dans Git pour annuler la modification manuelle.

### 4. Quelle est la différence entre `prune` et `selfHeal` dans une Application ArgoCD ?
> - `prune: true` supprime du cluster les objets qui ont été supprimés de Git.
> - `selfHeal: true` annule les modifications faites manuellement hors de Git sur le cluster.

### 5. Comment gérez-vous les secrets en GitOps sans les commiter en clair ?
> Soit via **Bitnami Sealed Secrets** (chiffrement asymétrique en local via `kubeseal`, le secret chiffré peut aller dans Git), soit via **External Secrets Operator (ESO)** (Git ne contient qu'une référence vers un coffre-fort externe comme AWS Secrets Manager ou HashiCorp Vault).

### 6. À quoi sert une Sync Wave ?
> À ordonnancer le déploiement des composants dans un ordre précis (ex: exécuter un Job de migration SQL en vague 0 avant de démarrer les nouveaux pods applicatifs en vague 1).

### 7. Quelle est la différence entre le statut `OutOfSync` et le statut `Degraded` ?
> `OutOfSync` indique une divergence entre le texte du fichier Git et les objets Kubernetes. `Degraded` indique un problème fonctionnel sur le cluster (pod en `CrashLoopBackOff`, mauvaise image ou sonde qui échoue).

### 8. À quoi sert le contrôleur ApplicationSet ?
> À générer automatiquement des dizaines d'applications ArgoCD à partir d'un modèle (template) et d'une liste de paramètres (ex: déployer le même microservice sur Dev, Staging et Prod).

### 9. Qu'est-ce qu'un déploiement Canary avec Argo Rollouts ?
> C'est une stratégie de déploiement où l'on envoie une petite partie du trafic réel (ex: 10%) vers la nouvelle version, pour vérifier sa stabilité avant de basculer 100% du trafic.

### 10. Pourquoi sépare-t-on le dépôt de code applicatif du dépôt de configuration GitOps ?
> Pour éviter les boucles de build infinies dans le CI, pour restreindre les droits d'accès à la production (seuls les DevOps/Leads valident les PRs d'infra) et pour faciliter les rollbacks sans recompiler l'application.
