# Observability and Monitoring: From Zero to Production

In DevOps / SRE interview, observability is the subject where recruiters immediately check if you have real field experience or only theoretical knowledge. The classic trick question: *"What is the difference between monitoring a server with Nagios and making a Kubernetes cluster observable?"*.

This course is designed to give you practical weapons, flow architecture, real queries and incident response reflexes.

---

## 1. From Binary Monitoring to Modern Observability

Traditional monitoring checks the external state (*Black-box*), while observability reconstructs the complete internal state (*White-box*) from the signals emitted.

```mermaid
flowchart TD
    subgraph Monitoring["Monitoring Traditionnel (Silos)"]
        M1["Check Ping / Port 80"] --> S1["Up / Down"]
        M2["CPU > 85%"] --> S2["Alerte Statique"]
    end

    subgraph Observabilite["Observabilité Unifiée (M.E.L.T)"]
        direction TB
        K8s["Cluster K8s / Cloud"] --> Metrics["Metrics (Prometheus)"]
        K8s --> Events["Events (Kubelet / API)"]
        K8s --> Logs["Logs Structurés (Loki / CW)"]
        K8s --> Traces["Traces Distribuées (OpenTelemetry)"]
        
        Metrics & Events & Logs & Traces ==> Engine["Corrélation & Root Cause Analysis"]
    end
```

!!! danger "The Trap of Traditional Monitoring"
    A container can respond `HTTP 200` on its health check route while having a saturated SQL connection pool and 90% of its business requests blocked. A simple ping is blind to distributed micro-failures.

---

## 2. Global Architecture of Flows in Production

Here is the standard telemetry pipeline deployed in an enterprise on a managed Kubernetes (EKS) cluster:

```mermaid
flowchart LR
    subgraph Cluster["Cluster Kubernetes / EKS"]
        App["Pod Applicatif (Spring / Node)"]
        NodeExp["Node Exporter"]
        KubeState["Kube-State-Metrics"]
    end

    subgraph Collector["Ingestion & Scraping"]
        Prom["Prometheus Server (Pull)"]
        OTel["OTel Collector (Push / Pull)"]
    end

    subgraph Backends["Stockage & Analyse"]
        AlertM["Alertmanager"]
        Grafana["Grafana Dashboards"]
        Jaeger["Tempo / Jaeger (Traces)"]
    end

    App -.->|"Expose /metrics"| Prom
    NodeExp -.->|"Scrape hardware"| Prom
    KubeState -.->|"Scrape états k8s"| Prom
    App ==>|"Spans OTLP (gRPC)"| OTel
    OTel --> Jaeger

    Prom -->|"Évalue les règles"| AlertM
    Prom -->|"Requêtes PromQL"| Grafana
    AlertM ==>|"Webhook / PagerDuty / Slack"| OnCall["Ingénieur d'Astreinte (On-Call)"]
```

---

## 3. MkDocs Curriculum

| Module | File | Operational Objective |
|---|---|---|
| **01** | `01-fondamentaux-theorie.md` | Master M.E.L.T, the 4 Golden Signals and the calculation of an Error Budget (SLI/SLO/SLA). |
| **02** | `02-methodes-use-red.md` | Know which framework to apply: USE (infra resources) vs RED (microservices). |
| **03** | `03-prometheus-architecture.md` | Understand the Pull model, internal TSDB and Kubernetes Service Discovery. |
| **04** | `04-prometheus-metriques.md` | Know how to instrument your code with Counter, Gauge, Histogram and Summary. |
| **05** | `05-promql-mastery.md` | Write complex queries: `rate()`, `histogram_quantile()` and vector joins. |
| **06** | `06-alertmanager.md` | Configure routing, cascading alert inhibition, and silences. |
| **07** | `07-grafana-dashboards.md` | Build efficient dashboards with dynamic variables and unified alerts. |
| **08** | `08-opentelemetry.md` | Deploy the OTel Collector, propagate W3C contexts and track distributed requests. |
| **09** | `09-aws-cloudwatch.md` | Leverage CloudWatch Logs Insights, Container Insights, and composite alarms. |
| **10** | `10-k8s-diagnostics.md` | Live diagnose CrashLoopBackOff, OOMKilled (Exit Code 137) and CPU Throttling. |
| **11** | `11-triage-incidents-prod.md` | Isolate 502/503/504 errors and calculate P95/P99 latencies without getting trapped by averages. |
| **12** | `12-cheatsheet-entretien.md` | Ultra-fast summary of elimination questions and crisis scenarios in interviews. |

