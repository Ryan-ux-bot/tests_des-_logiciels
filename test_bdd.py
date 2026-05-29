
import unittest
from datetime import date
from systeme_location import SystemeLocation


class TestBDD_Scenarios(unittest.TestCase):
    """
    Tests BDD : décrivent le comportement du système
    du point de vue de l'utilisateur/métier.
    """

    def setUp(self):
        """Initialise un système propre avant chaque scénario."""
        self.systeme = SystemeLocation()

    # ════════════════════════════════════════════════════════
    # SCÉNARIO 1 : Location réussie d'une voiture disponible
    # ════════════════════════════════════════════════════════
    def test_scenario_location_reussie(self):
        """
        SCÉNARIO : Un client loue avec succès une voiture disponible.

        GIVEN  une voiture Renault Clio (TN-010-AA) est dans le système
        AND    la voiture est disponible
        WHEN   le client "Rami Trabelsi" loue cette voiture pour 4 jours
        THEN   la location est créée avec succès
        AND    la voiture n'est plus disponible
        AND    la date de retour prévue est correcte
        """
        # GIVEN
        self.systeme.ajouter_voiture("TN-010-AA", "Renault", "Clio", 80)
        voiture = self.systeme.get_voiture("TN-010-AA")
        self.assertTrue(voiture.disponible, "GIVEN: La voiture doit être disponible")

        # WHEN
        location = self.systeme.louer_voiture(
            "TN-010-AA", "Rami Trabelsi", date(2024, 5, 10), 4
        )

        # THEN
        self.assertIsNotNone(location, "THEN: La location doit être créée")
        self.assertFalse(voiture.disponible, "THEN: La voiture ne doit plus être disponible")
        self.assertEqual(
            location.date_retour_prevue, date(2024, 5, 14),
            "THEN: La date de retour prévue doit être le 14 mai"
        )

    # ════════════════════════════════════════════════════════
    # SCÉNARIO 2 : Tentative de location d'une voiture indisponible
    # ════════════════════════════════════════════════════════
    def test_scenario_location_voiture_indisponible(self):
        """
        SCÉNARIO : Un client ne peut pas louer une voiture déjà louée.

        GIVEN  une voiture (TN-020-BB) est dans le système
        AND    elle est déjà louée par "Client A"
        WHEN   "Client B" tente de louer la même voiture
        THEN   une erreur est levée
        AND    la voiture reste assignée à "Client A"
        """
        # GIVEN
        self.systeme.ajouter_voiture("TN-020-BB", "Peugeot", "208", 90)
        self.systeme.louer_voiture("TN-020-BB", "Client A", date(2024, 5, 1), 3)

        # WHEN & THEN
        with self.assertRaises(ValueError) as contexte:
            self.systeme.louer_voiture("TN-020-BB", "Client B", date(2024, 5, 2), 2)

        self.assertIn("TN-020-BB", str(contexte.exception))

    # ════════════════════════════════════════════════════════
    # SCÉNARIO 3 : Retour sans pénalité
    # ════════════════════════════════════════════════════════
    def test_scenario_retour_a_temps(self):
        """
        SCÉNARIO : Un client retourne la voiture à la date prévue.

        GIVEN  une Volkswagen Golf à 120 DT/jour (TN-030-CC)
        AND    louée pour 5 jours à partir du 1er juin
        WHEN   le client retourne la voiture le 6 juin (date prévue)
        THEN   le coût total est de 600 DT (5 × 120)
        AND    aucune pénalité n'est appliquée
        AND    la voiture redevient disponible
        """
        # GIVEN
        self.systeme.ajouter_voiture("TN-030-CC", "Volkswagen", "Golf", 120)
        self.systeme.louer_voiture("TN-030-CC", "Houda Belhaj", date(2024, 6, 1), 5)

        # WHEN
        cout = self.systeme.retourner_voiture("TN-030-CC", date(2024, 6, 6))

        # THEN
        self.assertEqual(cout["total"], 600, "THEN: Coût total = 5 × 120 = 600 DT")
        self.assertEqual(cout["penalite"], 0, "THEN: Aucune pénalité")
        self.assertEqual(cout["jours_retard"], 0, "THEN: Aucun jour de retard")

        voiture = self.systeme.get_voiture("TN-030-CC")
        self.assertTrue(voiture.disponible, "THEN: Voiture à nouveau disponible")

    # ════════════════════════════════════════════════════════
    # SCÉNARIO 4 : Retour avec pénalité de retard
    # ════════════════════════════════════════════════════════
    def test_scenario_penalite_retard(self):
        """
        SCÉNARIO : Un client rend la voiture 3 jours en retard.

        GIVEN  une voiture Renault Clio à 80 DT/jour
        AND    louée pour 3 jours à partir du 10 juillet
        WHEN   le client retourne la voiture le 16 juillet (3 jours de retard)
        THEN   la durée réelle est de 6 jours
        AND    le coût de base est 6 × 80 = 480 DT
        AND    la pénalité est 3 × 15 = 45 DT
        AND    le total est 525 DT
        """
        # GIVEN
        self.systeme.ajouter_voiture("TN-040-DD", "Renault", "Clio", 80)
        self.systeme.louer_voiture("TN-040-DD", "Nizar Hamdi", date(2024, 7, 10), 3)
        # Date retour prévue = 13 juillet

        # WHEN
        cout = self.systeme.retourner_voiture("TN-040-DD", date(2024, 7, 16))
        # Retard = 16 - 13 = 3 jours

        # THEN
        self.assertEqual(cout["duree_reelle"], 6, "THEN: 6 jours de location effective")
        self.assertEqual(cout["cout_base"], 480, "THEN: 6 × 80 = 480 DT")
        self.assertEqual(cout["jours_retard"], 3, "THEN: 3 jours de retard")
        self.assertEqual(cout["penalite"], 45, "THEN: 3 × 15 = 45 DT")
        self.assertEqual(cout["total"], 525, "THEN: 480 + 45 = 525 DT")

    # ════════════════════════════════════════════════════════
    # SCÉNARIO 5 : Consultation des voitures disponibles
    # ════════════════════════════════════════════════════════
    def test_scenario_consultation_disponibilite(self):
        """
        SCÉNARIO : L'agence consulte ses voitures disponibles.

        GIVEN  3 voitures sont enregistrées dans le système
        AND    2 d'entre elles sont actuellement louées
        WHEN   on consulte la disponibilité
        THEN   seule 1 voiture apparaît comme disponible
        """
        # GIVEN
        self.systeme.ajouter_voiture("TN-A01", "Renault", "Clio", 80)
        self.systeme.ajouter_voiture("TN-A02", "Peugeot", "308", 95)
        self.systeme.ajouter_voiture("TN-A03", "Fiat", "500", 70)

        self.systeme.louer_voiture("TN-A01", "Client 1", date(2024, 8, 1), 5)
        self.systeme.louer_voiture("TN-A02", "Client 2", date(2024, 8, 1), 3)

        # WHEN
        disponibles = self.systeme.consulter_disponibilite()

        # THEN
        self.assertEqual(len(disponibles), 1, "THEN: 1 seule voiture disponible")
        self.assertEqual(disponibles[0].immatriculation, "TN-A03",
                         "THEN: La voiture TN-A03 est disponible")

    # ════════════════════════════════════════════════════════
    # SCÉNARIO 6 : Ajout d'une voiture avec tarif invalide
    # ════════════════════════════════════════════════════════
    def test_scenario_ajout_voiture_invalide(self):
        """
        SCÉNARIO : L'agence tente d'ajouter une voiture avec un tarif invalide.

        GIVEN  le système de location est initialisé
        WHEN   on tente d'ajouter une voiture avec un tarif de -50 DT
        THEN   une ValueError est levée
        AND    la voiture n'est pas ajoutée au système
        """
        # GIVEN
        nb_avant = len(self.systeme.voitures)

        # WHEN & THEN
        with self.assertRaises(ValueError):
            self.systeme.ajouter_voiture("TN-BAD", "Renault", "Kangoo", -50)

        # La voiture ne doit pas être dans le système
        nb_apres = len(self.systeme.voitures)
        self.assertEqual(nb_avant, nb_apres, "THEN: Aucune voiture ajoutée")


# ═══════════════════════════════════════════════════════════
#  POINT D'ENTRÉE POUR THONNY
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("   LANCEMENT DES TESTS BDD")
    print("=" * 60)
    print("  Format : GIVEN / WHEN / THEN")
    print("=" * 60)
    unittest.main(verbosity=2)
