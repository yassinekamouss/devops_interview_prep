# Partie VIII — Volumes

## Chapitre 22 : Persistance

### Pourquoi les données disparaissent

La couche en écriture d'un conteneur (Copy-on-Write, voir Partie II, Chapitre 7) est liée au **cycle de vie du conteneur**. Elle est détruite avec `docker rm`. Toute donnée écrite uniquement dans cette couche est donc perdue à la suppression du conteneur.

### Cycle de vie

| Stockage | Survit à `docker stop`/`start` | Survit à `docker rm` |
|---|---|---|
| Couche en écriture du conteneur | ✅ | ❌ |
| Volume nommé | ✅ | ✅ |
| Bind mount | ✅ | ✅ |
| tmpfs | ✅ (tant que le conteneur tourne) | ❌ (jamais écrit sur disque) |

---

## Chapitre 23 : Types de stockage

### Volumes

Gérés entièrement par Docker, stockés dans `/var/lib/docker/volumes/`. C'est le mécanisme **recommandé** pour la persistance en production.

```bash
docker volume create mes-donnees
docker run -d -v mes-donnees:/var/lib/postgresql/data postgres
```

Avantages : gérés par le CLI/API Docker, portables entre hôtes (via `docker volume` drivers réseau — NFS, cloud), sauvegarde facilitée, pas de dépendance à un chemin hôte précis.

### Bind Mount

Monte un chemin **existant de l'hôte** directement dans le conteneur.

```bash
docker run -d -v /home/user/app:/app mon-app
docker run -d --mount type=bind,source=/home/user/app,target=/app mon-app   # syntaxe explicite recommandée
```

Utile en développement (rechargement à chaud du code source), mais couple le conteneur à la structure de fichiers de l'hôte — moins portable.

### tmpfs

Stocke les données **en mémoire RAM uniquement**, jamais sur disque.

```bash
docker run -d --tmpfs /app/cache:size=100m mon-app
```

Utile pour des données temporaires sensibles (secrets déchiffrés, caches) qui ne doivent jamais persister sur disque.

!!! danger "Piège d'entretien"
    `-v` et `--mount` ne se comportent pas identiquement sur un cas limite : avec `-v`, si le chemin source (bind mount) n'existe pas sur l'hôte, Docker le **crée automatiquement** (souvent par erreur, créant un dossier vide au lieu d'échouer). Avec `--mount`, Docker **échoue explicitement** si la source n'existe pas. `--mount` est la syntaxe recommandée en production pour cette raison, en plus d'être plus lisible.

---

## Chapitre 24 : Gestion

### docker volume

```bash
docker volume create mes-donnees
docker volume ls
docker volume inspect mes-donnees
docker volume rm mes-donnees
docker volume prune          # supprime tous les volumes non utilisés par un conteneur
```

### Backup

```bash
docker run --rm \
  -v mes-donnees:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .
```

Principe : lancer un conteneur temporaire (`--rm`) montant le volume à sauvegarder et un répertoire hôte de sortie, puis archiver.

### Restore

```bash
docker run --rm \
  -v mes-donnees:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

### Migration

Pour migrer un volume vers un autre hôte : `backup` → transfert du `.tar.gz` (scp, S3...) → `restore` sur le nouvel hôte. Pour des volumes réseau (NFS, cloud), utiliser directement un driver de volume compatible (`local-persist`, `rexray`, CSI en Kubernetes) qui pointe vers le même backend de stockage partagé.

??? question "Question d'entretien : Volume ou bind mount pour une base de données en production ?"
    Volume nommé, sans hésitation. Il est géré par Docker (permissions cohérentes, meilleure portabilité, pas de dépendance à un chemin hôte spécifique), généralement plus performant sous Docker Desktop (Mac/Windows), et adapté aux outils de sauvegarde standards (`docker volume`). Le bind mount reste préférable uniquement pour le développement local (édition de code en direct).

??? question "Question d'entretien : Un volume anonyme et un volume nommé, quelle différence pratique ?"
    Un volume anonyme (`-v /data`, sans nom source) reçoit un identifiant généré aléatoirement et est supprimé automatiquement par `docker rm -v` — il est difficile à réutiliser entre conteneurs. Un volume nommé (`-v mes-donnees:/data`) est explicite, réutilisable par plusieurs conteneurs, et **jamais** supprimé automatiquement, même avec `docker rm -v`.