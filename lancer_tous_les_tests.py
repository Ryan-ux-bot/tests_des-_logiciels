import unittest
import sys

from test_unitaires import TestVoiture, TestLocation
from test_integration import TestSystemeLocation
from test_bdd import TestBDD_Scenarios


def lancer_tous_les_tests():
    """Lance l'ensemble des suites de tests avec un rapport détaillé."""

    print("\n" + "█" * 60)
    print("   RAPPORT COMPLET DES TESTS")
    print("   Système de Gestion de Location de Voitures")
    print("█" * 60)

    # Construction de la suite globale
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Ajout de chaque groupe de tests
    groupes = [
        ("Tests Unitaires - Voiture",    TestVoiture),
        ("Tests Unitaires - Location",   TestLocation),
        ("Tests d'Intégration",          TestSystemeLocation),
        ("Tests BDD (Gherkin-style)",    TestBDD_Scenarios),
    ]

    total_attendu = 0
    for nom, classe in groupes:
        tests = loader.loadTestsFromTestCase(classe)
        nb = tests.countTestCases()
        total_attendu += nb
        print(f"\n  + {nom} ({nb} tests)")
        suite.addTests(tests)

    print(f"\n  TOTAL : {total_attendu} tests à exécuter")
    print("─" * 60)

    # Exécution
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True
    )
    resultat = runner.run(suite)

    # Rapport final
    print("\n" + "═" * 60)
    print("  BILAN FINAL")
    print("═" * 60)
    print(f"  Tests exécutés : {resultat.testsRun}")
    print(f"  Réussis        : {resultat.testsRun - len(resultat.failures) - len(resultat.errors)}")
    print(f"  Échecs         : {len(resultat.failures)}")
    print(f"  Erreurs        : {len(resultat.errors)}")

    if resultat.wasSuccessful():
        print("\n  ✅  TOUS LES TESTS SONT PASSÉS !")
    else:
        print("\n  ❌  CERTAINS TESTS ONT ÉCHOUÉ.")
        if resultat.failures:
            print("\n  Détail des échecs :")
            for test, trace in resultat.failures:
                print(f"    - {test}")
        if resultat.errors:
            print("\n  Détail des erreurs :")
            for test, trace in resultat.errors:
                print(f"    - {test}")

    print("═" * 60)
    return resultat.wasSuccessful()


if __name__ == "__main__":
    succes = lancer_tous_les_tests()
    sys.exit(0 if succes else 1)
