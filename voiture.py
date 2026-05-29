
class Voiture:

    def __init__(self, immatriculation, marque, modele, tarif_journalier):

        if not immatriculation or not immatriculation.strip():
            raise ValueError("L'immatriculation ne peut pas être vide.")
        if tarif_journalier <= 0:
            raise ValueError("Le tarif journalier doit être positif.")

        self.immatriculation = immatriculation.strip().upper()
        self.marque = marque
        self.modele = modele
        self.tarif_journalier = tarif_journalier
        self.disponible = True  # Disponible par défaut

    def __str__(self):
        statut = "Disponible" if self.disponible else "Louée"
        return (f"[{self.immatriculation}] {self.marque} {self.modele} "
                f"- {self.tarif_journalier} DT/jour - {statut}")
