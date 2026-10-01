# Partie IX — Variables d'environnement

## Chapitre 25

### ENV

Définie dans le Dockerfile ou via `docker run -e`, persiste dans l'image (`ENV`) ou uniquement à l'exécution (`-e`).

```dockerfile
ENV NODE_ENV=production
```

```bash
docker run -e NODE_ENV=production mon-app
docker run --env-file .env mon-app
```

### ARG

Disponible **uniquement pendant le build**, absente du conteneur en exécution sauf si réinjectée via `ENV` (voir Partie VI, Chapitre 17).

```dockerfile
ARG BUILD_VERSION
ENV APP_VERSION=$BUILD_VERSION
```

### Secrets

!!! danger "Piège d'entretien"
    `ENV` et `ARG` sont visibles en clair via `docker inspect` et `docker history` — **jamais** de mot de passe, clé API ou token dans ces deux mécanismes. Utiliser à la place :
    
    - Docker Compose : `secrets:` (montés en fichier, pas en variable).
    - BuildKit : `RUN --mount=type=secret,id=mysecret` (secret disponible uniquement pendant l'exécution du `RUN`, jamais persistant dans une couche).
    - En orchestration : Kubernetes Secrets, Vault, ou les gestionnaires de secrets cloud (AWS Secrets Manager, Oracle Vault).

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    curl -H "Authorization: Bearer $API_KEY" https://exemple.com
```

```bash
docker build --secret id=api_key,src=./api_key.txt .
```

### .env

Fichier de variables consommé automatiquement par `docker compose` (pas par `docker run`, qui nécessite `--env-file` explicite).

```
# .env
DB_USER=admin
DB_PASSWORD=changeme
```

```yaml
services:
  db:
    environment:
      - POSTGRES_USER=${DB_USER}
```

!!! danger "Piège d'entretien"
    Un fichier `.env` à la racine d'un projet Compose est chargé **implicitement** par `docker compose` — mais `docker run` ne le lit jamais sans `--env-file .env` explicite. Confusion fréquente entre les deux comportements.

### Injection

Ordre de priorité (le plus prioritaire en dernier) pour Compose : valeurs par défaut du Dockerfile (`ENV`) < fichier `.env` < `environment:` du compose.yaml < variable shell exportée au moment de `docker compose up` < `-e` en ligne de commande pour `docker run` standalone.

??? question "Question d'entretien : Pourquoi ne jamais stocker un secret dans une variable ENV du Dockerfile ?"
    Parce qu'elle est gravée dans une couche de l'image, visible par quiconque a accès à l'image (`docker history`, `docker inspect`), y compris après suppression apparente du fichier dans une couche ultérieure (les couches précédentes restent accessibles). Un secret doit être injecté **au runtime**, jamais au build, sauf via le mécanisme `--mount=type=secret` qui ne persiste pas dans l'image finale.