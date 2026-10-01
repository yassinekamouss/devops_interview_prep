# Partie XVI — Docker et Kubernetes

## Chapitre 34

### Pourquoi Kubernetes

Docker (standalone ou Compose) gère bien **un hôte**. Dès qu'il faut répartir des conteneurs sur plusieurs machines, gérer la panne d'un nœud, scaler automatiquement selon la charge, ou faire du déploiement progressif sans interruption à grande échelle, il faut un **orchestrateur**. Kubernetes est devenu le standard de facto de l'industrie pour ce rôle.

### Limites de Docker seul

| Limite de Docker standalone/Compose | Réponse de Kubernetes |
|---|---|
| Un seul hôte | Cluster multi-nœuds |
| Pas de reprogrammation automatique en cas de panne de nœud | Rescheduling automatique des pods |
| Scaling manuel (`docker compose up --scale`) | Autoscaling (HPA) basé sur métriques |
| Pas de découverte de service native multi-hôte | Services + DNS interne cluster-wide |
| Rollout/rollback basique | Stratégies de déploiement natives (rolling update, historique de révisions) |
| Pas de gestion déclarative de l'état désiré à l'échelle du cluster | Reconciliation loop permanente (l'état réel converge vers l'état déclaré) |

!!! danger "Piège d'entretien"
    Kubernetes **ne remplace pas** Docker — depuis la dépréciation de `dockershim` (Kubernetes 1.24+), les clusters n'utilisent d'ailleurs plus le daemon Docker directement mais un runtime conforme **CRI** (containerd, CRI-O). Les images restent cependant construites au format **OCI**, le même format produit par `docker build`. Docker reste donc central pour la partie *build*, même si `dockerd` n'est plus l'exécuteur runtime des conteneurs dans le cluster.

### Pods

Le **pod** est l'unité de déploiement minimale de Kubernetes — pas le conteneur. Un pod encapsule un ou plusieurs conteneurs qui partagent le même network namespace (même IP, même espace de ports) et peuvent partager des volumes.

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

!!! danger "Piège d'entretien fréquent"
    Confondre pod et conteneur est une erreur classique en entretien. Un pod peut contenir **plusieurs conteneurs** (pattern sidecar : conteneur principal + agent de logs, proxy, etc.), qui partagent le réseau (`localhost` fonctionne **entre eux**, contrairement à deux conteneurs Docker isolés — voir Partie VII, Chapitre 21) mais restent isolés au niveau filesystem sauf volumes partagés explicitement.

### Images

Kubernetes consomme directement les images construites par `docker build` (ou tout outil produisant une image conforme OCI — Buildah, Kaniko, BuildKit standalone). Aucune modification du Dockerfile n'est nécessaire pour passer de Docker à Kubernetes.

```yaml
spec:
  containers:
    - image: registry.exemple.com/mon-app:1.0
      imagePullPolicy: IfNotPresent   # Always | IfNotPresent | Never
```

!!! danger "Piège d'entretien : imagePullPolicy et latest"
    Si le tag est `latest`, `imagePullPolicy` bascule **implicitement** sur `Always` même non spécifié — chaque redémarrage de pod re-tire l'image, cassant potentiellement la reproductibilité et ralentissant les redémarrages. Encore une raison d'épingler des tags de version explicites (voir Partie IV, Chapitre 11).

### Registry

Kubernetes tire les images depuis n'importe quel registre compatible (Docker Hub, registre privé, OCIR — voir Partie XI). L'authentification passe par un `Secret` de type `docker-registry`, référencé via `imagePullSecrets` :

```yaml
spec:
  imagePullSecrets:
    - name: mon-secret-registre
  containers:
    - image: <région>.ocir.io/<namespace>/mon-app:1.0
```

Sur Oracle Kubernetes Engine (OKE), l'intégration IAM avec OCIR peut rendre ce secret inutile si les policies sont correctement configurées au niveau de la tenancy (voir Partie XV).

### Déploiement

Un `Deployment` gère un ensemble de pods identiques (réplicas), leur mise à jour progressive, et leur rescheduling automatique en cas de panne.

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

Le `readinessProbe` joue le même rôle que le `HEALTHCHECK` Docker (Partie V) : le pod ne reçoit du trafic qu'une fois déclaré prêt.

### Différences Docker vs Kubernetes

| | Docker (standalone/Compose) | Kubernetes |
|---|---|---|
| Portée | Un hôte | Cluster multi-nœuds |
| Unité de base | Conteneur | Pod (1+ conteneurs) |
| Réseau inter-service | DNS interne du réseau Docker | DNS interne (CoreDNS) + `Service` |
| Scaling | Manuel (`--scale`) | Manuel ou automatique (HPA) |
| Auto-réparation | `restart policy` locale | Rescheduling cluster-wide |
| Config déclarative | `compose.yaml` | Manifests YAML (Deployment, Service, ConfigMap...) |
| Secrets | `.env`, Compose `secrets:` | `Secret` (objet API dédié, RBAC) |

??? question "Question d'entretien : Pourquoi le format d'image reste-t-il compatible entre Docker et Kubernetes malgré la suppression de dockershim ?"
    Parce que Docker produit des images au format **OCI (Open Container Initiative)**, un standard indépendant du runtime d'exécution. Kubernetes exécute ces images via un runtime conforme **CRI** (containerd, CRI-O) qui sait lire ce même format OCI — la dépréciation de dockershim a changé l'exécuteur runtime dans le cluster, pas le format d'image produit par `docker build`.

??? question "Question d'entretien : Deux conteneurs dans le même pod peuvent-ils communiquer via `localhost` ?"
    Oui — c'est une différence fondamentale avec deux conteneurs Docker standalone (Partie VII, Chapitre 21). Les conteneurs d'un même pod partagent le **même network namespace** : ils ont la même IP et peuvent se joindre via `localhost:PORT`. C'est ce qui permet le pattern sidecar (proxy, agent de log, etc.).