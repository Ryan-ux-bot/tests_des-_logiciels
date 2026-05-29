# Tests de Logiciels – Travaux Pratiques & Projet

Ce dépôt regroupe l’ensemble des **TPs** et du **rapport de projet** réalisés dans le cadre du module *Tests de Logiciels* (Licence Informatique – L2CS01, Université de Tunis El Manar).

---

## Contenu

###  TP1 – Tests unitaires avec JUnit 5
- Classe `Rational` (constructeur, add, equals, toString)
- Tests unitaires avec `assertEquals`
- Gestion du temps d’exécution avec `@Timeout`
- Cycle de vie des tests (`@BeforeAll`, `@BeforeEach`, `@AfterEach`, `@AfterAll`)

###  TP2 – Développement piloté par les tests (TDD)
- Classe `Loup` avec orientation initiale NORD
- Ajout progressif des tests (`testPositionInitialeAuNord`, `testTournerUneFois`)
- Implémentation de la méthode `tourner()`
- Refactoring avec `Enum Orientation`

###  TP3 – Tests automatisés avec JUnit et Spring
- Tests de la couche Service (`ProductService`)
- Initialisation du contexte Spring (manuelle, annotations, Spring Boot)
- Tests DAO avec gestion des transactions
- Utilisation de `@Transactional` et cycle de vie des méthodes

###  TP4 – Automatisation avec ChatGPT
- Génération de scripts Selenium (Java + LambdaTest)
- Définition de scénarios Cucumber (positifs et négatifs)
- Implémentation Playwright
- Vérification MySQL et résilience (retry)
- Pipeline CI/CD avec GitHub Actions et secrets sécurisés

###  TP5 – Tests d’intégration BDD avec Cucumber-JVM
- Projet Maven sous IntelliJ IDEA
- Dépendances JUnit et Cucumber
- Fichier `.feature` en Gherkin (FizzBuzz)
- Implémentation des Step Definitions (`ExampleSteps.java`)
- Exécution via `CukesRunner` : tous les tests passent

###  Rapport de Projet – Système de Gestion de Location de Voitures
- Développement en **Python** avec approche TDD
- Architecture : `Voiture`, `Location`, `SystemeLocation`
- Stratégie de tests pyramidale :
  - 14 tests unitaires
  - 10 tests d’intégration
  - 6 scénarios BDD
- Runner global : **30 tests réussis (100 %)**  
- Cas d’erreur validés : immatriculation vide, tarif ≤ 0, voiture indisponible, retour sans location active…

---

##  Technologies utilisées
- **Java 8 / 11**
- **JUnit 4 / JUnit 5**
- **Spring Framework / Spring Boot**
- **Maven**
- **Cucumber-JVM (BDD)**
- **Selenium / Playwright**
- **Python 3.10+**
- **GitHub Actions (CI/CD)**

---

##  Auteur
- **Rayen Bouyahia** – Classe L2CS01  
Institut Supérieur d'Informatique Ariana
---

 Ce dépôt illustre la progression complète :  
**Unit Tests → TDD → Spring → Automatisation → BDD → Projet Python validé par 30/30 tests.**

