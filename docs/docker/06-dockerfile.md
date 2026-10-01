# Partie VI — Dockerfile

## Chapitre 16 : Dockerfile

### Syntaxe

Un Dockerfile est une suite d'instructions, chacune sur une ligne, exécutées **séquentiellement** par le builder pour produire une image, couche par couche.

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Structure

Chaque instruction qui modifie le filesystem (`RUN`, `COPY`, `ADD`) crée une **nouvelle couche**. Les instructions de métadonnées (`ENV`, `LABEL`, `EXPOSE`, `CMD`, `ENTRYPOINT`) ne créent pas de couche filesystem mais mettent à jour la configuration de l'image.

### Build Context

```bash
docker build -t mon-app:1.0 .
```

Le `.` final est le **build context** : l'ensemble des fichiers envoyés au daemon Docker pour construire l'image. Tout ce qui est dans ce répertoire est transféré (sauf ce qui est exclu via `.dockerignore`), même les fichiers non utilisés par le Dockerfile.

```
# .dockerignore
.git
node_modules
*.log
.env
```

!!! danger "Piège d'entretien"
    Un build context trop large (ex. oubli d'exclure `.git` ou `node_modules`) ralentit fortement le build et peut faire fuiter des secrets dans les couches de l'image si un fichier sensible est copié par erreur (`COPY . .`). Toujours maintenir un `.dockerignore` strict.

### Cache

Docker met en cache chaque couche. Si l'instruction et son contexte (fichiers copiés, checksum) n'ont pas changé depuis le dernier build, la couche est **réutilisée** sans réexécution.

```dockerfile
# Mauvais ordre : invalide le cache pip à chaque changement de code
COPY . .
RUN pip install -r requirements.txt

# Bon ordre : le cache pip survit tant que requirements.txt ne change pas
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

!!! danger "Piège d'entretien classique"
    L'ordre des instructions dans un Dockerfile a un impact direct sur la vitesse de build. Règle générale : placer en premier ce qui change **le moins souvent** (dépendances) et en dernier ce qui change **le plus souvent** (code source applicatif), afin de maximiser la réutilisation du cache.

---

## Chapitre 17 : Toutes les instructions Dockerfile

| Instruction | Rôle |
|---|---|
| `FROM` | Image de base |
| `RUN` | Exécute une commande au moment du build (nouvelle couche) |
| `CMD` | Commande par défaut exécutée au démarrage (surchargeable) |
| `ENTRYPOINT` | Point d'entrée fixe (non surchargeable sans `--entrypoint`) |
| `COPY` | Copie des fichiers du build context vers l'image |
| `ADD` | Comme `COPY`, avec extraction d'archives et support d'URL |
| `WORKDIR` | Définit le répertoire de travail courant |
| `ENV` | Définit une variable d'environnement (persiste dans le conteneur) |
| `ARG` | Variable disponible uniquement au moment du build |
| `LABEL` | Ajoute des métadonnées (clé/valeur) à l'image |
| `EXPOSE` | Documente le port utilisé (n'ouvre rien réellement) |
| `USER` | Définit l'utilisateur d'exécution des instructions suivantes et du conteneur |
| `SHELL` | Change le shell utilisé pour les instructions `RUN` en forme shell |
| `HEALTHCHECK` | Définit une commande de vérification de santé |
| `STOPSIGNAL` | Change le signal envoyé par `docker stop` (par défaut SIGTERM) |
| `ONBUILD` | Déclenche une instruction dans les images **filles** qui héritent de celle-ci |
| `VOLUME` | Déclare un point de montage comme volume anonyme |

### CMD vs ENTRYPOINT

```dockerfile
# CMD seul : entièrement surchargeable
CMD ["nginx", "-g", "daemon off;"]
# docker run mon-image echo hello   -> exécute "echo hello", ignore CMD

# ENTRYPOINT seul : les arguments de "docker run" s'ajoutent à la suite
ENTRYPOINT ["python", "app.py"]
# docker run mon-image --debug   -> exécute "python app.py --debug"

# Combinaison ENTRYPOINT + CMD : CMD fournit les arguments par défaut de ENTRYPOINT
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]
# docker run mon-image             -> python app.py --port 8080
# docker run mon-image --port 9090 -> python app.py --port 9090
```

!!! danger "Piège d'entretien majeur"
    C'est l'une des questions les plus posées. Retenez : `ENTRYPOINT` définit **le programme exécuté**, `CMD` définit **les arguments par défaut** de ce programme (ou la commande complète s'il n'y a pas d'`ENTRYPOINT`). `docker run image <args>` remplace `CMD` mais s'ajoute à `ENTRYPOINT`.

### COPY vs ADD

!!! danger "Piège d'entretien"
    `ADD` peut extraire automatiquement des archives locales (`.tar.gz`) et télécharger des URL distantes — un comportement "magique" source de builds non reproductibles et de risques de sécurité (URL non vérifiée). La bonne pratique quasi unanime : **toujours préférer `COPY`**, et n'utiliser `ADD` que pour le cas précis de l'extraction d'archive locale.

### ARG vs ENV

```dockerfile
ARG VERSION=1.0        # disponible uniquement pendant le build
ENV APP_VERSION=$VERSION   # persiste dans l'image et le conteneur en cours d'exécution
```

```bash
docker build --build-arg VERSION=2.0 -t mon-app .
```

!!! danger "Piège d'entretien : secrets dans ARG"
    Ne jamais passer un secret via `ARG` (ex. `ARG API_KEY`) : sa valeur reste visible dans l'historique de l'image (`docker history`) et dans le cache de build, même si elle n'apparaît pas dans le `ENV` final. Utiliser plutôt `RUN --mount=type=secret` (BuildKit) ou injecter le secret uniquement à l'exécution via `ENV`/volume, jamais au build.

### USER

```dockerfile
RUN groupadd -r app && useradd -r -g app app
USER app
```

Exécuter le conteneur en non-root réduit fortement l'impact d'une éventuelle compromission (voir Partie XII, Sécurité).

### VOLUME

```dockerfile
VOLUME /data
```

Déclare que `/data` doit être un point de montage externe à la couche en écriture du conteneur — Docker y crée automatiquement un volume anonyme si aucun volume/bind mount n'est explicitement fourni au `run`.

### ONBUILD

```dockerfile
# Dans une image de base "builder-python"
ONBUILD COPY . /app
ONBUILD RUN pip install -r /app/requirements.txt
```

Utile pour créer des images de base génériques ("templates") que d'autres équipes étendent via `FROM builder-python`, sans dupliquer la logique de build.

---

## Chapitre 18 : Optimisation

### Multi-stage Build

```dockerfile
# Étape 1 : build (contient compilateurs, outils lourds)
FROM golang:1.22 AS builder
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app