!!! tip "Revision Method"
    Each course ends with **Real Interview Questions**. Practice the answer out loud using the precise technical terms (eg: *CFS quota*, *percentile*, *W3C traceparent*).

# Monitoring & Observabilité sur AWS EKS : schémas complets

Cinq vues complémentaires : concepts, architecture cible, flux de données par signal, gestion d'un incident, et plan d'adoption.

---

## 1. Monitoring vs Observabilité

```mermaid
flowchart TB
  subgraph MON["MONITORING : le QUOI et le QUAND"]
    direction TB
    M1["Questions connues<br/>known unknowns"]
    M2["Dashboards + seuils prédéfinis<br/>CPU, mémoire, 5xx, CrashLoopBackOff"]
    M3["Alerte : un problème existe"]
    M1 --> M2 --> M3
  end

  subgraph OBS["OBSERVABILITÉ : le POURQUOI et le COMMENT"]
    direction TB
    O1["Questions inconnues<br/>unknown unknowns"]
    O2["Données riches et corrélables<br/>filtrage par version, client, endpoint"]
    O3["Cause racine identifiée"]
    O1 --> O2 --> O3
  end

  subgraph PIL["Les 3 piliers"]
    direction TB
    P1["Métriques<br/>Combien ? À quel rythme ?<br/>Prometheus, CloudWatch"]
    P2["Logs structurés<br/>Que s'est-il passé ?<br/>Fluent Bit, Loki, OpenSearch"]
    P3["Traces distribuées<br/>Où est passé le temps ?<br/>OpenTelemetry, Tempo, X-Ray"]
  end

  PIL ==>|"alimente"| OBS
  PIL ==>|"alimente"| MON
  MON -->|"déclenche l'investigation"| OBS

  classDef mon fill:#FFF3CD,stroke:#B8860B,color:#4a3800
  classDef obs fill:#D1ECF1,stroke:#0C5460,color:#06303a
  classDef pil fill:#E2D9F3,stroke:#5B3FA0,color:#2b1d54
  class M1,M2,M3 mon
  class O1,O2,O3 obs
  class P1,P2,P3 pil
```

---

## 2. Architecture cible sur EKS (vue d'ensemble)

