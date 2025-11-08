import pandas as pd
from pathlib import Path

def clean_data():
    """
    Nettoie le fichier CSV brut et le sauvegarde dans data/processed/
    """
    raw_path = Path("data/raw/etat-du-trafic.csv")
    cleaned_path = Path("data/processed/etat-du-trafic-clean.csv")
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path, sep=";")

    # Conversion datetime
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Colonnes utiles
    cols = ['datetime', 'averageVehicleSpeed', 'travelTime', 'trafficStatus',
            'Geo Point', 'vitesse_maxi', 'denomination', 'hierarchie_dv']
    df_clean = df[cols]

    # Géolocalisation : lat / lon
    df_clean[["lat", "lon"]] = df_clean["Geo Point"].str.split(",", n=1, expand=True)
    df_clean["lat"] = pd.to_numeric(df_clean["lat"], errors="coerce")
    df_clean["lon"] = pd.to_numeric(df_clean["lon"], errors="coerce")

    # Sauvegarde
    df_clean.to_csv(cleaned_path, index=False, sep=";")
    print(f"Fichier nettoyé sauvegardé : {cleaned_path}")

if __name__ == "__main__":
    clean_data()
