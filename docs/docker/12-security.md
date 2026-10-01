# Partie XII — Sécurité Docker

## Chapitre 30

### Least Privilege

Principe directeur de toute la sécurité conteneur : chaque conteneur ne doit avoir accès qu'aux ressources strictement nécessaires à son fonctionnement — pas de root inutile, pas de capabilities superflues, pas de montage de socket Docker sauf nécessité absolue.

### Rootless Docker

Le daemon lui-même tourne comme utilisateur **non-root** sur l'hôte, via user namespaces (Partie II, Chapitre 5) : le "root" à l'intérieur d'un conteneur est mappé vers un UID non privilégié côté hôte.

```bash
dockerd-rootless-setuptool.sh install
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
```

!!! danger "Piège d'entretien"
    Rootless Docker limite certaines fonctionnalités : pas d'accès direct à certains ports privilégiés (<1024) sans configuration additionnelle, pas de support natif de certains drivers réseau (`macvlan`), performances I/O parfois réduites (via `fuse-overlayfs` au lieu de `overlay2` natif selon la config noyau). Ce n'est pas une solution universelle, c'est un compromis sécurité/fonctionnalité à évaluer selon le contexte.

### Capabilities

Le noyau Linux découpe les privilèges root en unités granulaires (capabilities). Docker retire déjà la plupart par défaut, mais on peut restreindre davantage :

```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE mon-app
```

`--cap-drop=ALL` retire tout, puis `--cap-add` ne réautorise que le strict nécessaire (ici, la capacité de bind sur un port <1024 sans être root).

### Seccomp

Filtre les **appels système (syscalls)** qu'un conteneur peut effectuer. Docker applique un profil par défaut bloquant ~44 syscalls dangereux (ex. `reboot`, `mount`). Un profil personnalisé peut restreindre davantage selon l'application.

```bash
docker run --security-opt seccomp=profil-custom.json mon-app
```

### AppArmor

Système de contrôle d'accès mandatoire (MAC) actif par défaut sur Ubuntu/Debian. Docker applique un profil par défaut restreignant l'accès aux fichiers, réseau, capabilities pour chaque conteneur.

### SELinux

Équivalent d'AppArmor, utilisé par défaut sur RHEL/CentOS/Fedora. Applique des labels de sécurité (contextes) à chaque processus et fichier — un conteneur ne peut accéder qu'aux ressources labellisées pour lui.

!!! danger "Piège d'entretien"
    Ne jamais désactiver SELinux/AppArmor "pour que ça marche" (`--security-opt apparmor=unconfined` ou `setenforce 0`) sans comprendre la cause du blocage — c'est un contournement de sécurité, pas une correction. Diagnostiquer d'abord via les logs (`journalctl`, `audit.log`) l'appel exact refusé.

### Secrets

Voir Partie IX, Chapitre 25 — jamais dans `ENV`/`ARG`, toujours via Compose `secrets:`, BuildKit `--mount=type=secret`, ou un gestionnaire externe (Vault, Oracle Vault, AWS Secrets Manager).

### Scan des images

```bash
docker scout cves mon-app:1.0
trivy image mon-app:1.0
```

Scanner systématiquement les images avant publication (CI/CD) pour détecter les CVE connues dans l'image de base et les dépendances installées.

### Docker Bench

Script officiel (`docker/docker-bench-security`) qui audite la configuration du daemon et des conteneurs par rapport au **CIS Docker Benchmark** (référentiel de bonnes pratiques de sécurité reconnu par l'industrie).

```bash
docker run --net host --pid host --cap-add audit_control \
  -v /var/lib:/var/lib -v /var/run/docker.sock:/var/run/docker.sock \
  docker/docker-bench-security
```

### Image Signing

Signature cryptographique des images pour garantir leur intégrité et leur provenance, via **Docker Content Trust** (Notary) ou **Sigstore/Cosign** (standard émergent, indépendant d'un registre).

```bash
export DOCKER_CONTENT_TRUST=1
docker push mon-app:1.0    # signe automatiquement si DCT activé
```

### SBOM

Le Software Bill of Materials liste **tous les composants** (paquets, librairies, versions) présents dans une image — essentiel pour tracer rapidement l'exposition à une CVE nouvellement découverte.

```bash
docker sbom mon-app:1.0
```

??? question "Question d'entretien : Un conteneur root peut-il compromettre l'hôte ?"
    Oui, potentiellement — sans user namespace remapping, root dans le conteneur correspond à UID 0 sur l'hôte. Combiné à une mauvaise configuration (`--privileged`, socket Docker monté, capability dangereuse comme `SYS_ADMIN`), un attaquant root dans le conteneur peut s'évader vers l'hôte. D'où l'importance cumulée de : `USER` non-root dans le Dockerfile, `--cap-drop=ALL`, rootless Docker, et ne jamais utiliser `--privileged` sauf nécessité technique absolue et isolée.

??? question "Question d'entretien : Que fait le flag `--privileged` et pourquoi est-il dangereux ?"
    Il désactive **toutes** les restrictions de sécurité (capabilities complètes, accès à tous les devices de l'hôte, désactivation de seccomp/AppArmor). C'est quasiment équivalent à donner un accès root complet à l'hôte depuis le conteneur. Réservé à des cas très spécifiques (Docker-in-Docker, accès matériel bas niveau) — jamais par défaut, jamais sur une image non maîtrisée.