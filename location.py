
from datetime import date

class Location:

    PENALITE_PAR_JOUR = 15  # DT de pénalité par jour de retard

    def __init__(self, client, voiture, date_debut, duree_prevue):

        if duree_prevue <= 0:
            raise ValueError("La durée prévue doit être d'au moins 1 jour.")
        if not client or not client.strip():
            raise ValueError("Le nom du client ne peut pas être vide.")

        self.client = client.strip()
        self.voiture = voiture
        self.date_debut = date_debut
        self.duree_prevue = duree_prevue
        self.date_retour_prevue = date(
            date_debut.year,
            date_debut.month,
            date_debut.day
        )
        # Calcul manuel de la date de retour prévue
        from datetime import timedelta
        self.date_retour_prevue = date_debut + timedelta(days=duree_prevue)
        self.date_retour_reelle = None  # Sera remplie au retour
        self.terminee = False

    def calculer_cout(self, date_retour_reelle=None):

        if date_retour_reelle is None:
            date_retour_reelle = self.date_retour_reelle
        if date_retour_reelle is None:
            raise ValueError("La date de retour réelle n'est pas définie.")

        from datetime import timedelta
        duree_reelle = (date_retour_reelle - self.date_debut).days
        if duree_reelle < 1:
            duree_reelle = 1  # Minimum 1 jour

        cout_base = duree_reelle * self.voiture.tarif_journalier

        # Calcul des jours de retard
        jours_retard = (date_retour_reelle - self.date_retour_prevue).days
        if jours_retard < 0:
            jours_retard = 0

        penalite = jours_retard * self.PENALITE_PAR_JOUR

        return {
            "duree_reelle": duree_reelle,
            "cout_base": cout_base,
            "jours_retard": jours_retard,
            "penalite": penalite,
            "total": cout_base + penalite
        }

    def __str__(self):
        statut = "Terminée" if self.terminee else "En cours"
        return (f"Location [{statut}] - Client: {self.client} - "
                f"Voiture: {self.voiture.immatriculation} - "
                f"Début: {self.date_debut} - "
                f"Retour prévu: {self.date_retour_prevue}")
