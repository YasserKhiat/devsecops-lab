Date : 26 Décembre 2025 Sujet : Mise en place d'un pipeline CI/CD sécurisé avec GitHub Actions et Docker.

1. Objectif de l'atelier
L'objectif principal était de comprendre comment passer d'une approche DevOps classique à une approche DevSecOps. Concrètement, il s'agissait d'automatiser les contrôles de sécurité directement dans le processus de développement, pour qu'ils soient continus et non plus effectués uniquement à la fin du projet .

Nous avons cherché à appliquer le principe du "Shift-Left" : détecter les failles le plus tôt possible (à gauche du cycle de vie) pour réduire les coûts et les risques .

2. Environnement Technique
Pour réaliser cette automatisation, nous avons construit une chaîne d'outils ("Toolchain") intégrée dans GitHub Actions :


L'Application Cible : Une API Python (Flask) volontairement vulnérable.

Analyse du Code (SAST) :


CodeQL : Pour une analyse profonde de la logique du code.


Bandit : Spécifique au langage Python, pour repérer des erreurs comme les eval() ou les secrets en dur.

Sécurité du Conteneur :


Docker : Pour conteneuriser l'application.


Trivy : Pour scanner l'image Docker et détecter les vulnérabilités du système d'exploitation (CVE).

3. Déroulement et Analyse
Phase 1 : Déploiement d'un code vulnérable (Test de détection)
Dans un premier temps, nous avons poussé sur le dépôt un code comportant des failles critiques classiques (OWASP Top 10), notamment :

Une Injection SQL dans la fonction de login.

Une clé secrète (SECRET_KEY) écrite en clair dans le code.

L'utilisation d'une image Docker de base trop lourde et obsolète.

Résultat observé : Le pipeline CI/CD a échoué (rouge). Explication : Les outils CodeQL et Bandit ont bloqué le processus de build en identifiant les lignes de code dangereuses. Trivy a identifié des failles "CRITICAL" dans l'image Docker. Cela prouve l'efficacité du blocage automatique.

Phase 2 : Remédiation et Sécurisation
Pour valider le pipeline, nous avons dû corriger le code en appliquant des correctifs de sécurité :


Correction de l'Injection SQL : Nous avons remplacé la construction dynamique de la requête SQL (f-strings) par des requêtes paramétrées, empêchant l'interprétation de commandes malveillantes.


Gestion des Secrets : La clé secrète a été retirée du code source et est désormais récupérée via une variable d'environnement (os.environ).

Optimisation Docker : Nous avons modifié le Dockerfile pour utiliser une image de base "Slim" (ex: python:3.9-slim). Cela réduit la surface d'attaque en limitant le nombre de composants inutiles installés dans le conteneur.

Résultat final : Après ces corrections, le pipeline est passé au vert ("Passed"). L'image Docker a été construite et validée saine.

4. Conclusion
Cet atelier a démontré que la sécurité ne doit pas être un frein, mais une partie intégrante de la qualité du code. L'automatisation via le pipeline permet aux développeurs de recevoir un feedback immédiat sur la sécurité de leur code, garantissant ainsi que seule une application "propre" peut être déployée en production.
