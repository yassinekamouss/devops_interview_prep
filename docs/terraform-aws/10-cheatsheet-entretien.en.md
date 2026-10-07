# 10 - R&D Interview Cheatsheet

This document is your ultimate survival cheatsheet for DevOps, Cloud Platform, and SRE technical interviews (especially at Oracle Cloud, major software vendors, and Cloud R&D environments). It brings together architecture decision matrices, surgical CLI arsenal, and the 15 most dreaded incident scenarios in interviews.

---

## 1. Decision Matrices & Architectural Comparisons (R&D Level)

| Trade-off | R&D Interview Recommendation | Technical Justification / Trap |
|---|---|---|
| **Terraform vs Ansible** | **Terraform** for IaaS provisioning (VPC, EKS, RDS); **Ansible** for in-guest configuration (OS packages, config files). | Terraform manages the full lifecycle (declaration, update, declarative destruction) via its State. Ansible is an imperative orchestration tool without a global lifecycle State. |
| **Terraform vs OpenTofu** | Functional equivalents; OpenTofu is 100% open source under Linux Foundation governance (MPL-2.0 license). | HashiCorp switched Terraform to the commercial BSL license in 2023. OpenTofu guarantees no competitive restriction for managed platforms. |
| **Workspaces vs Dedicated Directories** | **Dedicated directories** (`environments/dev`, `staging`, `prod`) for production. | Workspaces share the same state backend and AWS account, creating a critical human-error risk (`workspace select`). Folders enable strict isolation of AWS accounts and KMS keys. |
| **Monolithic State vs Micro-States** | **Micro-States split by layer** (Network, Security, Compute, Data). | Reduces blast radius, speeds up DAG computation during plans, and avoids DynamoDB lock contention at enterprise scale. |
| **Standalone SG Rules vs Inline SG Rules** | Use exclusively **Standalone** resources (`aws_vpc_security_group_ingress_rule`). | Inline blocks inside `aws_security_group` cause unsolvable mutual dependency cycles if two security groups must allow each other. |
| **IRSA vs Instance Profile on EKS** | **IRSA (IAM Roles for Service Accounts)** systematically. | An Instance Profile gives the same Cloud privileges to **all** containers hosted on the Worker Node. IRSA isolates AWS rights at the individual Pod level. |

---

## 2. Survival CLI Arsenal & Surgical Debugging

### A. Emergency Debugging of AWS API Calls
When Terraform fails with an opaque error or an incomprehensible AWS network timeout:

```bash
# 1. Active le logging verbeux au niveau gRPC et HTTP (affiche les requêtes AWS SigV4)
export TF_LOG=DEBUG
export TF_LOG_PATH="./terraform_debug.log"

# 2. Exécute l'action pour capturer la trace exacte des échanges avec l'API AWS
terraform apply -auto-approve

# 3. Réinitialise le logging après diagnostic
unset TF_LOG TF_LOG_PATH
```

### B. Surgical State Rescue & Manipulation

```bash
# 1. Déverrouiller un State bloqué après le crash d'un pipeline CI
terraform force-unlock <LOCK_ID>

# 2. Renommer une ressource dans le State sans la détruire sur AWS
terraform state mv aws_instance.old_name aws_instance.new_name

# 3. Déplacer une ressource vers un module sans recréation
terraform state mv aws_security_group.web module.networking.aws_security_group.web

# 4. Désindexer une ressource du State sans la supprimer sur AWS (ex: sauvetage d'urgence)
terraform state rm aws_db_instance.critical_postgres

# 5. Forcer le remplacement d'une instance défaillante sans toucher au reste (remplace taint)
terraform apply -replace="aws_instance.worker_node"
```

### C. Importing & Adopting Existing Infrastructure

```bash
# Bloc HCL à insérer dans le code (Terraform 1.5+)
import {
  to = aws_s3_bucket.legacy
  id = "nom-du-bucket-existant-sur-aws"
}

# Génère automatiquement le fichier HCL correspondant sans rien écraser
terraform plan -generate-config-out=generated_resources.tf
```

### D. Exploiting Plans & Graph in CI/CD

```bash
# Sauvegarder un plan binaire pour exécution garantie
terraform plan -out=tfplan

# Convertir le plan binaire en JSON pour inspection par script de sécurité (jq, trivy)
terraform show -json tfplan > tfplan.json

# Détecter si des modifications sont prévues (Exit 0 = Pas de changement, 2 = Modifications, 1 = Erreur)
terraform plan -detailed-exitcode

# Générer et visualiser le graphe de dépendances complet en image
terraform graph | dot -Tsvg > dependency_graph.svg
```

---

## 3. Top 15 Failure Scenarios & Interview Traps

!!! question "1. What happens if a colleague manually deletes an EC2 instance in the AWS console (Drift)?"
    On the next `terraform plan`, Terraform queries the AWS API (`ec2:DescribeInstances`), notices the instance no longer exists in the Cloud although it is still recorded in State, and proposes to **recreate (+)** a new instance to restore the declared state from HCL code.

