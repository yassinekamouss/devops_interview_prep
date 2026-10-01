# 08 - Cheatsheet Entretien R&D

Ce document est votre filet de sécurité ultime pour les entretiens techniques d'ingénierie logicielle, DevOps, Cloud et MLOps chez Oracle R&D. Il condense les matrices de décision d'architecture, les mécaniques internes bas-niveau et les commandes d'investigation chirurgicales.

---

## 1. Comparatifs Architecturaux & Matrices de Décision (R&D Level)

| Comparaison | Explication attendue en entretien R&D |
| :--- | :--- |
| **Docker Compose vs K8s** | Compose est pour le dev local (mono-hôte). K8s est pour la prod (multi-hôtes, auto-healing, rolling updates, RBAC, SDN). |
| **Deployment vs StatefulSet** | Deployment pour le Stateless (APIs, web). StatefulSet pour le Stateful (Kafka, DBs) nécessitant une identité réseau stable (`ordinal`), un ordre strict et un stockage attaché persistant (`volumeClaimTemplates`). |
| **Service vs Ingress vs Gateway API** | - **Service :** Load balancing interne TCP/UDP (Couche 4).<br>- **Ingress :** Routage externe HTTP/HTTPS (Couche 7) basé sur l'hôte/URL, limité en expressivité.<br>- **Gateway API :** Le standard moderne K8s (SIG-Network) remplaçant Ingress : architecture orientée rôles (Infra Provider vs App Developer), routage dynamique cross-namespace, support L4/L7 natif et gRPC direct. |
| **HPA vs VPA vs Cluster Autoscaler** | - **HPA :** Ajoute des réplicas de Pods (Horizontal).<br>- **VPA :** Ajuste la taille CPU/RAM des Pods (Vertical - redémarrage souvent requis).<br>- **Cluster Autoscaler / Karpenter :** Ajoute/retire des nœuds physiques/VMs dès que des Pods passent en `Pending`. |
| **CNI : Calico vs Cilium vs OCI VCN-Native** | - **Calico :** Routage BGP natif ou VXLAN, NetworkPolicies iptables classiques.<br>- **Cilium :** Moteur **eBPF**, bypass de la stack TCP/IP hôte, observabilité Hubble L7 sans sidecar, chiffrement transparent WireGuard.<br>- **OCI VCN-Native :** Zéro overhead d'encapsulation, IP directement routable dans le VCN Oracle, support **RoCEv2** pour GPU distributed training. |

---

## 2. Commandes de Survie & Arsenal CLI Zsh Avancé

!!! success "L'Alias indispensable"
    En début de test technique, configurez immédiatement votre terminal Zsh :
    ```bash
    alias k=kubectl
    export do="--dry-run=client -o yaml"
    ```

### Commandes Fondamentales de Survie
- `k describe pod <pod-name>` : La première commande à taper si un pod ne démarre pas (regarder la section `Events`).
- `k logs <pod-name>` : Lire les logs du conteneur.
- `k logs <pod-name> --previous` : Lire les logs du conteneur avant son dernier crash (vital pour le `CrashLoopBackOff`).
- `k exec -it <pod-name> -- /bin/sh` : Ouvrir un shell dans un pod en cours d'exécution pour tester le réseau interne (`curl`, `ping`).
- `k get nodes -o wide` : Vérifier l'état et l'IP des nœuds.
- `k top pods` / `k top nodes` : Vérifier la consommation CPU/RAM (nécessite Metrics Server).
- `k get events --sort-by='.metadata.creationTimestamp'` : Voir tout ce qui se passe dans le cluster en temps réel.

### Les 10 One-Liners R&D Indispensables (Zsh & JSONPath)

