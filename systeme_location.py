
from datetime import date
from voiture import Voiture
from location import Location


class SystemeLocation:

    def __init__(self):
        self.voitures = {}       # immatriculation -> Voiture
        self.locations = []      # liste de toutes les locations


    def ajouter_voiture(self, immatriculation, marque, modele, tarif_journalier):

        immat = immatriculation.strip().upper()
        if immat in self.voitures:
            raise ValueError(f"Une voiture avec l'immatriculation {immat} existe déjà.")

        voiture = Voiture(immatriculation, marque, modele, tarif_journalier)
        self.voitures[voiture.immatriculation] = voiture
        return voiture

    def consulter_disponibilite(self):

        return [v for v in self.voitures.values() if v.disponible]

    def get_voiture(self, immatriculation):

        return self.voitures.get(immatriculation.strip().upper())


    def louer_voiture(self, immatriculation, client, date_debut, duree_jours):

        voiture = self.get_voiture(immatriculation)
        if voiture is None:
            raise ValueError(f"Voiture {immatriculation} introuvable.")
        if not voiture.disponible:
            raise ValueError(f"La voiture {immatriculation} n'est pas disponible.")

        location = Location(client, voiture, date_debut, duree_jours)
        voiture.disponible = False
        self.locations.append(location)
        return location



    def retourner_voiture(self, immatriculation, date_retour_reelle):

        immat = immatriculation.strip().upper()
        location_active = self._trouver_location_active(immat)

        if location_active is None:
            raise ValueError(f"Aucune location active pour la voiture {immat}.")

        location_active.date_retour_reelle = date_retour_reelle
        location_active.terminee = True
        location_active.voiture.disponible = True  # La voiture redevient disponible

        return location_active.calculer_cout()

    def _trouver_location_active(self, immatriculation):

        for loc in self.locations:
            if (loc.voiture.immatriculation == immatriculation
                    and not loc.terminee):
                return loc
        return None


    def afficher_toutes_voitures(self):
        if not self.voitures:
            print("Aucune voiture enregistrée.")
            return
        print("\n=== LISTE DES VOITURES ===")
        for v in self.voitures.values():
            print(" ", v)

    def afficher_voitures_disponibles(self):
        dispo = self.consulter_disponibilite()
        if not dispo:
            print("Aucune voiture disponible actuellement.")
            return
        print("\n=== VOITURES DISPONIBLES ===")
        for v in dispo:
            print(" ", v)

    def afficher_historique_locations(self):
        if not self.locations:
            print("Aucune location enregistrée.")
            return
        print("\n=== HISTORIQUE DES LOCATIONS ===")
        for loc in self.locations:
            print(" ", loc)