```mermaid
flowchart LR
  USER(["Utilisateurs"]) --> ALB

  subgraph AWS["AWS Cloud"]
    subgraph VPC["VPC"]
      ALB["ALB / Ingress Controller"]

      subgraph EKS["Cluster EKS"]
        subgraph APPNS["Namespace applicatif"]
          API["api-backend<br/>SDK OTel, /metrics, logs JSON"]
          PAY["payments"]
          AUTH["auth"]
        end

        subgraph MONNS["Namespace monitoring"]
          PROM["Prometheus<br/>ServiceMonitor, PodMonitor"]
          RULES["PrometheusRule<br/>alertes + SLO"]
          AM["Alertmanager"]
          KSM["kube-state-metrics"]
          NE["node-exporter<br/>DaemonSet"]
          FB["Fluent Bit<br/>DaemonSet"]
          OTEL["OTel Collector<br/>ou ADOT"]
          GRAF["Grafana<br/>dashboards + Explore"]
        end
      end
    end

    subgraph AWSMGD["Services AWS de stockage"]
      AMP[("Amazon Managed<br/>Prometheus")]
      AMG["Amazon Managed<br/>Grafana"]
      CWL[("CloudWatch Logs")]
      XRAY[("AWS X-Ray")]
      OS[("OpenSearch")]
    end

    IAM["IAM : IRSA ou<br/>EKS Pod Identity"]
  end

  subgraph OSS["Backends open source"]
    LOKI[("Loki")]
    TEMPO[("Tempo / Jaeger")]
  end

  NOTIF(["Slack, PagerDuty, email"])

  ALB --> API
  API --> PAY
  API --> AUTH

  PROM -->|"scrape /metrics"| API
  PROM -->|"scrape"| PAY
  PROM -->|"scrape"| AUTH
  PROM -->|"scrape"| KSM
  PROM -->|"scrape"| NE
  RULES -.->|"évaluées par"| PROM
  PROM -->|"alertes"| AM
  AM --> NOTIF
  PROM -->|"remote_write"| AMP

  API -.->|"stdout JSON"| FB
  FB --> LOKI
  FB --> CWL
  FB --> OS

  API -->|"OTLP :4317"| OTEL
  PAY -->|"OTLP"| OTEL
  AUTH -->|"OTLP"| OTEL
  OTEL --> TEMPO
  OTEL --> XRAY
  OTEL -.->|"spanmetrics"| PROM

  GRAF -->|"PromQL"| PROM
  GRAF -->|"PromQL"| AMP
  GRAF -->|"LogQL"| LOKI
  GRAF --> TEMPO
  AMG -->|"PromQL"| AMP
  AMG --> CWL
  AMG --> XRAY

  IAM -.->|"autorise"| PROM
  IAM -.->|"autorise"| FB
  IAM -.->|"autorise"| OTEL

  classDef app fill:#D4EDDA,stroke:#1E7E34,color:#0b3d17
  classDef mon fill:#FFF3CD,stroke:#B8860B,color:#4a3800
  classDef aws fill:#FFE5D0,stroke:#C8641E,color:#5a2a05
  classDef oss fill:#D1ECF1,stroke:#0C5460,color:#06303a
  classDef sec fill:#F8D7DA,stroke:#A71D2A,color:#4d0d13
  class API,PAY,AUTH app
  class PROM,RULES,AM,KSM,NE,FB,OTEL,GRAF mon
  class AMP,AMG,CWL,XRAY,OS aws
  class LOKI,TEMPO oss
  class IAM sec
```

---

## 3. Flux de données par signal et corrélation

```mermaid
flowchart TB
  subgraph SRC["Source : pod applicatif"]
    CODE["Code instrumenté<br/>OpenTelemetry SDK"]
    ENDP["Endpoint /metrics"]
    STDOUT["stdout / stderr<br/>logs JSON avec trace_id"]
    SPANS["Spans OTLP"]
    CODE --> ENDP
    CODE --> STDOUT
    CODE --> SPANS
  end

  subgraph COL["Collecte"]
    PROM["Prometheus<br/>pull toutes les 30 s"]
    FB["Fluent Bit<br/>enrichit : pod, namespace, labels"]
    OTEL["OTel Collector<br/>batch, sampling, export"]
  end

  subgraph STO["Stockage"]
    MET[("Métriques<br/>TSDB ou AMP")]
    LOG[("Logs<br/>Loki, CloudWatch, OpenSearch")]
    TRA[("Traces<br/>Tempo, Jaeger, X-Ray")]
  end

  subgraph EXP["Exploitation dans Grafana"]
    DASH["Dashboards SLI / SLO"]
    ALRT["Alertes"]
    EXPL["Explore : investigation"]
  end

  ENDP --> PROM --> MET
  STDOUT --> FB --> LOG
  SPANS --> OTEL --> TRA

  MET --> DASH
  MET --> ALRT
  MET -.->|"exemplars"| TRA
  TRA -.->|"trace_id"| LOG
  LOG -.->|"derived fields"| TRA
  DASH --> EXPL
  TRA --> EXPL
  LOG --> EXPL

  classDef src fill:#D4EDDA,stroke:#1E7E34,color:#0b3d17
  classDef col fill:#FFF3CD,stroke:#B8860B,color:#4a3800
  classDef sto fill:#E2D9F3,stroke:#5B3FA0,color:#2b1d54
  classDef exp fill:#D1ECF1,stroke:#0C5460,color:#06303a
  class CODE,ENDP,STDOUT,SPANS src
  class PROM,FB,OTEL col
  class MET,LOG,TRA sto
  class DASH,ALRT,EXPL exp
```

---

