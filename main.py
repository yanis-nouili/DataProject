import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("data/raw/etat-du-trafic-en-temps-reel.csv", sep=';')

# --- Exploration des données ---
print("Aperçu du dataset :")
print(df.head(), "\n")

print("Dimensions :", df.shape, "\n")

print("Colonnes :")
print(df.columns, "\n")

print("Types de données :")
print(df.dtypes, "\n")

print("Valeurs manquantes :")
print(df.isna().sum(), "\n")


# --- Nettoyage de base ---
# Convertir datetime en format date
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Sélection de colonnes principales
colonnes_utiles = [
    'datetime', 'averageVehicleSpeed', 'travelTime', 'trafficStatus',
    'Geo Point', 'vitesse_maxi', 'denomination', 'hierarchie_dv'
]
df_clean = df[colonnes_utiles]

# Vérification du résultat
print("\nAperçu du dataset nettoyé :")
print(df_clean.head())

# Sauvegarder la version nettoyée
df_clean.to_csv("data/processed/etat_du_trafic_clean.csv", index=False, sep=';')
print("\n Fichier nettoyé sauvegardé dans data/processed/")
