# Partie XVII — Questions d'entretien Oracle

!!! info "Comment utiliser cette banque"
    🟢 Basique · 🟡 Intermédiaire · 🔴 Avancé/piège. Répondez à voix haute avant de lire la réponse — c'est la meilleure préparation pour un entretien oral.

## Questions pièges

1. 🟢 **Docker et une VM, quelle est la différence fondamentale ?**
   Une VM virtualise le matériel et embarque un noyau complet par instance ; un conteneur partage le noyau de l'hôte et isole seulement les processus via namespaces/cgroups (Partie I, Ch.2-3).

2. 🟡 **`docker stop` vs `docker kill` ?**
   `stop` envoie SIGTERM puis attend un délai de grâce avant SIGKILL ; `kill` envoie directement SIGKILL (ou un signal custom), sans délai (Partie V, Ch.13).

3. 🔴 **`CMD` vs `ENTRYPOINT` — donnez un exemple où les deux combinés changent le comportement.**
   `ENTRYPOINT ["python","app.py"]` + `CMD ["--port","8080"]` : `docker run image` exécute `python app.py --port 8080` ; `docker run image --port 9090` exécute `python app.py --port 9090` (CMD est remplacé, pas ENTRYPOINT) (Partie VI, Ch.17).

4. 🔴 **Pourquoi `latest` est dangereux en production ?**
   Ce n'est pas garanti d'être la version la plus récente sémantiquement, le digest pointé peut changer entre deux pulls, et il casse la reproductibilité des déploiements (Partie IV, Ch.11).

5. 🟡 **`docker save` vs `docker export` ?**
   `save` opère sur une image et conserve les layers/historique ; `export` opère sur un conteneur et aplatit son filesystem en une seule couche (Partie IV, Ch.12).

6. 🔴 **Un conteneur A peut-il joindre un service du conteneur B via `localhost` ?**
   Non, sauf s'ils sont dans le même pod Kubernetes (network namespace partagé). En Docker standalone, chaque conteneur a son propre `localhost` — il faut passer par le nom du conteneur sur un réseau Docker personnalisé (Partie VII, Ch.21).

7. 🟡 **`EXPOSE` dans un Dockerfile ouvre-t-il un port ?**
   Non, c'est purement documentaire. Seul `-p`/`-P` au `docker run` publie réellement un port (Partie VII, Ch.21).

8. 🟢 **Que devient la couche en écriture d'un conteneur supprimé ?**
   Elle est détruite avec le conteneur — toute donnée non persistée via volume/bind mount est perdue (Partie VIII, Ch.22).

9. 🟡 **`docker compose down` supprime-t-il les volumes ?**
   Non, par défaut. Il faut `docker compose down -v` explicitement (Partie X, Ch.28).

10. 🔴 **Que fait `--privileged` et pourquoi est-ce risqué ?**
    Désactive quasiment toutes les restrictions de sécurité (capabilities, accès devices, seccomp/AppArmor) — quasi équivalent à un accès root complet à l'hôte (Partie XII, Ch.30).

11. 🟡 **Le groupe `docker` donne-t-il un accès root implicite ?**
    Oui — un utilisateur du groupe `docker` peut monter `/` de l'hôte dans un conteneur et y obtenir un accès complet (Partie III, Ch.9).

12. 🔴 **Pourquoi éviter `ARG` pour un secret de build ?**
    Sa valeur reste visible dans `docker history` et le cache de build, même retirée d'une couche ultérieure (Partie IX, Ch.25).

## Questions de conception

13. 🟡 **Comment structurer un Dockerfile pour maximiser le cache de build ?**
    Placer en premier ce qui change le moins souvent (dépendances), copier le code source en dernier (Partie VI, Ch.16).

14. 🔴 **Concevez un Dockerfile multi-stage pour une app Go compilée statiquement.**
    Stage `builder` avec `golang` complet pour compiler (`CGO_ENABLED=0 go build`), stage final `FROM scratch` ne copiant que le binaire — image finale de quelques Mo (Partie VI, Ch.18).

15. 🟡 **Comment organiser les réseaux Docker pour une stack app + DB + cache ?**
    Réseau `frontend` (app exposée) et réseau `backend` isolé (DB, cache) ; l'app est connectée aux deux, la DB/cache uniquement à `backend` (Partie VII, Ch.20).

16. 🔴 **Concevez la stratégie de healthcheck d'une stack Compose avec dépendance stricte app → DB.**
    `healthcheck` sur le service DB (`pg_isready`), `depends_on: db: condition: service_healthy` sur l'app — l'app ne démarre que quand la DB répond réellement (Partie X, Ch.27).

