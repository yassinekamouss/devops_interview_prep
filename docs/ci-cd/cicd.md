# Vue d'ensemble du CI/CD

L'Intégration Continue (CI) et le Déploiement/Livraison Continu (CD) constituent l'épine dorsale de la culture DevOps. Dans des environnements cloud-native et des architectures distribuées, le CI/CD permet de transformer le code source en valeur livrée aux utilisateurs finaux de manière rapide, sécurisée et répétable.

## Pourquoi le CI/CD ? (L'enjeu Business et Technique)
Dans le contexte d'éditeurs logiciels majeurs ou d'infrastructures cloud à grande échelle, les cycles de release manuels ne sont plus viables. L'objectif est de :
- **Réduire le Time-to-Market :** Livrer des fonctionnalités plus rapidement.
- **Minimiser le risque (Fail Fast) :** Détecter les erreurs dès le commit grâce à des boucles de feedback courtes.
- **Éliminer le "Works on my machine" :** Standardiser les builds dans des environnements isolés (généralement conteneurisés).
- **Sécuriser la chaîne logicielle :** Intégrer les tests de sécurité au plus tôt dans le cycle de vie du code (approche Shift-Left).

## Les Métriques DORA : Mesurer la performance CI/CD
Lors d'un entretien technique DevOps, citer les métriques DORA (DevOps Research and Assessment) démontre une vision stratégique et une compréhension de l'impact métier de l'infrastructure :
1. **Deployment Frequency (Fréquence de déploiement) :** À quelle fréquence le code est-il déployé en production ?
2. **Lead Time for Changes (Délai de mise en œuvre) :** Combien de temps s'écoule-t-il entre le commit d'un développeur et son exécution en production ?
3. **Mean Time to Recovery (MTTR) :** Combien de temps faut-il pour restaurer le service après une défaillance en production ?
4. **Change Failure Rate (Taux d'échec des changements) :** Quel pourcentage des déploiements en production provoque une panne nécessitant une correction immédiate (rollback, hotfix) ?

Un pipeline CI/CD mature et robuste est l'outil principal pour optimiser ces quatre métriques.