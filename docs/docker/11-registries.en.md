# Part XI — Docker Registries

## Chapter 29

### Docker Hub

Default public registry. Limits to know: anonymous pull quota (rate limiting per IP), automatic retention of inactive images on free accounts.

### Private Registry

A self-hosted registry (official image `registry:2`, or full solutions like Harbor) gives total control: retention, integrated vulnerability scanning, replication, internal RBAC.

```bash
docker run -d -p 5000:5000 --name registry registry:2
docker tag mon-app:1.0 localhost:5000/mon-app:1.0
docker push localhost:5000/mon-app:1.0
```

### Oracle Container Registry

Managed service of Oracle Cloud Infrastructure (OCIR). URL format type `<region>.ocir.io/<namespace>/<repo>:<tag>`. Natively integrated with OCI IAM for permissions (policies), and with OKE (Oracle Kubernetes Engine) for pulling images without additional network configuration within the same tenancy.

```bash
docker login <région>.ocir.io -u '<namespace>/<utilisateur>' -p '<auth-token>'
docker tag mon-app:1.0 <région>.ocir.io/<namespace>/mon-app:1.0
docker push <région>.ocir.io/<namespace>/mon-app:1.0
```

!!! danger "Oracle Interview Trap"
    OCIR authentication does **not** use the OCI account password but an **auth token** generated separately from the IAM console. Confusing the two is a frequent mistake in Oracle technical interviews — be sure to mention it explicitly.

### GitHub Container Registry

`ghcr.io`, natively integrated with GitHub Actions (authentication via `GITHUB_TOKEN`, without separate credentials to manage in CI).

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker push ghcr.io/USERNAME/mon-app:1.0
```

### Authentication

#### Login

```bash
docker login                          # Docker Hub
docker login registry.exemple.com     # registre privé
```

Credentials are stored (in plain text by default, or via an OS credential helper — `pass`, Keychain, Windows Credential Manager) in `~/.docker/config.json`.

!!! danger "Security Interview Trap"
    Without a credential helper configured, `docker login` stores the token **in base64 (unencrypted)** in `~/.docker/config.json`. In CI/CD, never do `docker login` with a plain-text password in logs — use CI secrets and `--password-stdin` to prevent the password from appearing in shell history or process listings.

#### Push

Requires the image to be tagged with the target registry hostname (`docker tag`) before `docker push` — otherwise Docker assumes Docker Hub by default.

#### Pull

```bash
docker pull registry.exemple.com/mon-app:1.0
```

??? question "Interview Question: How to secure access to a private registry in a CI/CD pipeline?"
    Use dedicated CI secrets (never in plain text in the pipeline YAML), a service account with minimal privileges (push/pull access scoped to a single repository if possible), regular token/auth token rotation, and `--password-stdin` rather than `--password` to avoid exposure on the command line.