```bash
# 1. Lister tous les Pods qui ne sont PAS en statut Running sur l'ensemble du cluster
k get pods -A --field-selector status.phase!=Running

# 2. Détecter les Deployments dangereux en production : AUCUNE readinessProbe configurée
k get deploy -A -o jsonpath='{range .items[?(!.spec.template.spec.containers[0].readinessProbe)]}{.metadata.namespace}{"/"}{.metadata.name}{"\n"}{end}'

# 3. Détecter les Pods en classe QoS BestEffort (interdits en prod car premières cibles de l'OOM Killer)
k get pods -A -o jsonpath='{range .items[?(@.status.qosClass=="BestEffort")]}{.metadata.namespace}{"/"}{.metadata.name}{"\n"}{end}'

# 4. Extraire les conteneurs ayant redémarré avec leur exit code Linux exact (Exit 137 = OOMKilled)
k get pods -A -o jsonpath='{range .items[?(@.status.containerStatuses[*].restartCount>0)]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{range .status.containerStatuses[*]}{"Conteneur:"}{.name}{" Restarts:"}{.restartCount}{" ExitCode:"}{.lastState.terminated.exitCode}{end}{"\n"}{end}'

# 5. Déployer instantanément un conteneur éphémère de test réseau avec destruction automatique (--rm)
k run debug-probe --rm -it --image=nicolaka/netshoot -- /bin/bash

# 6. Auditer les permissions effectives d'un ServiceAccount (Impersonation)
k auth can-i delete pods --as=system:serviceaccount:production:cicd-sa -n production

# 7. Trouver tous les PVC orphelins non montés par des Pods
comm -23 <(k get pvc -A -o custom-columns=NAME:.metadata.name --no-headers | sort) \
         <(k get pods -A -o jsonpath='{.items[*].spec.volumes[*].persistentVolumeClaim.claimName}' | tr ' ' '\n' | sort -u)

# 8. Mesurer la latence DNS réelle depuis l'intérieur d'un pod vers CoreDNS
k run -it --rm dns-test --image=busybox -- time nslookup kubernetes.default

# 9. Supprimer d'urgence un Pod bloqué en Terminating (Attention aux VolumeAttachments !)
k delete pod <pod-name> --grace-period=0 --force

# 10. Afficher les événements d'erreur récents triés chronologiquement
k get events -A --field-selector type=Warning --sort-by='.lastTimestamp'
```

---

## 3. Manifestes YAML de Production Essentiels

### A. Sécurité Pod Security Standards (PSS) au niveau Namespace

En production moderne (Kubernetes 1.25+), les `PodSecurityPolicies` (dépréciées) sont remplacées par les labels natifs **Pod Security Standards (PSS)** :

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production-restricted
  labels:
    # Applique le profil de sécurité le plus strict (interdiction de root, de hostNetwork, etc.)
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    # Avertit les développeurs dans kubectl sans bloquer les pods en cas de non-conformité
    pod-security.kubernetes.io/warn: restricted
```

### B. Gateway API : HTTPRoute (Le Remplaçant d'Ingress)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: payment-route
  namespace: production
spec:
  parentRefs:
  - name: internal-gateway
    namespace: infra-gateways
  hostnames:
  - "payment.oraclecloud.internal"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /v2/checkout
    backendRefs:
    - name: checkout-service
      port: 8080
      weight: 90
    - name: checkout-canary
      port: 8080
      weight: 10              # Split de trafic Canary natif sans plugin Ingress tiers
```

---

## 4. Top Scénarios d'Entretien (Mises en Situation Oracle R&D)

!!! question "Scénario : Un déploiement vient d'être fait, mais les utilisateurs ont des erreurs 502/503. Que faites-vous ?"
    **Action :** Je vérifie l'état des Pods (`k get pods`). S'ils crashent, je lis les logs. S'ils sont *Running*, je vérifie la *Readiness Probe* via `k describe pod`. Si elle échoue, les Pods sont retirés du *Service*, donc l'*Ingress* n'a nulle part où envoyer le trafic.

!!! question "Scénario : Vous devez déployer un modèle de Machine Learning lourd (10Go de RAM). Comment l'isoler ?"
    **Action :** J'utilise les *Taints* sur des nœuds spécifiques (ex: instances optimisées RAM/GPU) et j'ajoute une *Toleration* ainsi qu'une *NodeAffinity* dans le Deployment du modèle pour m'assurer qu'il atterrit sur la bonne machine sans perturber les APIs classiques.