17. 🟡 **Comment gérer des configurations différentes dev/staging/prod avec Compose ?**
    Fichier de base `compose.yaml` + fichiers d'override (`compose.override.yaml`, `compose.prod.yaml`) fusionnés via `-f`, ou variables `.env` distinctes par environnement.

18. 🔴 **Concevez le pipeline d'image pour garantir zéro secret dans l'image finale.**
    `RUN --mount=type=secret` (BuildKit) pour tout accès à un secret pendant le build, jamais `ARG`/`ENV` ; scan (Trivy/Docker Scout) avant push ; injection des secrets d'exécution via un gestionnaire externe, jamais dans l'image (Partie IX, Ch.25 + Partie XII, Ch.30).

19. 🟡 **Comment limiter la surface d'attaque d'une image de production ?**
    Base minimale (distroless/alpine), `USER` non-root, `--cap-drop=ALL` + capabilities minimales, scan systématique, pas de shell si possible (Partie XII, Ch.30).

20. 🔴 **Concevez une stratégie de logs pour 50 conteneurs sur 5 hôtes.**
    Log driver centralisé (`gelf`/`fluentd`) ou sidecar de collecte (Fluent Bit) sur chaque hôte, agrégation vers un backend commun (ELK/Loki), rotation configurée sur le driver local en secours (Partie XIV, Ch.32).

## Questions de production

21. 🟢 **Un conteneur affiche `OOMKilled: true`. Que faites-vous ?**
    Vérifier `docker stats`/métriques historiques pour distinguer fuite mémoire réelle vs limite `--memory` trop basse pour un pic légitime, avant d'ajuster (Partie V, Ch.15).

22. 🟡 **Comment déployer sans interruption de service (zero-downtime) ?**
    Healthcheck fiable + rolling update ou blue-green pilotés par un orchestrateur/reverse proxy qui ne route qu'aux instances `healthy` (Partie XIV, Ch.32).

23. 🔴 **Le disque de l'hôte de production est saturé à 100% par Docker. Démarche ?**
    `docker system df -v` pour identifier la source (images, conteneurs, volumes, cache de build), puis `docker system prune` ciblé — jamais `-a --volumes` sans vérification préalable des volumes actifs (Partie XIII, Ch.31).

24. 🟡 **Pourquoi configurer `log-opts` (`max-size`, `max-file`) systématiquement ?**
    Sans limite, le driver `json-file` par défaut peut saturer le disque hôte avec les seuls logs applicatifs (Partie XIV, Ch.32).

25. 🔴 **Comment auditer la conformité sécurité d'un hôte Docker de production ?**
    Exécuter `docker/docker-bench-security` (CIS Docker Benchmark), scanner les images (Trivy), vérifier rootless/capabilities/SELinux-AppArmor actifs (Partie XII, Ch.30).

26. 🟡 **Comment sauvegarder les données d'un volume Docker en production ?**
    Conteneur temporaire montant le volume + un répertoire hôte, archivage avec `tar` (Partie VIII, Ch.24).

27. 🔴 **Un rollback est nécessaire suite à un déploiement défaillant. Prérequis pour que ce soit sûr ?**
    Image précédente disponible dans le registre (politique de rétention adaptée), compatibilité DB entre les deux versions applicatives (attention aux migrations destructives) (Partie XIV, Ch.32).

## Questions d'architecture

28. 🟡 **Pourquoi Kubernetes plutôt que Docker Compose pour une application à fort trafic ?**
    Compose est mono-hôte ; Kubernetes apporte scaling multi-nœuds, rescheduling automatique en cas de panne, et autoscaling basé métriques (Partie XVI, Ch.34).

