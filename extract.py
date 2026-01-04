import pandas

def lire_fichier(nom_fichier):
    donnees_anime = {}
    stats_votes = [] # Pour stocker les pourcentages à la fin

    with open(nom_fichier, 'r', encoding='utf-8') as f:
        for ligne in f:
            ligne = ligne.strip()
            
            # 1. Ignorer les lignes vides ou les balises de source
            if not ligne or ligne.startswith(""):
                continue
            
            # 2. Cas des lignes standards "Clé: Valeur"
            if ":" in ligne:
                cle, valeur = ligne.split(":", 1)
                donnees_anime[cle.strip()] = valeur.strip()
            
            # 3. Cas des lignes de statistiques (ex: "36.9%(154416 votes)")
            elif "%" in ligne: 
                stats_votes.append(ligne)
                
    # Ajouter les votes au dictionnaire si on en a trouvé
    if stats_votes:
        donnees_anime['Rating_Distribution'] = stats_votes
        
    return donnees_anime