## 4. Gestion d'un incident : de l'alerte à la cause racine

```mermaid
sequenceDiagram
  autonumber
  actor SRE as Ingénieur on-call
  participant AM as Alertmanager
  participant PROM as Prometheus
  participant GRAF as Grafana
  participant TEMPO as Tempo / X-Ray
  participant LOKI as Loki / CloudWatch Logs
  participant K8S as Cluster EKS

  Note over PROM: MONITORING
  PROM->>PROM: Évalue HighErrorRate toutes les 1 min
  PROM->>AM: Alerte firing : 5xx supérieur à 2 % pendant 5 min
  AM->>SRE: Notification Slack + PagerDuty

  Note over SRE,LOKI: OBSERVABILITÉ
  SRE->>GRAF: Ouvre le dashboard api-backend
  GRAF->>PROM: sum by (status, version)(rate(http_requests_total[5m]))
  PROM-->>GRAF: Pic de 504, uniquement version v2.3
  SRE->>GRAF: Clique sur un exemplar de latence
  GRAF->>TEMPO: Récupère la trace par trace_id
  TEMPO-->>GRAF: 800 ms dans le service payments, appel API externe
  SRE->>GRAF: Pivot trace vers logs
  GRAF->>LOKI: Requête par trace_id
  LOKI-->>GRAF: Timeout vers fournisseur de paiement externe

  Note over SRE,K8S: RÉSOLUTION
  SRE->>K8S: Rollback vers v2.2 ou ajustement des timeouts
  PROM->>AM: Alerte resolved
  AM->>SRE: Notification de résolution
  SRE->>SRE: Post-mortem et nouvelle alerte ciblée
```

---

## 5. Choix de l'approche et plan d'adoption

```mermaid
flowchart TB
  START(["Mise en place de l'observabilité sur EKS"]) --> Q1{"Équipe pour opérer<br/>la stack ?"}
  Q1 -->|"Oui, portabilité souhaitée"| OSS["Open source<br/>kube-prometheus-stack, Loki, Tempo, OTel"]
  Q1 -->|"Non, peu de ressources"| NAT["AWS-native<br/>Container Insights, CloudWatch Logs, X-Ray"]
  Q1 -->|"Compromis"| HYB["Hybride<br/>Prometheus + AMP + Amazon Managed Grafana + ADOT"]

  OSS --> P1
  NAT --> P1
  HYB --> P1

  subgraph PLAN["Plan d'adoption progressif"]
    direction TB
    P1["Phase 1 : Monitoring de base<br/>kube-prometheus-stack, alertes infra"]
    P2["Phase 2 : Métriques applicatives<br/>/metrics, SLI / SLO, alertes sur symptômes"]
    P3["Phase 3 : Logs centralisés<br/>JSON structuré, Fluent Bit, trace_id"]
    P4["Phase 4 : Tracing distribué<br/>OpenTelemetry, Collector, sampling"]
    P5["Phase 5 : Corrélation<br/>exemplars, derived fields, runbooks"]
    P1 --> P2 --> P3 --> P4 --> P5
  end

  P5 --> DONE(["Observabilité complète"])

  subgraph PIEGES["Pièges à éviter"]
    direction TB
    X1["Cardinalité : pas de user_id ou request_id en label"]
    X2["Alert fatigue : alerter sur ce qui exige une action"]
    X3["Coûts : sampling 5 à 10 %, 100 % des erreurs, rétention fixée"]
    X4["Rétention : AMP, Thanos ou Mimir pour le long terme"]
  end

  P2 -.-> X1
  P2 -.-> X2
  P4 -.-> X3
  P1 -.-> X4

  classDef choice fill:#FFF3CD,stroke:#B8860B,color:#4a3800
  classDef ok fill:#D4EDDA,stroke:#1E7E34,color:#0b3d17
  classDef warn fill:#F8D7DA,stroke:#A71D2A,color:#4d0d13
  classDef aws fill:#FFE5D0,stroke:#C8641E,color:#5a2a05
  class Q1 choice
  class OSS,HYB,P1,P2,P3,P4,P5 ok
  class NAT aws
  class X1,X2,X3,X4 warn
```