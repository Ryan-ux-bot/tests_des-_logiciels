# Tests de Logiciels en Java

Travaux pratiques réalisés dans le cadre du module **Tests de Logiciels** (L2CS01).  
Ce dépôt regroupe différents comptes rendus et exemples de code autour des tests unitaires, d’intégration et de l’automatisation en Java.

## 📚 Contenu des TP

### TP1 – Tests unitaires avec JUnit 5
- Création d’un projet Java sous Eclipse
- Classe `Rational` (constructeur, add, equals, toString)
- Tests unitaires avec `assertEquals`
- Gestion du temps d’exécution avec `@Timeout`
- Cycle de vie des tests (`@BeforeAll`, `@BeforeEach`, `@AfterEach`, `@AfterAll`)

### TP2 – Développement piloté par les tests (TDD)
- Classe `Loup` avec orientation initiale NORD
- Ajout progressif des tests (`testPositionInitialeAuNord`, `testTournerUneFois`)
- Implémentation de la méthode `tourner()`
- Refactoring du code avec `Enum Orientation`

### TP3 – Tests automatisés avec JUnit et Spring
- Tests de la couche Service (`ProductService`)
- Initialisation du contexte Spring (manuelle, annotations, Spring Boot)
- Tests DAO avec gestion des transactions
- Utilisation de `@Transactional` et cycle de vie des méthodes

### TP4 – Automatisation avec ChatGPT
- Génération de scripts Selenium (Java + LambdaTest)
- Définition de scénarios Cucumber (positifs et négatifs)
- Implémentation Playwright
- Vérification MySQL et résilience (retry)
- Pipeline CI/CD avec GitHub Actions et secrets sécurisés

### TP5 – Tests d’intégration BDD avec Cucumber-JVM
- Projet Maven sous IntelliJ IDEA
- Dépendances JUnit et Cucumber
- Fichier `.feature` en Gherkin (FizzBuzz)
- Implémentation des Step Definitions (`ExampleSteps.java`)
- Exécution via `CukesRunner` : tous les tests passent

## 🛠️ Technologies utilisées
- **Java 8 / 11**
- **JUnit 4 / JUnit 5**
- **Spring Framework / Spring Boot**
- **Maven**
- **Cucumber-JVM (BDD)**
- **Selenium / Playwright**
- **GitHub Actions (CI/CD)**

## 👨‍🎓 Auteur
- **Rayen Bouyahia** – Classe L2CS01  
Université de Tunis El Manar

---

⚡ Ce dépôt illustre la progression des TP : **Unit Tests → TDD → Spring → Automatisation → BDD**.
