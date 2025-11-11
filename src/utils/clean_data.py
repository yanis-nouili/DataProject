import pandas as pd
from pathlib import Path

def clean_data():
    """
    Nettoie le fichier CSV brut contenant les données de trafic de Rennes et
    génère un fichier nettoyé prêt à l'utilisation pour le dashboard.

    Étapes :
    1/ Chargement du CSV brut depuis data/raw/
    2/ Observation initiale des données pour vérification
    3/ Sélection des colonnes pertinentes
    4/ Extraction des coordonnées lat / lon depuis "Geo Point"
    5/ Export du CSV nettoyé dans data/processed/
    """


    ## 1/ Chargement du CSV brut depuis "data/raw/ 
   
    # On commence par définir les chemins des fichiers
 
    # raw_path est le chemin vers le CSV brut déjà téléchargé
    raw_path = Path("data/raw/etat-du-trafic-en-temps-reel.csv")

    # cleaned_path est le chemin où sera sauvegardé le CSV nettoyé
    cleaned_path = Path("data/processed/etats_du_trafic_clean.csv")
    
    # On crée le dossier "processed" dans le cas ou il n'existerait pas encore
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)

    # Cela fait, on charge le fichier en utilisant ";" comme séparateur dû à
    # la façon dont le CSV est rempli
    df = pd.read_csv(raw_path, sep=";")

    """
    ## 2/ Observation initiale des données

    # Nous observons mainteant le jeu de données pour pouvoir appréhender
    # le matériel avec lequel nous allons devoir travailler

    # Affiche les 5 premières lignes
    print("Aperçu du dataset :")
    print(df.head(), "\n")

    # Affiche le nombre de lignes et colonnes
    print("Dimensions :", df.shape, "\n")

    # Affiche la liste des colonnes
    print("Colonnes :")
    print(df.columns, "\n")

    # Affiche le type de données pour chaque colonne
    print("Types de données :")
    print(df.dtypes, "\n")

    # Vérifie la présence de valeurs manquantes
    print("Valeurs manquantes :")
    print(df.isna().sum(), "\n")
    """

    ## 3/ Sélection des colonnes pertinentes

    # Maintenant que nous savons ce que nous avons a disposition, nous choisissons
    # uniquement les colonnes pertinentes sur lesquelles nous pouvons travailler.

    # On commence par transformer toute les valeurs de la colonne "datetime" en type 
    # "datetime" pour pouvoir trier, filtrer et manipuler les dates. Le parametre 
    # errors="coerce" quand à lui remplace les valeurs non convertibles par NaT 
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Cela fait nous isolons toutes les colonnes que nous voulons dans la variable "cols"
    cols = [
        "datetime",           # date et heure de la mesure
        "averageVehicleSpeed",# vitesse moyenne observée
        "travelTime",         # temps de parcours
        "trafficStatus",      # statut du trafic (fluide, bouchon...)
        "Geo Point",          # coordonnées géographiques sous forme "latitude, longitude"
        "vitesse_maxi",       # vitesse maximale autorisée
        "denomination",       # nom de la route
        "hierarchie_dv"       # hiérarchie de la voie
    ]

    # Finalement, on crée une copie explicite pour éviter le "SettingWithCopyWarning"
    df_clean = df[cols].copy()


    # 4/ Extraction latitude / longitude depuis "Geo Point"

    # "Geo Point" est sous la forme "lat, lon". Nous allons le séparer en deux colonnes 
    # distinctes pour pouvoir récupérer la latitude et la longitude 


    # "str.split(",", n=1, expand=True)" sépare "Geo Point" en deux colonnes
    df_clean[["lat", "lon"]] = df_clean["Geo Point"].str.split(",", n=1, expand=True)

    # "pd.to_numeric(df_clean["lat/lon"], errors="coerce") convertit en float 
    # et remplace les valeurs incorrectes par NaN
    df_clean["lat"] = pd.to_numeric(df_clean["lat"], errors="coerce")
    df_clean["lon"] = pd.to_numeric(df_clean["lon"], errors="coerce")


    # 5/ Export du CSV nettoyé

    # Et pour nous exportons le fichier nettoyé vers le chemin défini au
    # préalable et enregistré dans la varibale cleaned_path


    # Le paramètre "index=False" permet de ne pas ajouter de colonne index
    # et sep=";" nous permet de conserver le séparateur d'origine
    df_clean.to_csv(cleaned_path, index=False, sep=";")
    print(f"Fichier nettoyé sauvegardé : {cleaned_path}")



# Permet d'exécuter la fonction directement si le script est lancé seul
if __name__ == "__main__":
    clean_data()
