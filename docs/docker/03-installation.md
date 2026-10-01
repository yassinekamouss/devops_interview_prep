# Partie III — Installation

## Chapitre 8 : Installation Docker

### Linux

Docker s'installe nativement sur Linux via le dépôt officiel (à privilégier sur les paquets distro, souvent obsolètes).

#### Ubuntu

```bash
# Prérequis
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# Ajout de la clé GPG officielle
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Ajout du dépôt
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Debian

Procédure quasi identique à Ubuntu, en pointant vers `https://download.docker.com/linux/debian`. Attention à la variable `VERSION_CODENAME` qui doit correspondre à une version supportée (bookworm, bullseye...).

#### CentOS

```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

!!! danger "Piège d'entretien"
    Ne confondez pas le paquet historique `docker.io` (souvent disponible via `apt install docker.io`) avec `docker-ce` (Community Edition, dépôt officiel). `docker.io` est maintenu par la distribution et souvent **en retard** de plusieurs versions.

### Windows

#### WSL2

Docker Desktop sous Windows utilise **WSL2 (Windows Subsystem for Linux v2)** comme backend : un vrai noyau Linux tourne dans une VM légère gérée par Hyper-V, et le daemon Docker s'exécute dedans. C'est ce qui permet des performances proches du natif Linux, contrairement à l'ancien backend Hyper-V pur.

Prérequis :
```powershell
wsl --install
wsl --set-default-version 2
```

#### Docker Desktop

Docker Desktop embarque : le daemon (dans la VM WSL2/Hyper-V), le CLI, une UI graphique, Kubernetes optionnel en un clic, et l'intégration avec l'explorateur de fichiers Windows.

!!! note
    Depuis 2021, **Docker Desktop est payant** pour les entreprises de plus de 250 employés ou plus de 10M$ de revenus (licence Docker Subscription Service Agreement). En entretien, c'est un point que les recruteurs orientés architecture/coûts peuvent creuser.

### Vérification

```bash
docker --version
docker info
docker run hello-world
```

`docker run hello-world` est le test de référence : il vérifie que le client peut contacter le daemon, tirer une image, créer un conteneur et l'exécuter.

---

## Chapitre 9 : Configuration

### Docker Service

Sous Linux, Docker fonctionne comme un service système géré par **systemd**.

#### systemctl

```bash
sudo systemctl start docker      # démarrer
sudo systemctl stop docker       # arrêter
sudo systemctl restart docker    # redémarrer
sudo systemctl enable docker     # démarrage automatique au boot
sudo systemctl status docker     # état du service
```

Les logs du daemon sont consultables via :
```bash
sudo journalctl -u docker.service -f
```

### docker group

Par défaut, seul `root` (ou un membre du groupe `docker`) peut communiquer avec le socket Unix `/var/run/docker.sock`. Pour utiliser Docker sans `sudo` :

```bash
sudo usermod -aG docker $USER
newgrp docker   # ou se déconnecter/reconnecter
```

!!! danger "Piège d'entretien : le groupe docker = root implicite"
    Appartenir au groupe `docker` est **équivalent à avoir un accès root** sur la machine hôte. En effet, un conteneur peut être lancé avec `-v /:/host` et donner un accès complet au filesystem hôte. C'est une question de sécurité classique en entretien Oracle : ne jamais ajouter un utilisateur non fiable au groupe `docker` sans comprendre cette implication (voir Partie XII, Sécurité — Rootless Docker).

### Root vs non-root

| Mode | Description | Sécurité |
|---|---|---|
| Rootless | Le daemon tourne comme utilisateur non-root, via user namespaces | ✅ Recommandé en environnement sensible |
| Standard (root) | Le daemon `dockerd` tourne en root (par défaut) | ⚠️ Surface d'attaque plus large |

### docker info

Affiche l'état complet du daemon : nombre de conteneurs (running/paused/stopped), nombre d'images, driver de stockage utilisé (`overlay2`), driver de logging, cgroup driver (`systemd` ou `cgroupfs`), version du noyau, ressources totales (CPU/RAM), et configuration du registre.

```bash
docker info
```

### docker version

Affiche séparément la version du **Client** et celle du **Server (Engine)** — utile pour diagnostiquer une incompatibilité API (ex. client trop récent pour un vieux serveur, ou inversement).

```bash
docker version
```

??? question "Question d'entretien : Vous lancez `docker ps` et obtenez `permission denied` sur le socket. Que faites-vous ?"
    Deux causes possibles : (1) l'utilisateur n'est pas dans le groupe `docker` → l'ajouter avec `usermod -aG docker $USER` puis se reconnecter ; (2) le daemon n'est pas démarré → vérifier avec `systemctl status docker`. Il ne faut **pas** systématiquement recommander `sudo` en production : c'est un contournement, pas une solution, et cela masque potentiellement un problème de configuration RBAC plus large.

??? question "Question d'entretien : Quelle est la différence entre `overlay2` et les anciens drivers (`aufs`, `devicemapper`) ?"
    `overlay2` est le driver de stockage recommandé depuis le noyau Linux 4.0+ : plus performant, mieux supporté nativement par le noyau, et plus stable. `aufs` n'est pas dans le noyau mainline (patch externe), `devicemapper` en mode loopback n'est pas recommandé en production (performances I/O dégradées). En entretien, mentionner `overlay2` comme réponse par défaut est presque toujours correct pour un hôte Linux moderne.