29. 🔴 **Pod vs conteneur : quelle est l'unité de déploiement Kubernetes et pourquoi cette distinction existe-t-elle ?**
    Le pod, pas le conteneur — il permet le pattern sidecar (conteneurs partageant réseau/volumes, ex. proxy ou agent de logs à côté de l'app principale) (Partie XVI, Ch.34).

30. 🟡 **Docker a-t-il encore un rôle dans un environnement 100% Kubernetes ?**
    Oui pour le **build** (format d'image OCI produit par `docker build`) même si le runtime d'exécution du cluster n'est plus `dockerd` mais containerd/CRI-O (Partie XVI, Ch.34).

31. 🔴 **Concevez l'architecture réseau d'une stack microservices avec base de données isolée.**
    Réseau `edge` (reverse proxy exposé publiquement), réseau `services` (microservices, communication interne par nom DNS), réseau `data` isolé (DB, non exposé), chaque service ne rejoignant que les réseaux dont il a besoin (Partie VII, Ch.20).

32. 🟡 **Quelle est la différence architecturale entre `bridge` et `overlay` ?**
    `bridge` connecte des conteneurs sur un **même hôte** ; `overlay` connecte des conteneurs sur **des hôtes différents** via encapsulation VXLAN (Partie VII, Ch.19).

33. 🔴 **Comment intégrer OCIR et OKE de façon sécurisée dans une architecture Oracle Cloud ?**
    Policies IAM scopées par compartiment/tenancy permettant à OKE de pull depuis OCIR sans `imagePullSecrets` manuel, auth token dédié (jamais le mot de passe du compte) pour les pushs CI (Partie XI, Ch.29 + Partie XV, Ch.33).

## Exercices de raisonnement

34. 🔴 **Un `docker build` fonctionne en local mais échoue en CI avec "no space left on device". Diagnostic ?**
    Cache de build accumulé sur le runner CI (`docker system df -v`), souvent des runners éphémères mal nettoyés entre jobs ou un build context trop large (`.dockerignore` manquant) — vérifier les deux (Partie VI, Ch.16 + Partie XIII, Ch.31).

35. 🔴 **Deux conteneurs sur le même réseau Docker personnalisé ne se joignent pas par nom. Trois causes possibles ?**
    (1) réseau `bridge` par défaut sans DNS interne au lieu d'un réseau personnalisé ; (2) l'appli écoute sur `127.0.0.1` au lieu de `0.0.0.0` dans le conteneur cible ; (3) règle de pare-feu applicative bloquant le trafic inter-conteneurs (Partie VII, Ch.21).

36. 🔴 **Une image de 2 Go doit être réduite. Ordre de priorité des optimisations ?**
    1) Multi-stage build (retirer les outils de build) ; 2) base plus légère (alpine/distroless) ; 3) fusion des `RUN` + nettoyage cache paquets dans la même couche ; 4) `.dockerignore` strict (Partie VI, Ch.18).

37. 🔴 **Un conteneur `healthy` selon Docker mais l'application ne répond pas aux vraies requêtes utilisateurs. Explication possible ?**
    Le `HEALTHCHECK` teste probablement un endpoint trop superficiel (ex. `/ping` statique) qui ne reflète pas l'état réel des dépendances critiques (DB, cache) — le healthcheck doit vérifier la capacité fonctionnelle réelle, pas juste que le process répond (Partie V, Ch.15).

38. 🔴 **Un déploiement rolling update Kubernetes bascule tout le trafic vers la nouvelle version avant qu'elle soit prête. Cause probable ?**
    Absence de `readinessProbe` correctement configurée — sans elle, Kubernetes considère un pod prêt dès qu'il démarre, pas quand il peut réellement traiter des requêtes (Partie XVI, Ch.34).

## Débogage de scénarios réels

39. 🔴 **Scénario : un service en production redémarre en boucle toutes les 30 secondes depuis un déploiement récent.**
    Démarche : `docker logs --tail 50` pour l'erreur applicative → `docker inspect --format='{{.State.ExitCode}}'` (137 = probable SIGKILL/OOM, 1 = erreur applicative gérée) → vérifier `OOMKilled` → vérifier si une dépendance (DB) n'est pas prête (`depends_on`/healthcheck) → comparer avec la configuration du déploiement précédent qui fonctionnait (Partie XIII, Ch.31).

40. 🔴 **Scénario : après un `docker system prune -a --volumes` accidentel en production, un service ne redémarre plus.**
    Le volume nommé contenant les données a été supprimé (aucun conteneur ne l'utilisait au moment du prune). Restauration depuis la dernière sauvegarde (Partie VIII, Ch.24) — leçon : ne jamais exécuter cette commande en production sans audit préalable des volumes actifs (Partie XIII, Ch.31).

41. 🔴 **Scénario : les logs d'une application semblent vides dans `docker logs` alors que l'app tourne visiblement.**
    L'application écrit probablement dans un fichier interne plutôt que sur stdout/stderr — seul flux capturé par `docker logs`. Reconfigurer le logger vers stdout ou monter/inspecter le fichier via volume (Partie XIII, Ch.31).

42. 🔴 **Scénario : un pipeline CI Docker-in-Docker échoue par intermittence sur un runner partagé.**
    `dind` nécessite `--privileged`, source d'instabilité et de conflits sur des runners mutualisés. Envisager le mode "Docker-outside-of-Docker" (montage du socket hôte) en évaluant le compromis de sécurité associé, ou un runner dédié isolé par job (Partie XV, Ch.33).

43. 🔴 **Scénario : une image passe les tests en local mais un scan de sécurité CI bloque le déploiement.**
    Le scan (Trivy/Docker Scout) a détecté une CVE dans l'image de base ou une dépendance — vérifier le rapport, mettre à jour la version de base/dépendance concernée, ou documenter une exception temporaire si le risque est accepté et tracé (Partie XII, Ch.30).