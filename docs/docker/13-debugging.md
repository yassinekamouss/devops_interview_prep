# Partie XIII — Débogage

## Chapitre 31

### Logs

```bash
docker logs mon-app
docker logs -f mon-app              # suivi en temps réel
docker logs --since 10m mon-app     # dernières 10 minutes
docker logs --tail 100 mon-app      # 100 dernières lignes
```

Docker capture uniquement **stdout/stderr** du processus PID 1. Une application qui écrit ses logs dans un fichier interne au conteneur (`/var/log/app.log`) n'apparaîtra **pas** dans `docker logs` — reconfigurer l'app pour logger sur stdout, ou monter un volume et tailer le fichier séparément.

### docker inspect

```bash
docker inspect mon-app
docker inspect --format='{{.State.Status}}' mon-app
docker inspect --format='{{json .NetworkSettings.Networks}}' mon-app | jq
```

Première commande à lancer face à un comportement inattendu : état, code de sortie, montages, config réseau, variables d'environnement effectives — tout y est.

### docker events

```bash
docker events
docker events --filter 'container=mon-app'
docker events --filter 'event=die'
```

Flux temps réel des événements du daemon (création, démarrage, arrêt, OOM kill...) — utile pour corréler un crash avec une action externe (déploiement, `docker prune`, etc.) au moment précis où il survient.

### docker stats

```bash
docker stats
docker stats --no-stream mon-app     # une seule mesure, sans rafraîchissement continu
```

Vue temps réel CPU/RAM/réseau/I/O — premier réflexe pour diagnostiquer une consommation anormale ou confirmer un `OOMKilled` imminent.

### docker top

```bash
docker top mon-app
```

Liste les processus internes du conteneur, vus depuis l'hôte (PID hôte réels) — utile pour repérer un processus zombie ou un fork excessif.

### docker diff

Voir Partie V, Chapitre 14 — liste les fichiers modifiés depuis le démarrage, utile pour auditer une écriture inattendue en dehors des volumes attendus.

### docker system df

```bash
docker system df
docker system df -v      # détail par image/conteneur/volume
```

Affiche l'espace disque utilisé par images, conteneurs, volumes et cache de build — premier réflexe face à un disque hôte saturé.

### docker system prune

```bash
docker system prune                 # conteneurs arrêtés + réseaux inutilisés + images dangling + cache de build
docker system prune -a              # + toutes les images non utilisées par un conteneur actif
docker system prune -a --volumes    # + tous les volumes non utilisés (destructif, à utiliser avec prudence)
```

!!! danger "Piège d'entretien"
    `docker system prune -a --volumes` est **irréversible** et supprime toute donnée non explicitement rattachée à un conteneur en cours d'exécution. Ne jamais l'exécuter sur un hôte de production sans vérification préalable des volumes concernés (`docker volume ls` + `docker inspect` de chaque service actif).

### Méthodologie de débogage type

| Symptôme | Première commande |
|---|---|
| Conteneur ne démarre pas | `docker logs`, puis `docker inspect --format='{{.State.Error}}'` |
| Conteneur redémarre en boucle | `docker inspect --format='{{.State.ExitCode}}'`, `docker logs --tail 50` |
| Conteneur lent / consomme trop | `docker stats`, `docker top` |
| Conteneur tué de façon inattendue | `docker inspect --format='{{.State.OOMKilled}}'`, `docker events --filter event=oom` |
| Impossible de joindre un autre service | `docker network inspect`, test DNS interne (`docker exec ... nslookup`) |
| Disque hôte saturé | `docker system df -v` |

??? question "Question d'entretien : Un conteneur redémarre en boucle (`CrashLoop`). Démarche de diagnostic ?"
    1) `docker logs mon-app --tail 50` pour voir l'erreur applicative avant le crash. 2) `docker inspect --format='{{.State.ExitCode}}' mon-app` — un code 137 suggère un SIGKILL (souvent OOM), un code 1 une erreur applicative gérée. 3) Vérifier `OOMKilled` dans `docker inspect`. 4) Vérifier la `restart policy` en cours (`on-failure` peut masquer un vrai problème en relançant indéfiniment). 5) Si l'app dépend d'un autre service (DB), vérifier que le `healthcheck`/`depends_on` est correctement configuré (voir Partie X).

??? question "Question d'entretien : Pourquoi `docker logs` peut-il être vide alors que l'application écrit visiblement des logs ?"
    Parce que l'application écrit dans un fichier à l'intérieur du conteneur plutôt que sur stdout/stderr. Docker ne capture que ces deux flux du processus PID 1. Solution : reconfigurer le logger applicatif vers stdout (bonne pratique "12-factor app"), ou monter le fichier de log via un volume et l'inspecter directement.