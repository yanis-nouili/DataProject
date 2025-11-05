import pandas as pd

import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from pathlib import Path


"""# Charger le fichier CSV
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
print("\n Fichier nettoyé sauvegardé dans data/processed/")"""


# --- Chargement ---
clean_path = Path("data/processed/etat_du_trafic_clean.csv")
df = pd.read_csv(clean_path, sep=";")

# Nettoyages complémentaires
df["datetime"] = pd.to_datetime(df["datetime"], format="ISO8601", errors="coerce")


# "Geo Point" => lat, lon (forme "lat, lon")
df[["lat", "lon"]] = df["Geo Point"].str.split(",", n=1, expand=True)
df["lat"] = df["lat"].astype(float)
df["lon"] = df["lon"].astype(float)

# Valeurs possibles de statut
statuses = sorted(df["trafficStatus"].dropna().unique())

#Instancie l'application Dash
app = Dash(__name__)
app.title = "Trafic Rennes — Dashboard"

app.layout = html.Div(
    [
        html.H1("Trafic routier — Rennes Métropole"),
        html.Div(
            [
                html.Label("Filtrer par statut du trafic"),
                dcc.Dropdown(       #sélecteur déroulant
                    id="status",
                    options=[{"label": s, "value": s} for s in statuses],
                    value=statuses,                # sélectionne tout par défaut
                    multi=True,
                ),
            ],
            style={"marginBottom": "12px"},
        ),
        dcc.Slider(     #seuil minimal de vitesse
            id="vmin",
            min=int(df["averageVehicleSpeed"].min()),
            max=int(df["averageVehicleSpeed"].max()),
            value=int(df["averageVehicleSpeed"].min()),
            step=1,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        dcc.Graph(id="hist"),
        dcc.Graph(id="map"),  #emplacement vide au depart; sera rempli par le callback 
    ],
    style={"maxWidth": 1000, "margin": "auto"}, #centre le contenu
)

@app.callback(  #met à jour les graphiques en fonction des filtres
    Output("hist", "figure"),
    Output("map", "figure"),
    Input("status", "value"),
    Input("vmin", "value"),
)
def update(selected_status, vmin): #crée un dataframe filtré; par les statuts selectionnés et la vitesse minimale
    dff = df.copy()
    if selected_status:
        dff = dff[dff["trafficStatus"].isin(selected_status)]
    dff = dff[dff["averageVehicleSpeed"] >= vmin]

    # Histogramme
    fig_hist = px.histogram( #compte le nombre d'occurrences pour chaque intervalle de vitesse
        dff,
        x="averageVehicleSpeed",
        nbins=20,
        title="Distribution des vitesses moyennes (km/h)",
    )

    # Carte (OpenStreetMap)
    fig_map = px.scatter_mapbox(
        dff,
        lat="lat",
        lon="lon",
        color="trafficStatus",
        hover_name="denomination",
        hover_data={ #affiche les infos au survol; masque lat et lon
            "averageVehicleSpeed": True,
            "vitesse_maxi": True,
            "lat": False,
            "lon": False,
        },
        size="averageVehicleSpeed",
        size_max=15,
        zoom=10,
        title="Carte du trafic (statut + vitesse)",
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=40, b=0)) #évite d'avoir besoin d'une clé Mapbox
    return fig_hist, fig_map #renvoie les deux figures 

if __name__ == "__main__":
    app.run(debug=True) #lance l'app en local

