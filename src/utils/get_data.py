import requests
from pathlib import Path

def get_data():
    """
    Télécharge le fichier CSV du trafic routier Rennes et le stocke dans data/raw/
    """
    url = "https://data.exemple.fr/etat-du-trafic-en-temps-reel.csv"  # Remplacer par l'URL réelle

    raw_path = Path("data/raw/etat-du-trafic-en-temps-reel.csv")
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    r = requests.get(url)
    if r.status_code == 200:
        raw_path.write_bytes(r.content)
        print(f"✅ Fichier téléchargé : {raw_path}")
    else:
        raise Exception(f"❌ Erreur téléchargement : {r.status_code}")

if __name__ == "__main__":
    get_data()
