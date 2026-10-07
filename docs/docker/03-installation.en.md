# Part III — Installation

## Chapter 8: Docker Installation

### Linux

Docker installs natively on Linux via the official repository (preferred over distro packages, often outdated).

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

Procedure almost identical to Ubuntu, pointing to `https://download.docker.com/linux/debian`. Watch the `VERSION_CODENAME` variable which must match a supported version (bookworm, bullseye...).

#### CentOS

```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

!!! danger "Interview Trap"
    Do not confuse the historic package `docker.io` (often available via `apt install docker.io`) with `docker-ce` (Community Edition, official repository). `docker.io` is maintained by the distribution and often **several versions behind**.

### Windows

#### WSL2

Docker Desktop on Windows uses **WSL2 (Windows Subsystem for Linux v2)** as backend: a real Linux kernel runs inside a lightweight VM managed by Hyper-V, and the Docker daemon runs inside it. This enables near-native Linux performance, unlike the old pure Hyper-V backend.

Prerequisites:
```powershell
wsl --install
wsl --set-default-version 2
```

#### Docker Desktop

Docker Desktop includes: the daemon (inside the WSL2/Hyper-V VM), the CLI, a graphical UI, optional one-click Kubernetes, and integration with Windows File Explorer.

!!! note
    Since 2021, **Docker Desktop is paid** for companies with more than 250 employees or more than $10M in revenue (Docker Subscription Service Agreement license). In an interview, this is a point that architecture/cost-oriented recruiters may dig into.

### Verification

```bash
docker --version
docker info
docker run hello-world
```

`docker run hello-world` is the reference test: it verifies that the client can contact the daemon, pull an image, create a container and run it.

---

## Chapter 9: Configuration

### Docker Service

On Linux, Docker runs as a system service managed by **systemd**.

#### systemctl

```bash
sudo systemctl start docker      # démarrer
sudo systemctl stop docker       # arrêter
sudo systemctl restart docker    # redémarrer
sudo systemctl enable docker     # démarrage automatique au boot
sudo systemctl status docker     # état du service
```

Daemon logs can be viewed via:
```bash
sudo journalctl -u docker.service -f
```

### docker group

By default, only `root` (or a member of the `docker` group) can communicate with the Unix socket `/var/run/docker.sock`. To use Docker without `sudo`:

```bash
sudo usermod -aG docker $USER
newgrp docker   # ou se déconnecter/reconnecter
```

!!! danger "Interview Trap: the docker group = implicit root"
    Belonging to the `docker` group is **equivalent to having root access** on the host machine. Indeed, a container can be launched with `-v /:/host` and give full access to the host filesystem. This is a classic security interview question at Oracle: never add an untrusted user to the `docker` group without understanding this implication (see Part XII, Security — Rootless Docker).

### Root vs non-root

| Mode | Description | Security |
|---|---|---|
| Rootless | The daemon runs as a non-root user, via user namespaces | ✅ Recommended in sensitive environments |
| Standard (root) | The `dockerd` daemon runs as root (default) | ⚠️ Larger attack surface |

### docker info

Displays the full daemon state: number of containers (running/paused/stopped), number of images, storage driver used (`overlay2`), logging driver, cgroup driver (`systemd` or `cgroupfs`), kernel version, total resources (CPU/RAM), and registry configuration.

```bash
docker info
```

### docker version

Displays separately the **Client** and **Server (Engine)** versions — useful to diagnose an API incompatibility (e.g. client too recent for an old server, or vice versa).

```bash
docker version
```

??? question "Interview Question: You run `docker ps` and get `permission denied` on the socket. What do you do?"
    Two possible causes: (1) the user is not in the `docker` group → add them with `usermod -aG docker $USER` then reconnect; (2) the daemon is not started → check with `systemctl status docker`. You should **not** systematically recommend `sudo` in production: it's a workaround, not a solution, and it may hide a larger RBAC configuration problem.

??? question "Interview Question: What is the difference between `overlay2` and the older drivers (`aufs`, `devicemapper`)?"
    `overlay2` is the recommended storage driver since Linux kernel 4.0+: more performant, better natively supported by the kernel, and more stable. `aufs` is not in the mainline kernel (external patch), `devicemapper` in loopback mode is not recommended in production (degraded I/O performance). In an interview, mentioning `overlay2` as the default answer is almost always correct for a modern Linux host.
