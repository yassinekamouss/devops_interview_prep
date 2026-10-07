# Part XII — Docker Security

## Chapter 30

### Least Privilege

Guiding principle of all container security: each container should only have access to resources strictly necessary for its operation — no unnecessary root, no superfluous capabilities, no Docker socket mount unless absolutely necessary.

### Rootless Docker

The daemon itself runs as a **non-root** user on the host, via user namespaces (Part II, Chapter 5): "root" inside a container is mapped to an unprivileged UID on the host.

```bash
dockerd-rootless-setuptool.sh install
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
```

!!! danger "Interview Trap"
    Rootless Docker limits some features: no direct access to certain privileged ports (<1024) without additional configuration, no native support for some network drivers (`macvlan`), sometimes reduced I/O performance (via `fuse-overlayfs` instead of native `overlay2` depending on kernel config). It is not a universal solution; it is a security/functionality trade-off to evaluate depending on context.

### Capabilities

The Linux kernel splits root privileges into granular units (capabilities). Docker already drops most by default, but you can restrict further:

```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE mon-app
```

`--cap-drop=ALL` removes everything, then `--cap-add` only re-allows the strict minimum (here, the ability to bind to a port <1024 without being root).

### Seccomp

Filters **system calls (syscalls)** that a container can make. Docker applies a default profile blocking ~44 dangerous syscalls (e.g. `reboot`, `mount`). A custom profile can restrict further according to the application.

```bash
docker run --security-opt seccomp=profil-custom.json mon-app
```

### AppArmor

Mandatory Access Control (MAC) system active by default on Ubuntu/Debian. Docker applies a default profile restricting access to files, network, capabilities for each container.

### SELinux

Equivalent of AppArmor, used by default on RHEL/CentOS/Fedora. Applies security labels (contexts) to each process and file — a container can only access resources labeled for it.

!!! danger "Interview Trap"
    Never disable SELinux/AppArmor "to make it work" (`--security-opt apparmor=unconfined` or `setenforce 0`) without understanding the cause of the block — it's a security workaround, not a fix. Diagnose first via logs (`journalctl`, `audit.log`) the exact denied call.

### Secrets

See Part IX, Chapter 25 — never in `ENV`/`ARG`, always via Compose `secrets:`, BuildKit `--mount=type=secret`, or an external manager (Vault, Oracle Vault, AWS Secrets Manager).

### Image Scanning

```bash
docker scout cves mon-app:1.0
trivy image mon-app:1.0
```

Systematically scan images before publishing (CI/CD) to detect known CVEs in the base image and installed dependencies.

### Docker Bench

Official script (`docker/docker-bench-security`) that audits daemon and container configuration against the **CIS Docker Benchmark** (industry-recognized best-practice security baseline).

```bash
docker run --net host --pid host --cap-add audit_control \
  -v /var/lib:/var/lib -v /var/run/docker.sock:/var/run/docker.sock \
  docker/docker-bench-security
```

### Image Signing

Cryptographic signing of images to guarantee their integrity and provenance, via **Docker Content Trust** (Notary) or **Sigstore/Cosign** (emerging standard, registry-independent).

```bash
export DOCKER_CONTENT_TRUST=1
docker push mon-app:1.0    # signe automatiquement si DCT activé
```

### SBOM

The Software Bill of Materials lists **all components** (packages, libraries, versions) present in an image — essential to quickly trace exposure to a newly discovered CVE.

```bash
docker sbom mon-app:1.0
```

??? question "Interview Question: Can a root container compromise the host?"
    Yes, potentially — without user namespace remapping, root inside the container corresponds to UID 0 on the host. Combined with a misconfiguration (`--privileged`, Docker socket mounted, dangerous capability like `SYS_ADMIN`), an attacker with root inside the container can escape to the host. Hence the cumulative importance of: non-root `USER` in the Dockerfile, `--cap-drop=ALL`, rootless Docker, and never using `--privileged` except for absolute and isolated technical necessity.

??? question "Interview Question: What does the `--privileged` flag do and why is it dangerous?"
    It disables **all** security restrictions (full capabilities, access to all host devices, seccomp/AppArmor disabled). It is almost equivalent to giving full root access to the host from the container. Reserved for very specific cases (Docker-in-Docker, low-level hardware access) — never by default, never on an untrusted image.
