# 10 - Cheatsheet Entretien R&D

Ce document est votre condensé de survie ultime pour les entretiens techniques d'ingénierie DevOps, Cloud Platform et SRE (notamment chez Oracle Cloud, grands éditeurs et environnements Cloud R&D). Il regroupe les matrices de décision d'architecture, l'arsenal CLI chirurgical et les 15 scénarios d'incident les plus redoutés en entretien.

---

## 1. Matrices de Décision & Comparatifs Architecturaux (R&D Level)

| Arbitrage | Recommandation en Entretien R&D | Justification Technique / Piège |
|---|---|---|
| **Terraform vs Ansible** | **Terraform** pour le provisionnement IaaS (VPC, EKS, RDS) ; **Ansible** pour la configuration in-guest (paquets OS, fichiers de conf). | Terraform gère le cycle de vie complet (déclaration, mise à jour, destruction déclarative) via son State. Ansible est un outil d'orchestration impératif sans State de cycle de vie global. |
| **Terraform vs OpenTofu** | Équivalents fonctionnels ; OpenTofu est 100% open-source sous gouvernance Linux Foundation (licence MPL-2.0). | HashiCorp a basculé Terraform sous licence commerciale BSL en 2023. OpenTofu garantit l'absence de restriction de concurrence pour les plateformes managées. |
| **Workspaces vs Répertoires Dédiés** | **Répertoires dédiés** (`environments/dev`, `staging`, `prod`) pour la production. | Les workspaces partagent le même backend d'état et le même compte AWS, créant un risque critique d'erreur humaine (`workspace select`). Les dossiers permettent une isolation stricte des comptes AWS et des clés KMS. |
| **Monolith State vs Micro-States** | **Micro-States découpés par couche** (Réseau, Sécurité, Compute, Data). | Réduit le rayon d'impact (Blast Radius), accélère le calcul du DAG lors des plans et évite les blocages de verrous DynamoDB à l'échelle de l'entreprise. |
| **Standalone SG Rules vs Inline SG Rules** | Utiliser exclusivement les ressources **Standalone** (`aws_vpc_security_group_ingress_rule`). | Les blocs inline intégrés dans `aws_security_group` provoquent des cycles de dépendance mutuelle impossibles à résoudre si deux groupes de sécurité doivent s'autoriser mutuellement. |
| **IRSA vs Instance Profile sur EKS** | **IRSA (IAM Roles for Service Accounts)** systématiquement. | Un Instance Profile donne les mêmes privilèges Cloud à **tous** les conteneurs hébergés sur le Worker Node. IRSA isole les droits AWS au niveau de chaque Pod individuel. |

---

## 2. Arsenal CLI de Survie & Debugging Chirurgical

### A. Debugging d'Urgence des Appels API AWS
Lorsque Terraform échoue avec une erreur opaque ou un timeout réseau AWS incompréhensible :

```bash
# 1. Active le logging verbeux au niveau gRPC et HTTP (affiche les requêtes AWS SigV4)
export TF_LOG=DEBUG
export TF_LOG_PATH="./terraform_debug.log"

# 2. Exécute l'action pour capturer la trace exacte des échanges avec l'API AWS
terraform apply -auto-approve

# 3. Réinitialise le logging après diagnostic
unset TF_LOG TF_LOG_PATH
```

### B. Sauvetage & Manipulation Chirurgicale du State

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

### C. Importation & Adoption d'Infrastructure Déjà Existante

```bash
# Bloc HCL à insérer dans le code (Terraform 1.5+)
import {
  to = aws_s3_bucket.legacy
  id = "nom-du-bucket-existant-sur-aws"
}

# Génère automatiquement le fichier HCL correspondant sans rien écraser
terraform plan -generate-config-out=generated_resources.tf
```

### D. Exploitation des Plans & Graph en CI/CD

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

## 3. Top 15 des Scénarios de Panne & Pièges d'Entretien

!!! question "1. Que se passe-t-il si un collègue supprime manuellement une instance EC2 dans la console AWS (Drift) ?"
    Lors du prochain `terraform plan`, Terraform interroge l'API AWS (`ec2:DescribeInstances`), constate que l'instance n'existe plus dans le Cloud bien qu'elle soit toujours inscrite dans le State, et propose de **recréer (+)** une nouvelle instance pour rétablir l'état déclaré dans le code HCL.

!!! question "2. Que faire si deux runners CI/CD tentent d'exécuter `terraform apply` en même temps ?"
    Le premier runner acquiert le verrou d'écriture dans la table **DynamoDB** (écriture de l'item avec `LockID`). Le second runner reçoit immédiatement une erreur `Error acquiring the state lock` et son exécution s'arrête net, protégeant ainsi le State de toute corruption concurrentielle.

!!! question "3. Comment empêcher la suppression accidentelle d'une base de données critique lors d'un `terraform destroy` ?"
    On configure deux niveaux de protection :
    1. Dans Terraform : le méta-argument `lifecycle { prevent_destroy = true }` au sein de la ressource HCL. Toute tentative de destruction fera échouer le `plan` immédiatement.
    2. Côté AWS : l'attribut natif de l'API RDS `deletion_protection = true`.

!!! question "4. Un `terraform apply` échoue à mi-parcours (ex: quota d'IP élastiques atteint). Dans quel état reste l'infrastructure ?"
    Terraform applique les ressources au fur et à mesure. Les ressources créées avec succès avant l'erreur sont immédiatement enregistrées dans le State. Celles qui n'ont pas pu être provisionnées ne sont pas dans le State. L'état n'est pas corrompu : après avoir résolu le problème (ex: augmentation de quota AWS), il suffit de relancer `terraform apply` pour que Terraform reprenne exactement là où il s'était arrêté (idempotence).

