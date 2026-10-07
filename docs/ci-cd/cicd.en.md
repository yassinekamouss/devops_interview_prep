# CI/CD Overview

Continuous Integration (CI) and Continuous Deployment/Delivery (CD) form the backbone of DevOps culture. In cloud-native environments and distributed architectures, CI/CD transforms source code into value delivered to end users quickly, securely, and repeatably.

## Why CI/CD? (Business and Technical Stakes)
In the context of major software vendors or large-scale cloud infrastructures, manual release cycles are no longer viable. The goals are to:
- **Reduce Time-to-Market:** Deliver features faster.
- **Minimize risk (Fail Fast):** Detect errors as early as the commit thanks to short feedback loops.
- **Eliminate "Works on my machine":** Standardize builds in isolated environments (usually containerized).
- **Secure the software supply chain:** Integrate security testing as early as possible in the code lifecycle (Shift-Left approach).

## DORA Metrics: Measuring CI/CD Performance
In a DevOps technical interview, citing the DORA metrics (DevOps Research and Assessment) shows strategic vision and an understanding of infrastructure's business impact:
1. **Deployment Frequency:** How often is code deployed to production?
2. **Lead Time for Changes:** How long between a developer's commit and its execution in production?
3. **Mean Time to Recovery (MTTR):** How long does it take to restore service after a production failure?
4. **Change Failure Rate:** What percentage of production deployments cause an outage requiring immediate remediation (rollback, hotfix)?

A mature and robust CI/CD pipeline is the primary tool for optimizing these four metrics.