!!! question "Scénario d'entretien Oracle : Cluster totalement figé suite à la saturation du quota d'espace etcd"
    **Examinateur :** "Plus aucune modification n'est possible sur le cluster. Toutes les commandes `kubectl apply` ou `helm upgrade` renvoient l'erreur fatale : `etcdserver: mvcc: database space exceeded`. L'API Server refuse toute écriture. 
    1. Quelle est la cause sous-jacente de ce blocage ?
    2. Pourquoi la simple suppression d'anciens Deployments avec `kubectl delete` est-elle impossible ?
    3. Quelle est la procédure chirurgicale exacte pour restaurer le cluster ?"

    **Réponse structurée attendue du candidat :**

    1. **Cause sous-jacente :**
       - etcd possède une limite de stockage de sécurité par défaut (`--quota-backend-bytes`, typiquement 2GB, extensible à 8GB max).
       - En raison de l'accumulation d'anciennes révisions MVCC (créations de pods, cronjobs, secrets), la base `bbolt` a atteint ce quota. Dès que le quota est dépassé, etcd active une alarme `NOSPACE` et bascule l'ensemble du cluster en mode lecture seule stricte.

    2. **Impossibilité du `kubectl delete` :**
       - Sous etcd, une suppression est en réalité une **nouvelle écriture MVCC** (génération d'un enregistrement de type *tombstone* avec une nouvelle révision globale incrémentée). Tenter de supprimer un objet nécessite de l'espace disque supplémentaire et échoue donc avec la même erreur.

    3. **Procédure de déblocage chirurgicale :**
       - **Étape 1 : Obtenir la révision actuelle d'etcd** :
         `rev=$(etcdctl endpoint status --write-out="json" | jq .[0].Status.header.revision)`
       - **Étape 2 : Compacter l'historique jusqu'à la révision actuelle** :
         `etcdctl compact $rev`
       - **Étape 3 : Défragmenter le fichier bbolt pour restituer les blocs vides à l'OS** :
         `etcdctl defrag --endpoints=https://127.0.0.1:2379`
       - **Étape 4 : Désactiver l'alarme de sécurité** :
         `etcdctl alarm disarm`
       - **Étape 5 (Pérennisation) :** Configurer `--auto-compaction-retention=1h` et augmenter `--quota-backend-bytes=8589934592` (8GB) dans les arguments statiques de kube-apiserver/etcd.

!!! question "Scénario d'entretien Oracle : Pod bloqué indéfiniment en statut `Terminating` (Finalizer orphelin)"
    **Examinateur :** "Un Pod applicatif a été supprimé il y a 3 heures mais reste bloqué en statut `Terminating`. Le Kubelet a pourtant bien arrêté le conteneur physique sur la machine hôte. Qu'est-ce qui bloque la suppression dans l'API Kubernetes et comment le débloquer proprement ?"

    **Réponse structurée attendue du candidat :**

    1. **Cause racine (Les Finalizers) :**
       - Dans Kubernetes, lorsqu'un objet possède des `.metadata.finalizers`, l'API Server n'efface pas l'enregistrement d'etcd lors d'un `DELETE`. Il se contente de positionner un timestamp `deletionTimestamp`.
       - L'objet reste visible avec le statut `Terminating` tant qu'un contrôleur tiers (ex: un opérateur de stockage, un service mesh ou un contrôleur de backup) n'a pas finalisé ses opérations de nettoyage et retiré sa clé de la liste des finalizers.
       - Si le contrôleur externe est en panne, crashé ou désinstallé, le Pod reste bloqué à jamais.

    2. **Diagnostic & Résolution :**
       - Inspecter la liste des finalizers bloquants :
         `kubectl get pod <pod-name> -o jsonpath='{.metadata.finalizers}'`
       - Résolution d'urgence : Si le conteneur est confirmé mort sur le nœud physique et qu'aucun dommage de données n'est encouru, retirer le finalizer bloquant par patch JSON à chaud :
         `kubectl patch pod <pod-name> -p '{"metadata":{"finalizers":null}}' --type=merge`
       - L'API Server efface immédiatement l'objet d'etcd sans attendre.