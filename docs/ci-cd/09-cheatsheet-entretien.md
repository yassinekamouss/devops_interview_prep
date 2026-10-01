# 09 - Cheatsheet Entretien CI/CD

Ce document rassemble les éléments clés à garder en tête juste avant votre entretien. Il synthétise les concepts, les mots-clés et les réponses aux mises en situation classiques pour des postes orientés Cloud, DevOps ou MLOps.

## 1. Les Mots-Clés (Buzzwords) à utiliser à bon escient

- **Pipeline as Code / IaC :** Versionnement de toute la configuration.
- **Shift-Left :** Intégrer les tests et la sécurité (DevSecOps) le plus tôt possible dans le cycle (dès le commit).
- **Immuabilité (Build once, deploy anywhere) :** L'artefact ne change jamais entre les environnements.
- **Éphémère / Stateless :** Des runners de CI jetables (ex: pods K8s sur AWS EKS).
- **Métriques DORA :** Lead Time, Deployment Frequency, MTTR, Change Failure Rate.
- **GitOps :** Pull model, réconciliation de l'état, Git comme source de vérité.

## 2. Scénarios Pratiques (Mises en situation)

!!! question "Scénario 1 : « Le pipeline prend 45 minutes, les développeurs se plaignent. Que faites-vous ? »"
    **Réponse structurée :**
    1. **Auditer :** J'analyse les logs pour identifier le goulot d'étranglement (Build Docker ? Tests E2E ?).
    2. **Mettre en cache :** J'implémente le cache des dépendances (Maven, NPM) et le Docker Layer Caching.
    3. **Paralléliser :** Je sépare les tests unitaires, d'intégration et le scan de sécurité pour qu'ils tournent en même temps (Fan-out).
    4. **Fail-fast :** Je m'assure que les vérifications rapides (lint, SAST) s'exécutent en premier.

!!! question "Scénario 2 : « Un développeur a pushé une clé secrète AWS en clair sur GitHub. Quelle est votre procédure ? »"
    **Réponse structurée :**
    
    1. **Révocation immédiate :** Je vais sur la console AWS et je désactive/supprime la clé compromise instantanément. (Ne pas juste supprimer le commit, car les bots ont déjà la clé).
    2. **Rotation :** Je génère de nouvelles clés et les place dans le Secret Manager (Vault, GitHub Secrets).
    3. **Audit :** Je vérifie CloudTrail pour m'assurer que la clé compromise n'a pas été utilisée pour des actions malveillantes.
    4. **Prévention (Shift-Left) :** J'ajoute un outil comme `trufflehog` ou `git-secrets` dans les pre-commit hooks et dans la CI pour bloquer tout futur push contenant des secrets.

!!! question "Scénario 3 : « Comment gérez-vous le CI/CD si l'on déploie non pas une application web, mais un pipeline Big Data ou des modèles de Machine Learning ? »"
    **Réponse structurée :**
    L'approche reste similaire mais s'enrichit. Pour du ML (MLOps), au lieu de builder juste du code, on intègre le *Continuous Training* (CT).
    
    1. Le code de l'entraînement et des pipelines de données (ex: PySpark, Kafka) est versionné.
    2. La CI lance des tests sur le traitement des données avec des datasets factices.
    3. L'artefact généré n'est plus seulement une image Docker, mais aussi un modèle versionné dans un registre (comme MLflow).
    4. Le déploiement (via Kubernetes/Kubeflow) expose ce modèle via une API (ex: FastAPI) en utilisant des stratégies Canary pour valider sa précision en production avant de basculer 100% du trafic.

## 3. Checklist Finale

- [x] Je sais différencier CI, Delivery (CD) et Deployment (CD).
- [x] Je sais expliquer Blue-Green vs Canary.
- [x] Je connais la différence entre Jenkins (On-premise, Controller/Agent) et GitHub Actions (SaaS, Event-driven).
- [x] Je sais pourquoi GitOps (Pull) est plus sécurisé que la CI classique (Push).