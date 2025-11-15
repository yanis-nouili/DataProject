import requests
from pathlib import Path

def get_data():
    """
    Télécharge le fichier CSV brut contenant les données de trafic de Rennes.
    Le fichier est sauvegardé dans `data/raw/etat-du-trafic-en-temps-reel.csv`

    1/ Définir le chemin de sauvegarde du fichier.
    2/ Vérifier si le fichier existe déjà.
    3/ Télécharger le fichier depuis Open Data Rennes si nécessaire.
    """

    # 1/ On commence par définir le chemin de destination du fichier
    raw_path = Path("data/raw/etat-du-trafic-en-temps-reel.csv")
    raw_path.parent.mkdir(parents=True, exist_ok=True)  # création dossier si inexistant

    # 2/ Puis on vérifier si le fichier existe déjà, si oui on arrête la fonction
    if raw_path.exists():
        print(f"Fichier déjà présent : {raw_path}")
        return  

    # 3/ Sinon, on télécharge le fichier depuis le site "Open Data Rennes"
    url = "https://www.data.gouv.fr/datasets/etat-du-trafic-en-temps-reel/#/resources/02666160-4137-4c9a-a859-ed0a9e84679a"
    
    response = requests.get(url)
    if response.status_code == 200:
        raw_path.write_bytes(response.content)  # sauvegarde du fichier
        print(f"Fichier téléchargé et sauvegardé : {raw_path}")
    else:
        print(f"Erreur lors du téléchargement. Status code : {response.status_code}")


# Point d'entrée pour exécuter directement le script
if __name__ == "__main__":
    get_data()
