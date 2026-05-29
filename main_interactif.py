from datetime import date, timedelta
from systeme_location import SystemeLocation
 
# ─────────────────────────────────────────────────────────────
# CODES ANSI — palette : rouge, noir
# ─────────────────────────────────────────────────────────────
 
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
 
    ROUGE  = "\033[91m"   # rouge vif
    GRIS   = "\033[37m"   # gris clair (texte sur fond sombre)
 
    BG_ROUGE = "\033[41m"  # fond rouge (titre)
 
 
# ─────────────────────────────────────────────────────────────
# UTILITAIRES D'AFFICHAGE
# ─────────────────────────────────────────────────────────────
 
def effacer_ecran():
    print("\n" * 2)
 
def titre_principal():
    print(f"{C.BG_ROUGE}{C.BOLD}{C.GRIS}")
    print("  ╔══════════════════════════════════════════════════╗  ")
    print("  ║     🚗  SYSTÈME DE LOCATION DE VOITURES  🚗      ║  ")
    print("  ║              Tunisie — DT / Jours                ║  ")
    print("  ╚══════════════════════════════════════════════════╝  ")
    print(C.RESET)
 
def separateur(titre=""):
    if titre:
        print(f"\n{C.ROUGE}{C.BOLD}{'─' * 52}{C.RESET}")
        print(f"{C.ROUGE}{C.BOLD}  {titre}{C.RESET}")
        print(f"{C.ROUGE}{'─' * 52}{C.RESET}")
    else:
        print(f"{C.DIM}{'─' * 52}{C.RESET}")
 
def succes(msg):
    print(f"  {C.ROUGE}{C.BOLD}✓{C.RESET} {msg}")
 
def erreur(msg):
    print(f"  {C.ROUGE}{C.BOLD}✗ {msg}{C.RESET}")
 
def info(msg):
    print(f"  {C.ROUGE}ℹ{C.RESET}  {msg}")
 
def afficher_voiture(v):
    statut_txt = "Disponible" if v.disponible else f"{C.ROUGE}{C.BOLD}Louée{C.RESET}"
    print(f"  {C.ROUGE}[{v.immatriculation}]{C.RESET} "
          f"{C.BOLD}{v.marque} {v.modele}{C.RESET} "
          f"— {v.tarif_journalier} DT/jour "
          f"— {statut_txt}")
 
def afficher_location(loc):
    if loc.terminee:
        statut_txt = f"{C.DIM}Terminée{C.RESET}"
    else:
        statut_txt = f"{C.ROUGE}{C.BOLD}En cours{C.RESET}"
    print(f"  {statut_txt} │ {C.BOLD}{loc.client:<20}{C.RESET} │ "
          f"{C.ROUGE}{loc.voiture.immatriculation}{C.RESET} │ "
          f"Début : {loc.date_debut} │ "
          f"Retour prévu : {C.BOLD}{loc.date_retour_prevue}{C.RESET}")
 
def afficher_cout(cout):
    print(f"\n  {'─' * 38}")
    print(f"  Durée réelle     : {cout['duree_reelle']} jour(s)")
    print(f"  Coût de base     : {C.BOLD}{cout['cout_base']} DT{C.RESET}")
    if cout['jours_retard'] > 0:
        print(f"  Jours de retard  : {C.ROUGE}{C.BOLD}{cout['jours_retard']} jour(s){C.RESET}")
        print(f"  Pénalité retard  : {C.ROUGE}{C.BOLD}{cout['penalite']} DT{C.RESET}")
    else:
        print(f"  Retard           : Aucun ✓")
    print(f"  {'─' * 38}")
    print(f"  {C.BOLD}TOTAL À PAYER    : {C.ROUGE}{cout['total']} DT{C.RESET}")
    print(f"  {'─' * 38}")
 
 
# ─────────────────────────────────────────────────────────────
# SAISIE AVEC VALIDATION
# ─────────────────────────────────────────────────────────────
 
def saisir_texte(invite, min_len=1, max_len=100):
    while True:
        valeur = input(f"  {C.ROUGE}➤{C.RESET} {invite} : ").strip()
        if len(valeur) < min_len:
            erreur(f"Entrée trop courte (min {min_len} caractère(s)).")
        elif len(valeur) > max_len:
            erreur(f"Entrée trop longue (max {max_len} caractères).")
        else:
            return valeur
 
def saisir_entier(invite, mini=1, maxi=None):
    while True:
        try:
            valeur = int(input(f"  {C.ROUGE}➤{C.RESET} {invite} : ").strip())
            if valeur < mini:
                erreur(f"Valeur minimale : {mini}.")
            elif maxi is not None and valeur > maxi:
                erreur(f"Valeur maximale : {maxi}.")
            else:
                return valeur
        except ValueError:
            erreur("Veuillez saisir un nombre entier valide.")
 
