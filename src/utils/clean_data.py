import pandas as pd
import os

RAW_FILE = "data/raw/etat-du-trafic-en-temps-reel.csv"
CLEAN_FILE = "data/cleaned/etat_du_trafic_clean.csv"

def clean():
    df = pd.read_csv(RAW_FILE, sep=';')

    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    colonnes_utiles = [
        'datetime', 'averageVehicleSpeed', 'travelTime', 'trafficStatus',
        'Geo Point', 'vitesse_maxi', 'denomination', 'hierarchie_dv'
    ]
    df = df[colonnes_utiles]

    df.to_csv(CLEAN_FILE, sep=';', index=False)
    print("✅ Données nettoyées enregistrées dans", CLEAN_FILE)

if __name__ == "__main__":
    clean()
