import os
import csv
import pandas as pd

# =========================
# 📁 CHEMINS
# =========================
DOSSIER = r"C:\Users\tmargerand\Downloads"
CHEMIN_EXCEL = r"C:\Users\tmargerand\Downloads\MAL_dataset.xlsx"

# =========================
# 🚫 FILTRES
# =========================

# lignes à supprimer par préfixe (langues)
LIGNES_A_SUPPRIMER = (
    "Japanese:",
    "German:",
    "Spanish:"
)

# clés à supprimer STRICTEMENT
CLES_A_SUPPRIMER = {
    "Genre",      # on garde "Genres"
    "Theme",      # on garde "Themes"
    "Rating",
    "Source",
    "Licensors",
    "Producers",
    "Broadcast",
    "Status",
    "French",
    "Aired",
    "Synonyms",
    "Total",
    "On-Hold",
    "Watching",
    "Plan to Watch",
    "Dropped"
}

# =========================
# 1️⃣ LECTURE + NETTOYAGE
# =========================
MAL_extraction = []

for filename in sorted(os.listdir(DOSSIER)):
    if filename.endswith(".txt"):
        filepath = os.path.join(DOSSIER, filename)
        fichier_data = []

        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for ligne in reader:
                valeur = ligne[0]
                key = valeur.split(":", 1)[0]

                # filtres combinés
                if not valeur.startswith(LIGNES_A_SUPPRIMER) and key not in CLES_A_SUPPRIMER:
                    fichier_data.append(ligne)

        MAL_extraction.append(fichier_data)
        print(f"✔ {filename} chargé ({len(fichier_data)} lignes)")

print(f"\nTotal fichiers chargés : {len(MAL_extraction)}")

# =========================
# 2️⃣ CONVERSION EN DICTS
# =========================
def anime_to_dict(anime):
    data = {}
    for champ in anime:
        texte = champ[0]
        if ":" in texte:
            key, value = texte.split(":", 1)
            data[key.strip()] = value.strip()
    return data

anime_dicts = [anime_to_dict(anime) for anime in MAL_extraction]

# =========================
# 3️⃣ NETTOYAGES SPÉCIFIQUES
# =========================

def score_nettoyage(texte):
    return texte[:5]

def duree_nettoyage(texte):
    return texte[:6]

def extraire_rang(texte):
    if "based" in texte:
        return texte.split("based", 1)[0]
    return texte

def garder_premier_studio(texte):
    if "," in texte:
        return texte.split(",", 1)[0].strip()
    return texte

for anime in anime_dicts:
    if "Score" in anime:
        anime["Score"] = score_nettoyage(anime["Score"])

    if "Duration" in anime:
        anime["Duration"] = duree_nettoyage(anime["Duration"])

    if "Ranked" in anime:
        anime["Ranked"] = extraire_rang(anime["Ranked"])

    if "Studios" in anime:
        anime["Studios"] = garder_premier_studio(anime["Studios"])


def nettoyer_genres_themes(texte):
    if not texte:
        return texte

    elements = texte.split(",")
    nettoyes = []

    for elem in elements:
        elem = elem.strip()
        longueur = len(elem)

        # supprimer doublon concaténé (DramaDrama → Drama)
        if longueur % 2 == 0:
            moitie = longueur // 2
            if elem[:moitie] == elem[moitie:]:
                elem = elem[:moitie]

        nettoyes.append(elem)

    # supprimer doublons éventuels tout en gardant l'ordre
    nettoyes_uniques = list(dict.fromkeys(nettoyes))

    return ",".join(nettoyes_uniques)



for anime in anime_dicts:
    if "Themes" in anime:
        anime["Themes"] = nettoyer_genres_themes(anime["Themes"])

    if "Demographic" in anime:
        anime["Demographic"] = nettoyer_genres_themes(anime["Demographic"])

    if "Genres" in anime:
        anime["Genres"] = nettoyer_genres_themes(anime["Genres"])

# =========================
# 4️⃣ EXPORT EXCEL
# =========================
df = pd.DataFrame(anime_dicts)
df.to_excel(CHEMIN_EXCEL, index=False)
print("\n✅ Export Excel terminé")
print(f"📄 Fichier créé : {CHEMIN_EXCEL}")