def saisir_flottant(invite, mini=0.01):
    while True:
        try:
            valeur = float(input(f"  {C.ROUGE}➤{C.RESET} {invite} : ").strip().replace(",", "."))
            if valeur < mini:
                erreur(f"Valeur minimale : {mini}.")
            else:
                return valeur
        except ValueError:
            erreur("Veuillez saisir un nombre valide (ex : 95.5).")
 
def saisir_date(invite):
    while True:
        try:
            saisie = input(f"  {C.ROUGE}➤{C.RESET} {invite} (JJ/MM/AAAA) : ").strip()
            j, m, a = map(int, saisie.split("/"))
            return date(a, m, j)
        except (ValueError, TypeError):
            erreur("Format invalide. Exemple : 05/10/2024")
 
def confirmer(invite):
    while True:
        rep = input(f"  {C.ROUGE}➤{C.RESET} {invite} [{C.BOLD}o{C.RESET}/{C.DIM}n{C.RESET}] : ").strip().lower()
        if rep in ("o", "oui", "y", "yes"):
            return True
        if rep in ("n", "non", "no"):
            return False
        erreur("Répondez 'o' (oui) ou 'n' (non).")
 
def attendre():
    print()
    input(f"  {C.DIM}Appuyez sur Entrée pour continuer...{C.RESET}")
 
 
# ─────────────────────────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────────────────────────
 
def afficher_menu(systeme):
    effacer_ecran()
    titre_principal()
 
    nb_total  = len(systeme.voitures)
    nb_dispo  = len(systeme.consulter_disponibilite())
    nb_louees = nb_total - nb_dispo
    en_cours  = sum(1 for l in systeme.locations if not l.terminee)
 
    print(f"  Parc : {C.BOLD}{nb_total}{C.RESET} voiture(s)  │  "
          f"{nb_dispo} disponible(s)  │  "
          f"{C.ROUGE}{C.BOLD}{nb_louees} louée(s){C.RESET}  │  "
          f"{C.ROUGE}{en_cours} en cours{C.RESET}")
    separateur()
 
    options = [
        ("1", "Ajouter une voiture"),
        ("2", "Louer une voiture"),
        ("3", "Retourner une voiture"),
        ("4", "Consulter les voitures"),
        ("5", "Historique des locations"),
        ("0", "Quitter"),
    ]
 
    print(f"\n{C.BOLD}  Que souhaitez-vous faire ?{C.RESET}\n")
    for code, label in options:
        print(f"  {C.ROUGE}{C.BOLD}[{code}]{C.RESET}  {label}")
 
    print()
    separateur()
    choix = input(f"  {C.BOLD}Votre choix :{C.RESET} ").strip()
    return choix
 
 
# ─────────────────────────────────────────────────────────────
# ACTIONS DU MENU
# ─────────────────────────────────────────────────────────────
 
def action_ajouter_voiture(systeme):
    separateur("➕  AJOUTER UNE VOITURE")
    immat  = saisir_texte("Immatriculation (ex: TN-1234-AB)", min_len=3, max_len=20)
    marque = saisir_texte("Marque (ex: Renault)")
    modele = saisir_texte("Modèle (ex: Clio)")
    tarif  = saisir_flottant("Tarif journalier en DT (ex: 85)")
    print()
    info(f"Voiture à ajouter : {C.BOLD}{marque} {modele}{C.RESET} — {immat.upper()} — {tarif} DT/jour")
    if confirmer("Confirmer l'ajout ?"):
        try:
            v = systeme.ajouter_voiture(immat, marque, modele, tarif)
            succes(f"Voiture ajoutée : {v}")
        except ValueError as e:
            erreur(str(e))
    else:
        info("Ajout annulé.")
    attendre()
 
 
def action_louer_voiture(systeme):
    separateur("🔑  LOUER UNE VOITURE")
    dispo = systeme.consulter_disponibilite()
    if not dispo:
        erreur("Aucune voiture disponible actuellement.")
        attendre()
        return
 
    print(f"\n  {C.BOLD}Voitures disponibles :{C.RESET}")
    for v in dispo:
        afficher_voiture(v)
 
    print()
    immat  = saisir_texte("Immatriculation de la voiture à louer")
    client = saisir_texte("Nom complet du client")
    debut  = saisir_date("Date de début de location")
    duree  = saisir_entier("Durée prévue (jours)", mini=1, maxi=365)
 
    retour_prevu = debut + timedelta(days=duree)
    print()
    info(f"Client         : {C.BOLD}{client}{C.RESET}")
    info(f"Voiture        : {C.BOLD}{immat.upper()}{C.RESET}")
    info(f"Début          : {C.BOLD}{debut}{C.RESET}")
    info(f"Durée prévue   : {C.BOLD}{duree} jour(s){C.RESET}")
    info(f"Retour prévu   : {C.BOLD}{retour_prevu}{C.RESET}")
 
    if confirmer("Confirmer la location ?"):
        try:
            loc = systeme.louer_voiture(immat, client, debut, duree)
            succes(f"Location enregistrée : {loc}")
        except ValueError as e:
            erreur(str(e))
    else:
        info("Location annulée.")
    attendre()
 
 
