
import unittest
from datetime import date, timedelta
from voiture import Voiture
from location import Location


class TestVoiture(unittest.TestCase):

    def setUp(self):
        """une voiture valide avant chaque test."""
        self.voiture = Voiture("TN-123-AB", "Renault", "Clio", 80)

    # ── Test 1 ───────────────────────────────────────────────
    def test_creation_voiture_valide(self):
        """
        TDD - RED→GREEN :
        Une voiture créée avec des données valides doit avoir
        les bons attributs et être disponible par défaut.
        """
        self.assertEqual(self.voiture.immatriculation, "TN-123-AB")
        self.assertEqual(self.voiture.marque, "Renault")
        self.assertEqual(self.voiture.modele, "Clio")
        self.assertEqual(self.voiture.tarif_journalier, 80)
        self.assertTrue(self.voiture.disponible)  # Disponible par défaut

    # ── Test 2 ───────────────────────────────────────────────
    def test_immatriculation_mise_en_majuscule(self):
        """
        TDD - Normalisation :
        L'immatriculation doit être stockée en majuscules,
        peu importe la casse saisie.
        """
        v = Voiture("tn-456-cd", "Peugeot", "208", 90)
        self.assertEqual(v.immatriculation, "TN-456-CD")

    # ── Test 3 ───────────────────────────────────────────────
    def test_immatriculation_vide_leve_exception(self):
        """
        TDD - Validation :
        Une immatriculation vide doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            Voiture("", "Renault", "Clio", 80)

    # ── Test 4 ───────────────────────────────────────────────
    def test_tarif_negatif_leve_exception(self):
        """
        TDD - Validation :
        Un tarif négatif ou nul doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            Voiture("TN-999-ZZ", "Renault", "Clio", -10)

    # ── Test 5 ───────────────────────────────────────────────
    def test_tarif_zero_leve_exception(self):
        """
        TDD - Validation :
        Un tarif égal à zéro doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            Voiture("TN-999-ZZ", "Renault", "Clio", 0)

    # ── Test 6 ───────────────────────────────────────────────
    def test_str_voiture_disponible(self):
        """
        TDD - Affichage :
        La méthode __str__ doit indiquer "Disponible"
        pour une voiture disponible.
        """
        resultat = str(self.voiture)
        self.assertIn("Disponible", resultat)
        self.assertIn("TN-123-AB", resultat)

    # ── Test 7 ───────────────────────────────────────────────
    def test_str_voiture_louee(self):
        """
        TDD - Affichage :
        La méthode __str__ doit indiquer "Louée"
        quand la voiture n'est plus disponible.
        """
        self.voiture.disponible = False
        resultat = str(self.voiture)
        self.assertIn("Louée", resultat)


# ═══════════════════════════════════════════════════════════
#  TESTS UNITAIRES : LOCATION
# ═══════════════════════════════════════════════════════════

class TestLocation(unittest.TestCase):
    """Tests unitaires pour la classe Location."""

    def setUp(self):
        """Prépare une voiture et une location valide avant chaque test."""
        self.voiture = Voiture("TN-100-XX", "Volkswagen", "Golf", 100)
        self.date_debut = date(2024, 6, 1)
        self.location = Location("Ali Ben Salah", self.voiture, self.date_debut, 5)

    # ── Test 8 ───────────────────────────────────────────────
    def test_creation_location_valide(self):
        """
        TDD - Création :
        Une location valide doit avoir les bons attributs
        et la date de retour prévue calculée correctement.
        """
        self.assertEqual(self.location.client, "Ali Ben Salah")
        self.assertEqual(self.location.voiture, self.voiture)
        self.assertEqual(self.location.duree_prevue, 5)
        self.assertEqual(self.location.date_retour_prevue, date(2024, 6, 6))
        self.assertFalse(self.location.terminee)

    # ── Test 9 ───────────────────────────────────────────────
    def test_cout_sans_retard(self):
        """
        TDD - Calcul du coût :
        Si la voiture est retournée à temps (ou avant),
        il n'y a pas de pénalité.
        Coût attendu = 5 jours × 100 DT = 500 DT.
        """
        date_retour = date(2024, 6, 6)  # Exactement la date prévue
        cout = self.location.calculer_cout(date_retour)

        self.assertEqual(cout["duree_reelle"], 5)
        self.assertEqual(cout["cout_base"], 500)
        self.assertEqual(cout["jours_retard"], 0)
        self.assertEqual(cout["penalite"], 0)
        self.assertEqual(cout["total"], 500)

    # ── Test 10 ──────────────────────────────────────────────
    def test_cout_avec_retard(self):
        """
        TDD - Pénalité de retard :
        Un retard de 3 jours avec pénalité de 15 DT/jour
        doit ajouter 45 DT au coût de base.
        Coût attendu = (5+3)×100 + 3×15 = 800 + 45 = 845 DT.
        """
        date_retour = date(2024, 6, 9)  # 3 jours de retard
        cout = self.location.calculer_cout(date_retour)

        self.assertEqual(cout["duree_reelle"], 8)
        self.assertEqual(cout["cout_base"], 800)
        self.assertEqual(cout["jours_retard"], 3)
        self.assertEqual(cout["penalite"], 45)
        self.assertEqual(cout["total"], 845)

    # ── Test 11 ──────────────────────────────────────────────
    def test_cout_retour_anticipe(self):
        """
        TDD - Retour anticipé :
        Un retour avant la date prévue ne génère pas de pénalité.
        Coût = 3 jours × 100 DT = 300 DT.
        """
        date_retour = date(2024, 6, 4)  # 2 jours avant la date prévue
        cout = self.location.calculer_cout(date_retour)

        self.assertEqual(cout["jours_retard"], 0)
        self.assertEqual(cout["penalite"], 0)
        self.assertEqual(cout["cout_base"], 300)
        self.assertEqual(cout["total"], 300)

    # ── Test 12 ──────────────────────────────────────────────
    def test_duree_nulle_leve_exception(self):
        """
        TDD - Validation :
        Une durée de 0 ou négative doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            Location("Client", self.voiture, self.date_debut, 0)

    # ── Test 13 ──────────────────────────────────────────────
    def test_client_vide_leve_exception(self):
        """
        TDD - Validation :
        Un nom de client vide doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            Location("", self.voiture, self.date_debut, 3)

    # ── Test 14 ──────────────────────────────────────────────
    def test_calcul_cout_sans_date_retour_leve_exception(self):
        """
        TDD - Robustesse :
        Appeler calculer_cout() sans date de retour définie
        doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            self.location.calculer_cout()  # date_retour_reelle est None


# ═══════════════════════════════════════════════════════════
#  POINT D'ENTRÉE POUR THONNY
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("   LANCEMENT DES TESTS UNITAIRES")
    print("=" * 60)
    unittest.main(verbosity=2)
