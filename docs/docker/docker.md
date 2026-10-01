# Docker — Vue d'ensemble

!!! info "Objectif de cette section"
    Préparation complète Docker pour l'entretien **DevOps Engineer chez Oracle** : théorie, architecture interne, commandes, bonnes pratiques et plus de 120 questions d'entretien classées par difficulté.

## Plan de la section

| Partie | Contenu | Priorité entretien |
|---|---|---|
| I. Introduction | Historique, problèmes résolus, VM vs conteneurs | 🟢 Basique |
| II. Architecture interne | Client/Daemon, namespaces, cgroups, UnionFS | 🔴 Critique |
| III. Installation | Linux, WSL2, configuration | 🟡 Moyenne |
| IV. Images | Layers, Docker Hub, gestion | 🟢 Basique |
| V. Conteneurs | Cycle de vie, commandes, ressources | 🔴 Critique |
| VI. Dockerfile | Instructions, multi-stage, optimisation | 🔴 Critique |
| VII. Réseau | Bridge, overlay, port mapping | 🔴 Critique |
| VIII. Volumes | Persistance, bind mount, tmpfs | 🟡 Moyenne |
| IX. Variables d'env | ENV, ARG, secrets | 🟡 Moyenne |
| X. Compose | compose.yaml, commandes | 🔴 Critique |
| XI. Registres | Docker Hub, GHCR, OCR | 🟢 Basique |
| XII. Sécurité | Rootless, capabilities, seccomp | 🔴 Critique |
| XIII. Débogage | Logs, inspect, events | 🟡 Moyenne |
| XIV. Production | Monitoring, HA, rollback | 🔴 Critique |
| XV. DevOps | CI/CD, Jenkins, GitHub Actions, ArgoCD | 🔴 Critique |
| XVI. Kubernetes | Pourquoi K8s, pods, différences | 🔴 Critique |
| XVII. Questions | Banque de questions Oracle | 🔴 Critique |

## Comment utiliser cette section

- Les blocs `!!! danger "Piège d'entretien"` signalent les questions classiques où les candidats se trompent.
- Les blocs `??? question "Question d'entretien"` sont dépliables — testez-vous avant de lire la réponse.
- Les schémas `mermaid` sont à savoir **redessiner à la main** au tableau si demandé en entretien.