# Partie X — Docker Compose

## Chapitre 26 : Introduction

### Pourquoi Compose

`docker run` devient vite ingérable dès qu'une application comprend plusieurs conteneurs liés (app + base de données + cache). Compose déclare l'ensemble de la stack dans **un seul fichier YAML**, versionnable et reproductible.

### Cas d'utilisation

- Environnements de développement multi-services (app + DB + Redis).
- Tests d'intégration en CI (stack complète jetable).
- Déploiements simples mono-hôte (petites applications, sans besoin de Kubernetes).

### Compose Specification

Depuis 2020, Compose suit la **Compose Specification**, un standard ouvert (plus lié à un éditeur unique) — d'où la disparition de la clé `version:` dans les fichiers récents (`docker compose` ignore la version et applique toujours la dernière spec supportée).

---

## Chapitre 27 : Le fichier compose.yaml

```yaml
services:
  app:
    build: .
    ports:
      - "8080:80"
    environment:
      - DB_HOST=db
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - backend

  db:
    image: postgres:16
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

volumes:
  db-data:

networks:
  backend:
```

### services

Chaque clé sous `services:` définit un conteneur (nom du service = nom réseau DNS interne, comme un `--network` personnalisé sous `docker run`).

### volumes

Déclarés au niveau racine (`volumes:`), référencés par nom dans les services — équivalent à `docker volume create` + `-v nom:/chemin`.

### networks

Par défaut, Compose crée **un réseau bridge dédié** au projet (tous les services s'y connectent automatiquement) — DNS interne disponible nativement, sans configuration manuelle.

### depends_on

```yaml
depends_on:
  db:
    condition: service_healthy
```

!!! danger "Piège d'entretien classique"
    `depends_on` sans `condition` garantit uniquement l'**ordre de démarrage** des conteneurs, pas que le service dépendant soit réellement prêt à recevoir des requêtes (ex. Postgres démarré mais pas encore accepteur de connexions). Toujours combiner avec `condition: service_healthy` et un `healthcheck` défini sur le service dont on dépend, pour une vraie garantie de disponibilité.

### restart

Mêmes valeurs que `docker run --restart` (Partie V, Chapitre 15) : `no`, `always`, `on-failure`, `unless-stopped`.

### healthcheck

Même sémantique qu'en Dockerfile (Partie V, Chapitre 15), défini ici au niveau du service.

### build

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
      args:
        - VERSION=1.0
```

### image

```yaml
services:
  db:
    image: postgres:16
```

Si `build:` et `image:` sont tous deux présents, Compose construit l'image et l'étiquette avec le nom indiqué dans `image:`.

### environment

```yaml
environment:
  - DB_HOST=db
  - DB_PASSWORD=${DB_PASSWORD}   # substitution depuis .env ou variable shell
```

---

## Chapitre 28 : Commandes Compose

| Commande | Rôle |
|---|---|
| `docker compose up` | Crée et démarre tous les services (`-d` pour arrière-plan) |
| `docker compose down` | Arrête et supprime conteneurs + réseaux (garde les volumes sauf `-v`) |
| `docker compose stop` | Arrête les conteneurs sans les supprimer |
| `docker compose start` | Redémarre des conteneurs arrêtés |
| `docker compose restart` | Redémarre les services |
| `docker compose logs` | Logs agrégés de tous les services (`-f` pour suivre en direct) |
| `docker compose exec` | Exécute une commande dans un service en cours d'exécution |
| `docker compose build` | (Re)construit les images définies avec `build:` |
| `docker compose pull` | Tire les images définies avec `image:` |
| `docker compose ps` | Liste les conteneurs du projet Compose courant |

```bash
docker compose up -d
docker compose logs -f app
docker compose exec app bash
docker compose down -v      # supprime aussi les volumes nommés
```

!!! danger "Piège d'entretien"
    `docker compose down` **ne supprime pas** les volumes nommés par défaut — comportement volontaire pour ne pas perdre de données par erreur. Il faut explicitement `-v` pour les supprimer. Beaucoup de candidats pensent, à tort, que `down` fait un nettoyage complet par défaut.

??? question "Question d'entretien : Compose est-il adapté à un cluster multi-hôtes en production ?"
    Non — Compose (dans son usage `docker compose up`) cible un déploiement **mono-hôte**. Pour du multi-hôte, il faut Docker Swarm (`docker stack deploy`, qui réutilise en partie la syntaxe Compose) ou, en pratique quasi systématique aujourd'hui, Kubernetes (voir Partie XVI). Docker Compose reste néanmoins un excellent outil de développement local et de CI, même dans un environnement de production Kubernetes.

??? question "Question d'entretien : Comment forcer la reconstruction d'une image sans cache dans Compose ?"
    `docker compose build --no-cache`, suivi de `docker compose up -d --force-recreate` si vous voulez également forcer le remplacement des conteneurs existants (même si la configuration n'a pas changé du point de vue de Compose).