!!! question "2. What if two CI/CD runners try to run `terraform apply` at the same time?"
    The first runner acquires the write lock in the **DynamoDB** table (writing the item with `LockID`). The second runner immediately receives an `Error acquiring the state lock` error and its execution stops dead, thus protecting State from any concurrent corruption.

!!! question "3. How do you prevent accidental deletion of a critical database during `terraform destroy`?"
    Two levels of protection are configured:
    1. In Terraform: the `lifecycle { prevent_destroy = true }` meta-argument inside the HCL resource. Any destruction attempt will make the `plan` fail immediately.
    2. On the AWS side: the native RDS API attribute `deletion_protection = true`.

!!! question "4. A `terraform apply` fails halfway (e.g., elastic IP quota reached). What state is the infrastructure left in?"
    Terraform applies resources progressively. Resources successfully created before the error are immediately recorded in State. Those that could not be provisioned are not in State. The state is not corrupted: after fixing the problem (e.g., increasing AWS quota), simply re-run `terraform apply` for Terraform to resume exactly where it left off (idempotence).

!!! question "5. Where are passwords and sensitive data declared with `sensitive = true` stored?"
    The `sensitive = true` argument only hides the value in console output and logs. **The value remains stored in plain text in the `terraform.tfstate` file**. That is why State security depends entirely on S3 bucket encryption at rest (KMS), drastic IAM access restrictions to the bucket, and the prohibition on committing state to Git.

!!! question "6. How do you resolve a circular dependency between two Security Groups?"
    If group A must allow group B and group B must allow group A, defining inline rules inside `aws_security_group` blocks creates a deadlock. The solution is to create both `aws_security_group` blocks empty of rules, then add rules independently via dedicated **`aws_vpc_security_group_ingress_rule`** resources.

!!! question "7. Why is the standalone `terraform refresh` command discouraged today?"
    Historically, `terraform refresh` directly modified State without giving the operator a preview. Since Terraform 0.15+, the preferred command is `terraform apply -refresh-only` (or `plan -refresh-only`), which first shows the report of drifts detected on AWS and asks for explicit confirmation before updating State.

!!! question "8. How do you migrate a project from local State to an S3 Remote Backend without recreating everything?"
    Simply add the `backend "s3" {}` block in the HCL configuration, then run `terraform init`. Terraform detects the presence of an existing local State and automatically asks: *"Do you want to copy existing state to the new backend?"*. Answering `yes`, Terraform uploads the state to the S3 bucket and enables DynamoDB locking without impacting resources on AWS.

!!! question "9. What is the difference between `count` and `for_each` for instantiating multiple resources?"
    `count` uses a numeric index (`[0]`, `[1]`, `[2]`). If you remove the first element from a list in the middle, Terraform shifts all subsequent indices, which can cause unnecessary destruction and recreation of all following resources. `for_each` uses unique textual keys (maps or sets of identifiers): removing one element only affects the targeted resource, without impacting others.

!!! question "10. How do you handle a clean rollback with Terraform in production?"
    Never run a partial manual `terraform destroy`. In GitOps practice, simply do a `git revert` of the faulty commit on the `main` branch. CI/CD generates a new cancellation plan (which restores previous configurations) and applies it deterministically and in a tracked manner.

!!! question "11. How do you pass a secret to Terraform in CI/CD without creating a temporary file on the runner's disk?"
    Use system environment variables prefixed with `TF_VAR_`. For example, in the pipeline, export `export TF_VAR_db_password="$SECRET_VAULT_VALUE"`. Terraform automatically associates this environment variable with the `variable "db_password" {}` input variable declared in HCL code.

!!! question "12. Why is it discouraged to run `terraform apply -target` in production?"
    `-target` applies changes in isolation on one resource without updating the rest of the dependency graph. This creates an incomplete state, hides potential conflicts with other components, and can leave orphaned resources. It is an absolute emergency tool, never a standard deployment mode.

!!! question "13. How does Terraform handle ordered destruction of resources?"
    Terraform simply reverses the Directed Acyclic Graph (DAG) computed during creation. If resource B depends on resource A (e.g., an EC2 instance placed in a Subnet), Terraform first destroys the EC2 instance (B), then the Subnet (A).

!!! question "14. What is the best practice for testing module changes without breaking the team?"
    Use a Git branching and semantic tagging strategy. The module developer works on a dedicated branch and tests code with automated test frameworks like **Terratest** (in Go) or the native `terraform test` framework (introduced in v1.6). Once validated, a new tagged release (e.g., `v2.0.0`) is published without affecting users of version `v1.x`.

!!! question "15. What is 'Blast Radius' and how do you minimize it with Terraform on AWS?"
    Blast Radius refers to the extent of potential damage in case of mishandling or State corruption. To minimize it:
    
    - Split infrastructure into several sealed projects/states (network layer, Kubernetes layer, database layer).
    - Apply the principle of least privilege on CI/CD IAM roles (an application's deployment role must not have permission to modify the VPC).
    - Use separate AWS accounts for each environment (Dev, Staging, Prod).