# Étape 2 : image finale (minimale)
FROM scratch
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
```

Seuls les artefacts nécessaires (`--from=builder /app`) sont copiés dans l'image finale : les outils de build (compilateurs, dépendances de dev) ne s'y retrouvent jamais. Résultat : image passant potentiellement de plusieurs centaines de Mo à quelques Mo.

### Réduction de taille

#### Alpine

Image de base minimaliste (~5 Mo) basée sur `musl libc` plutôt que `glibc`. Attention : certaines librairies compilées pour `glibc` peuvent ne pas fonctionner directement sous Alpine (incompatibilité binaire) — un piège classique avec certains paquets Python/Node natifs.

#### Distroless

Images Google (`gcr.io/distroless/*`) qui ne contiennent **que le runtime nécessaire** (ex. juste la libc + le binaire), sans shell, sans gestionnaire de paquets, sans outils système.

!!! danger "Piège d'entretien : distroless et débogage"
    Une image distroless n'a **pas de shell** (`/bin/sh` absent) : `docker exec -it mon-app sh` échoue. C'est un compromis volontaire pour la sécurité (surface d'attaque minimale, rien à exploiter après compromission) — le débogage doit alors passer par des outils externes (sidecar de debug, `kubectl debug` en Kubernetes) ou par les logs/traces uniquement.

### Cache

Voir Chapitre 16 — ordonner les instructions du moins volatile au plus volatile pour maximiser la réutilisation du cache de build.

### Bonnes pratiques

- Toujours épingler une version précise de l'image de base (`FROM python:3.12.3-slim`, pas `FROM python`).
- Fusionner les `RUN` liés logiquement pour limiter le nombre de couches (`RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*`).
- Ne jamais lancer en `root` sans raison (`USER app`).
- Utiliser un `.dockerignore` exhaustif.
- Utiliser `HEALTHCHECK` pour permettre à l'orchestrateur de détecter les instances défaillantes.
- Scanner l'image (Trivy, Docker Scout, Grype) avant publication (voir Partie XII).

??? question "Question d'entretien : Pourquoi une image `scratch` ne peut-elle pas exécuter un binaire compilé dynamiquement ?"
    `scratch` est une image **totalement vide** (0 octet) : pas de libc, pas de `/bin/sh`, rien. Un binaire lié dynamiquement (dynamic linking) a besoin de la libc au runtime pour résoudre ses symboles — absente dans `scratch`, il ne peut pas démarrer. Il faut soit compiler statiquement (`CGO_ENABLED=0` en Go, par exemple), soit utiliser une base minimale contenant la libc (`distroless/base`, `alpine`).

??? question "Question d'entretien : Un multi-stage build améliore-t-il la vitesse de build, ou seulement la taille de l'image finale ?"
    Principalement la **taille finale** et la **sécurité** (moins d'outils = moins de surface d'attaque). Pour la vitesse, l'effet dépend du cache : les stages intermédiaires sont eux-mêmes cachés indépendamment, donc si seul le code source change, l'étape `builder` peut être partiellement invalidée mais le stage final reste rapide à reconstruire.