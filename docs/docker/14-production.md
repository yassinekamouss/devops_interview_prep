# Partie XIV — Docker en production

## Chapitre 32

### Bonnes pratiques

- Images versionnées explicitement (jamais `latest`, voir Partie IV, Chapitre 11).
- Limites de ressources définies sur chaque conteneur (Partie V, Chapitre 15).
- `HEALTHCHECK` défini et exploité par l'orchestrateur.
- Utilisateur non-root (Partie XII).
- Logs envoyés sur stdout/stderr, jamais dans des fichiers internes au conteneur.
- Configuration externalisée (variables d'environnement, secrets), jamais codée en dur dans l'image.
- Registre privé avec scan de vulnérabilités automatisé avant chaque déploiement.

### Monitoring

Le monitoring conteneur combine généralement trois niveaux :

| Niveau | Outils typiques | Ce qui est mesuré |
|---|---|---|
| Hôte | Node Exporter, cAdvisor | CPU/RAM/disque de la machine |
| Conteneur | cAdvisor, `docker stats` | Ressources par conteneur (cgroups) |
| Application | Prometheus client, APM (Datadog, New Relic) | Métriques métier, latence, taux d'erreur |

`cAdvisor` (Container Advisor, Google) est la référence pour exposer les métriques cgroups de chaque conteneur au format Prometheus.

### Logging

En production, les logs ne doivent **jamais** rester uniquement dans `docker logs` (rotation par défaut du daemon si mal configurée = perte de logs anciens). Deux approches :

- **Log driver Docker** : configurer `--log-driver` (json-file avec rotation, `syslog`, `journald`, `awslogs`, `gelf` vers Logstash/Graylog) pour envoyer les logs vers un système centralisé directement depuis le daemon.
- **Sidecar de collecte** : un conteneur agent (Fluentd, Filebeat, Vector) qui lit les logs et les expédie vers un backend (ELK, Loki, Splunk).

### Rotation des logs

```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

!!! danger "Piège d'entretien"
    Sans configuration de rotation (`log-opts`), le driver `json-file` par défaut **n'a aucune limite de taille** — un conteneur bavard peut remplir le disque de l'hôte avec ses seuls logs jusqu'à provoquer une panne complète (y compris du daemon Docker lui-même). C'est une cause réelle et fréquente d'incident de production.

### Haute disponibilité

Docker seul (mode standalone) n'offre **aucune haute disponibilité multi-hôte** native : si l'hôte tombe, tous ses conteneurs tombent avec lui. La HA nécessite un orchestrateur :

- **Docker Swarm** : réplication de services, répartition automatique sur plusieurs nœuds, reprogrammation en cas de panne d'un nœud.
- **Kubernetes** : équivalent plus riche, standard de l'industrie (voir Partie XVI).

### Stratégies de mise à jour

| Stratégie | Principe | Avantage | Inconvénient |
|---|---|---|---|
| Recreate | Arrêt total, puis démarrage de la nouvelle version | Simple | Interruption de service |
| Rolling update | Remplacement progressif instance par instance | Pas d'interruption totale | Coexistence temporaire de deux versions |
| Blue-Green | Bascule d'un environnement complet à un autre en une fois | Rollback instantané | Nécessite le double des ressources pendant la bascule |
| Canary | Déploiement à un petit sous-ensemble du trafic d'abord | Détection précoce des régressions | Complexité de routage supplémentaire |

### Rollback

```bash
# Docker Swarm
docker service update --rollback mon-service

# Compose (approche manuelle : redéployer le tag précédent)
docker compose up -d --no-deps app  # après avoir changé le tag d'image dans le compose.yaml
```

Le rollback doit être **testé avant** d'en avoir besoin en urgence — une image précédente doit rester disponible dans le registre (politique de rétention adaptée), et la base de données doit rester compatible avec les deux versions applicatives pendant la transition (attention aux migrations de schéma destructives).

??? question "Question d'entretien : Comment garantir un déploiement sans interruption (zero-downtime) avec Docker ?"
    Combiner : `HEALTHCHECK` fiable, stratégie rolling update ou blue-green pilotée par un orchestrateur (Swarm/Kubernetes) ou un reverse proxy (Traefik, Nginx) capable de retirer une instance du pool tant qu'elle n'est pas `healthy`, et `depends_on: condition: service_healthy` pour ne router du trafic que vers des instances réellement prêtes.

??? question "Question d'entretien : Que se passe-t-il pour les logs si vous ne configurez pas `log-opts` ?"
    Le driver `json-file` par défaut accumule les logs sans limite de taille ni de rotation automatique — risque de saturation disque sur l'hôte à moyen/long terme. Toujours définir `max-size`/`max-file` explicitement, ou déléguer la rétention à un système de collecte centralisé.