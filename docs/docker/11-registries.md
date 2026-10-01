# Partie XI — Registres Docker

## Chapitre 29

### Docker Hub

Registre public par défaut. Limites à connaître : quota de pull anonyme (rate limiting par IP), retention automatique des images inactives sur les comptes gratuits.

### Registry privé

Un registre auto-hébergé (image officielle `registry:2`, ou solutions complètes type Harbor) donne le contrôle total : rétention, scan de vulnérabilités intégré, réplication, RBAC interne.

```bash
docker run -d -p 5000:5000 --name registry registry:2
docker tag mon-app:1.0 localhost:5000/mon-app:1.0
docker push localhost:5000/mon-app:1.0
```

### Oracle Container Registry

Service managé d'Oracle Cloud Infrastructure (OCIR). Format d'URL type `<région>.ocir.io/<namespace>/<repo>:<tag>`. Intégré nativement à IAM d'OCI pour les permissions (policies), et à OKE (Oracle Kubernetes Engine) pour le pull d'images sans configuration réseau supplémentaire au sein de la même tenancy.

```bash
docker login <région>.ocir.io -u '<namespace>/<utilisateur>' -p '<auth-token>'
docker tag mon-app:1.0 <région>.ocir.io/<namespace>/mon-app:1.0
docker push <région>.ocir.io/<namespace>/mon-app:1.0
```

!!! danger "Piège d'entretien Oracle"
    L'authentification OCIR n'utilise **pas** le mot de passe du compte OCI mais un **auth token** généré séparément depuis la console IAM. Le confondre est une erreur fréquente en entretien technique Oracle — sachez le mentionner explicitement.

### GitHub Container Registry

`ghcr.io`, intégré nativement aux GitHub Actions (authentification via `GITHUB_TOKEN`, sans credentials séparés à gérer en CI).

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker push ghcr.io/USERNAME/mon-app:1.0
```

### Authentification

#### Login

```bash
docker login                          # Docker Hub
docker login registry.exemple.com     # registre privé
```

Les credentials sont stockés (en clair par défaut, ou via un credential helper OS — `pass`, Keychain, Windows Credential Manager) dans `~/.docker/config.json`.

!!! danger "Piège d'entretien sécurité"
    Sans credential helper configuré, `docker login` stocke le token **en base64 (non chiffré)** dans `~/.docker/config.json`. En CI/CD, ne jamais faire de `docker login` avec un mot de passe en clair dans les logs — utiliser des secrets CI et `--password-stdin` pour éviter que le mot de passe apparaisse dans l'historique shell ou les process listings.

#### Push

Nécessite que l'image soit taguée avec le nom d'hôte du registre cible (`docker tag`) avant `docker push` — sinon Docker suppose Docker Hub par défaut.

#### Pull

```bash
docker pull registry.exemple.com/mon-app:1.0
```

??? question "Question d'entretien : Comment sécuriser l'accès à un registre privé dans un pipeline CI/CD ?"
    Utiliser des secrets CI dédiés (jamais en clair dans le YAML de pipeline), un compte de service à privilèges minimaux (accès push/pull scoped à un seul repository si possible), une rotation régulière des tokens/auth tokens, et `--password-stdin` plutôt que `--password` pour éviter l'exposition en ligne de commande.