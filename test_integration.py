

import unittest
from datetime import date
from systeme_location import SystemeLocation




class TestSystemeLocation(unittest.TestCase):


    def setUp(self):
        """
        Prépare un système propre avec 3 voitures avant chaque test.
        """
        self.systeme = SystemeLocation()
        self.systeme.ajouter_voiture("TN-001-AA", "Renault", "Clio", 80)
        self.systeme.ajouter_voiture("TN-002-BB", "Peugeot", "208", 90)
        self.systeme.ajouter_voiture("TN-003-CC", "Volkswagen", "Golf", 120)

    # ── Test 1 ───────────────────────────────────────────────
    def test_ajout_voiture_et_consultation(self):
        """
        Intégration - Ajout + Consultation :
        Après ajout de 3 voitures, toutes doivent apparaître
        comme disponibles dans la consultation.
        """
        disponibles = self.systeme.consulter_disponibilite()
        self.assertEqual(len(disponibles), 3)

    # ── Test 2 ───────────────────────────────────────────────
    def test_ajout_voiture_dupliquee_leve_exception(self):
        """
        Intégration - Unicité :
        Ajouter deux fois la même immatriculation doit lever ValueError.
        """
        with self.assertRaises(ValueError):
            self.systeme.ajouter_voiture("TN-001-AA", "Toyota", "Yaris", 75)

    # ── Test 3 ───────────────────────────────────────────────
    def test_location_reduit_disponibilites(self):
        """
        Intégration - Location + Disponibilité :
        Après location d'une voiture, la disponibilité passe de 3 à 2.
        La voiture louée ne doit plus apparaître dans la liste.
        """
        self.systeme.louer_voiture("TN-001-AA", "Mohamed Ali",
                                    date(2024, 7, 1), 3)

        disponibles = self.systeme.consulter_disponibilite()
        self.assertEqual(len(disponibles), 2)

        immatriculees = [v.immatriculation for v in disponibles]
        self.assertNotIn("TN-001-AA", immatriculees)

    # ── Test 4 ───────────────────────────────────────────────
    def test_location_voiture_indisponible_leve_exception(self):
        """
        Intégration - Disponibilité :
        Louer une voiture déjà louée doit lever une ValueError.
        """
        self.systeme.louer_voiture("TN-002-BB", "Client 1",
                                    date(2024, 7, 1), 3)

        with self.assertRaises(ValueError):
            self.systeme.louer_voiture("TN-002-BB", "Client 2",
                                        date(2024, 7, 2), 2)

    # ── Test 5 ───────────────────────────────────────────────
    def test_location_voiture_inexistante_leve_exception(self):
        """
        Intégration - Robustesse :
        Louer une voiture qui n'existe pas doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            self.systeme.louer_voiture("XX-999-ZZ", "Client",
                                        date(2024, 7, 1), 5)

    # ── Test 6 ───────────────────────────────────────────────
    def test_retour_voiture_sans_retard(self):
        """
        Intégration - Location + Retour à temps :
        Après retour à la date prévue, la voiture redevient disponible
        et le coût total est correct (sans pénalité).
        Voiture à 80 DT/j pendant 3 jours = 240 DT.
        """
        self.systeme.louer_voiture("TN-001-AA", "Sami Karoui",
                                    date(2024, 8, 1), 3)

        cout = self.systeme.retourner_voiture("TN-001-AA", date(2024, 8, 4))

        # Coût sans pénalité
        self.assertEqual(cout["total"], 240)
        self.assertEqual(cout["penalite"], 0)
        self.assertEqual(cout["jours_retard"], 0)

        # La voiture est à nouveau disponible
        voiture = self.systeme.get_voiture("TN-001-AA")
        self.assertTrue(voiture.disponible)

    # ── Test 7 ───────────────────────────────────────────────
    def test_retour_voiture_avec_retard(self):
        """
        Intégration - Pénalité de retard :
        Retard de 2 jours avec pénalité de 15 DT/jour.
        Coût base = (5+2) × 90 = 630 DT.
        Pénalité  = 2 × 15 = 30 DT.
        Total     = 660 DT.
        """
        self.systeme.louer_voiture("TN-002-BB", "Leila Mansouri",
                                    date(2024, 9, 1), 5)

        cout = self.systeme.retourner_voiture("TN-002-BB", date(2024, 9, 8))

        self.assertEqual(cout["jours_retard"], 2)
        self.assertEqual(cout["penalite"], 30)
        self.assertEqual(cout["cout_base"], 630)
        self.assertEqual(cout["total"], 660)

    # ── Test 8 ───────────────────────────────────────────────
    def test_retour_sans_location_active_leve_exception(self):
        """
        Intégration - Robustesse :
        Retourner une voiture qui n'a pas de location active
        doit lever une ValueError.
        """
        with self.assertRaises(ValueError):
            self.systeme.retourner_voiture("TN-003-CC", date(2024, 7, 10))

    # ── Test 9 ───────────────────────────────────────────────
    def test_flux_complet_location_retour_relocation(self):
        """
        Intégration - Scénario complet :
        Une voiture peut être louée, retournée,
        puis louée à nouveau par un autre client.
        Vérifie le cycle de vie complet d'une voiture.
        """
        # 1ère location
        self.systeme.louer_voiture("TN-001-AA", "Client A",
                                    date(2024, 10, 1), 3)
        self.assertEqual(len(self.systeme.consulter_disponibilite()), 2)

        # Retour de la 1ère location
        self.systeme.retourner_voiture("TN-001-AA", date(2024, 10, 4))
        self.assertEqual(len(self.systeme.consulter_disponibilite()), 3)

        # 2ème location de la même voiture
        self.systeme.louer_voiture("TN-001-AA", "Client B",
                                    date(2024, 10, 5), 7)
        self.assertEqual(len(self.systeme.consulter_disponibilite()), 2)

        # Vérifier que 2 locations sont enregistrées dans l'historique
        self.assertEqual(len(self.systeme.locations), 2)

    # ── Test 10 ──────────────────────────────────────────────
    def test_plusieurs_locations_simultanees(self):
        """
        Intégration - Concurrence :
        Plusieurs clients peuvent louer simultanément des voitures différentes.
        """
        self.systeme.louer_voiture("TN-001-AA", "Client 1", date(2024, 11, 1), 2)
        self.systeme.louer_voiture("TN-002-BB", "Client 2", date(2024, 11, 1), 4)

        disponibles = self.systeme.consulter_disponibilite()
        self.assertEqual(len(disponibles), 1)
        self.assertEqual(disponibles[0].immatriculation, "TN-003-CC")


# ═══════════════════════════════════════════════════════════
#  POINT D'ENTRÉE POUR THONNY
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("   LANCEMENT DES TESTS D'INTÉGRATION")
    print("=" * 60)
    unittest.main(verbosity=2)