!!! question "5. Où sont stockés les mots de passe et données sensibles déclarés avec `sensitive = true` ?"
    L'argument `sensitive = true` masque uniquement la valeur dans la sortie console et les logs. **La valeur reste stockée en clair dans le fichier `terraform.tfstate`**. C'est pourquoi la sécurité du State dépend entièrement du chiffrement au repos du bucket S3 (KMS), de la restriction drastique des accès IAM au bucket et de l'interdiction de commiter le state dans Git.

!!! question "6. Comment résoudre une dépendance circulaire entre deux Security Groups ?"
    Si le groupe A doit autoriser le groupe B et le groupe B doit autoriser le groupe A, définir les règles en ligne (`inline`) dans les blocs `aws_security_group` crée un deadlock. La solution est de créer les deux blocs `aws_security_group` vides de règles, puis d'ajouter les règles indépendamment via des ressources dédiées **`aws_vpc_security_group_ingress_rule`**.

!!! question "7. Pourquoi la commande `terraform refresh` seule est-elle déconseillée aujourd'hui ?"
    Historiquement, `terraform refresh` modifiait directement le State sans donner de prévisualisation à l'opérateur. Depuis Terraform 0.15+, on lui préfère la commande `terraform apply -refresh-only` (ou `plan -refresh-only`), qui affiche d'abord le rapport des dérives détectées sur AWS et demande une confirmation explicite avant de mettre à jour le State.

!!! question "8. Comment migrer un projet d'un State local vers un Remote Backend S3 sans tout recréer ?"
    On ajoute simplement le bloc `backend "s3" {}` dans la configuration HCL, puis on exécute `terraform init`. Terraform détecte la présence d'un State local existant et demande automatiquement : *"Do you want to copy existing state to the new backend?"*. En répondant `yes`, Terraform téléverse l'état vers le bucket S3 et active le verrou DynamoDB sans impacter les ressources sur AWS.

!!! question "9. Quelle est la différence entre `count` et `for_each` pour instancier des ressources multiples ?"
    `count` utilise un index numérique (`[0]`, `[1]`, `[2]`). Si vous supprimez le premier élément d'une liste au milieu, Terraform décale tous les index suivants, ce qui peut provoquer la destruction et recréation inutile de toutes les ressources suivantes. `for_each` utilise des clés textuelles uniques (maps ou sets d'identifiants) : supprimer un élément ne modifie que la ressource ciblée, sans impacter les autres.

!!! question "10. Comment gérer un rollback propre avec Terraform en production ?"
    On ne lance jamais de `terraform destroy` partiel manuel. En pratique GitOps, on effectue un simple `git revert` du commit fautif sur la branche `main`. La CI/CD génère un nouveau plan d'annulation (qui remet les configurations antérieures) et l'applique de façon déterministe et tracée.

!!! question "11. Comment passer un secret à Terraform en CI/CD sans créer de fichier temporaire sur le disque du runner ?"
    On utilise les variables d'environnement système préfixées par `TF_VAR_`. Par exemple, dans le pipeline, on exporte `export TF_VAR_db_password="$SECRET_VAULT_VALUE"`. Terraform associe automatiquement cette variable d'environnement à la variable d'entrée `variable "db_password" {}` déclarée dans le code HCL.

!!! question "12. Pourquoi est-il déconseillé d'exécuter `terraform apply -target` en production ?"
    `-target` applique les changements de façon isolée sur une ressource sans mettre à jour le reste du graphe de dépendances. Cela crée un état incomplet, masque d'éventuels conflits avec les autres composants et peut laisser des ressources orphelines. C'est un outil d'urgence absolue, jamais un mode de déploiement standard.

!!! question "13. Comment Terraform gère-t-il la destruction ordonnée des ressources ?"
    Terraform inverse tout simplement le Directed Acyclic Graph (DAG) calculé lors de la création. Si la ressource B dépend de la ressource A (ex: une instance EC2 placée dans un Subnet), Terraform détruit d'abord l'instance EC2 (B), puis le Subnet (A).

!!! question "14. Quelle est la bonne pratique pour tester des modifications de modules sans casser l'équipe ?"
    On utilise une stratégie de branches Git et de tags sémantiques. Le développeur du module travaille sur une branche dédiée et teste son code avec des frameworks de test automatisés comme **Terratest** (en Go) ou le framework natif `terraform test` (introduit en v1.6). Une fois validé, une nouvelle release étiquetée (ex: `v2.0.0`) est publiée sans affecter les utilisateurs de la version `v1.x`.

!!! question "15. En quoi consiste le 'Blast Radius' et comment le minimiser avec Terraform sur AWS ?"
    Le Blast Radius (rayon d'impact) désigne l'étendue des dégâts potentiels en cas d'erreur de manipulation ou de corruption du State. Pour le minimiser :
    - On découpe l'infrastructure en plusieurs projets/states étanches (couche réseau, couche Kubernetes, couche base de données).
    - On applique le principe du moindre privilège sur les rôles IAM de la CI/CD (le rôle de déploiement d'une application ne doit pas avoir le droit de modifier le VPC).
    - On utilise des comptes AWS séparés pour chaque environnement (Dev, Staging, Prod).