def action_retourner_voiture(systeme):
    separateur("🔄  RETOURNER UNE VOITURE")
    en_cours = [l for l in systeme.locations if not l.terminee]
    if not en_cours:
        info("Aucune location en cours.")
        attendre()
        return
 
    print(f"\n  {C.BOLD}Locations en cours :{C.RESET}")
    for loc in en_cours:
        afficher_location(loc)
 
    print()
    immat       = saisir_texte("Immatriculation de la voiture à retourner")
    date_retour = saisir_date("Date de retour réelle")
 
    if confirmer("Confirmer le retour ?"):
        try:
            cout = systeme.retourner_voiture(immat, date_retour)
            succes("Retour enregistré avec succès.")
            afficher_cout(cout)
        except ValueError as e:
            erreur(str(e))
    else:
        info("Retour annulé.")
    attendre()
 
 
def action_consulter_voitures(systeme):
    separateur("🚗  CONSULTER LES VOITURES")
    if not systeme.voitures:
        info("Aucune voiture dans le système.")
        attendre()
        return
 
    print(f"\n  {C.BOLD}Toutes les voitures ({len(systeme.voitures)}) :{C.RESET}\n")
    for v in systeme.voitures.values():
        afficher_voiture(v)
 
    dispo = systeme.consulter_disponibilite()
    print(f"\n  → {C.BOLD}{len(dispo)} disponible(s){C.RESET} / "
          f"{C.ROUGE}{C.BOLD}{len(systeme.voitures) - len(dispo)} louée(s){C.RESET}")
    attendre()
 
 
def action_historique(systeme):
    separateur("📋  HISTORIQUE DES LOCATIONS")
    if not systeme.locations:
        info("Aucune location enregistrée.")
        attendre()
        return
 
    en_cours  = [l for l in systeme.locations if not l.terminee]
    terminees = [l for l in systeme.locations if l.terminee]
 
    if en_cours:
        print(f"\n  {C.ROUGE}{C.BOLD}── En cours ({len(en_cours)}) ──{C.RESET}")
        for loc in en_cours:
            afficher_location(loc)
 
    if terminees:
        print(f"\n  {C.DIM}── Terminées ({len(terminees)}) ──{C.RESET}")
        for loc in terminees:
            afficher_location(loc)
 
    print(f"\n  {C.BOLD}Total : {len(systeme.locations)} location(s){C.RESET}")
    attendre()
 
 
# ─────────────────────────────────────────────────────────────
# INITIALISATION OPTIONNELLE
# ─────────────────────────────────────────────────────────────
 
def charger_donnees_demo(systeme):
    voitures_demo = [
        ("TN-1234-AB", "Renault",    "Clio",   80),
        ("TN-5678-CD", "Peugeot",    "208",    95),
        ("TN-9012-EF", "Volkswagen", "Golf",  120),
        ("TN-3456-GH", "Toyota",     "Yaris",  75),
        ("TN-7890-IJ", "Fiat",       "500",    70),
    ]
    for immat, marque, modele, tarif in voitures_demo:
        try:
            systeme.ajouter_voiture(immat, marque, modele, tarif)
        except ValueError:
            pass
 
 
# ─────────────────────────────────────────────────────────────
# BOUCLE PRINCIPALE
# ─────────────────────────────────────────────────────────────
 
def main():
    systeme = SystemeLocation()
 
    effacer_ecran()
    titre_principal()
    print(f"  Bienvenue dans le système de location de voitures !\n")
    if confirmer("Charger les 5 voitures de démonstration ?"):
        charger_donnees_demo(systeme)
        succes("5 voitures de démonstration chargées.")
        attendre()
 
    while True:
        choix = afficher_menu(systeme)
 
        if choix == "1":
            action_ajouter_voiture(systeme)
        elif choix == "2":
            action_louer_voiture(systeme)
        elif choix == "3":
            action_retourner_voiture(systeme)
        elif choix == "4":
            action_consulter_voitures(systeme)
        elif choix == "5":
            action_historique(systeme)
        elif choix == "0":
            effacer_ecran()
            titre_principal()
            print(f"\n  {C.BOLD}Merci d'avoir utilisé le système. À bientôt !{C.RESET}\n")
            break
        else:
            erreur(f"Choix invalide : '{choix}'. Entrez un chiffre entre 0 et 5.")
            attendre()
 
 
if __name__ == "__main__":
    main()