# 09 - CI/CD Interview Cheatsheet

This document gathers key points to keep in mind just before your interview. It summarizes concepts, keywords and answers to classic situational questions for Cloud, DevOps or MLOps roles.

## 1. Keywords (Buzzwords) to Use Wisely

- **Pipeline as Code / IaC:** Versioning all configuration.
- **Shift-Left:** Integrating tests and security (DevSecOps) as early as possible in the cycle (from the commit).
- **Immutability (Build once, deploy anywhere):** The artifact never changes between environments.
- **Ephemeral / Stateless:** Disposable CI runners (e.g., K8s pods on AWS EKS).
- **DORA Metrics:** Lead Time, Deployment Frequency, MTTR, Change Failure Rate.
- **GitOps:** Pull model, state reconciliation, Git as source of truth.

## 2. Practical Scenarios (Situational Questions)

!!! question "Scenario 1: “The pipeline takes 45 minutes, developers complain. What do you do?”"
    **Structured answer:**
    1. **Audit:** I analyze logs to identify the bottleneck (Docker Build? E2E Tests?).
    2. **Cache:** I implement dependency caching (Maven, NPM) and Docker Layer Caching.
    3. **Parallelize:** I split unit, integration and security scans to run concurrently (Fan-out).
    4. **Fail-fast:** I ensure fast checks (lint, SAST) run first.

!!! question "Scenario 2: “A developer pushed a plain-text AWS secret key to GitHub. What is your procedure?”"
    **Structured answer:**
    
    1. **Immediate revocation:** I go to the AWS console and immediately disable/delete the compromised key. (Do not just delete the commit, as bots already have the key).
    2. **Rotation:** I generate new keys and place them in the Secret Manager (Vault, GitHub Secrets).
    3. **Audit:** I check CloudTrail to ensure the compromised key was not used for malicious actions.
    4. **Prevention (Shift-Left):** I add a tool like `trufflehog` or `git-secrets` in pre-commit hooks and in CI to block any future push containing secrets.

!!! question "Scenario 3: “How do you handle CI/CD if you deploy not a web app, but a Big Data pipeline or Machine Learning models?”"
    **Structured answer:**
    The approach remains similar but enriched. For ML (MLOps), instead of just building code, we integrate *Continuous Training* (CT).
    
    1. Training code and data pipelines (e.g., PySpark, Kafka) are versioned.
    2. CI runs tests on data processing with dummy datasets.
    3. The generated artifact is no longer just a Docker image, but also a model versioned in a registry (like MLflow).
    4. Deployment (via Kubernetes/Kubeflow) exposes this model via an API (e.g., FastAPI) using Canary strategies to validate its accuracy in production before switching 100% of traffic.

## 3. Final Checklist

- [x] I can differentiate CI, Delivery (CD) and Deployment (CD).
- [x] I can explain Blue-Green vs Canary.
- [x] I know the difference between Jenkins (On-premise, Controller/Agent) and GitHub Actions (SaaS, Event-driven).
- [x] I know why GitOps (Pull) is more secure than classic CI (Push).
