import pandas as pd
import plotly.express as px 
from dash import Dash, dcc, html, Input, Output 
from pathlib import Path 

# On importe les fonctions utilitaires
from utils.clean_data import clean_data
from utils.get_data import get_data


# 1) On recupere le fichier CSV depuis le site grace à la
# fonction définie dans "utils/get_data.py"
print("Import du fichier CSV brut depuis le site en ligne")
get_data()

# Puis on exécute la fonction définie dans "utils/clean_data.py" pour 
# génèrer le chemin data/processed/etats_du_trafic_clean.csv
print("Nettoyage du fichier CSV brut")
clean_data()


# Cela fait, on charge le chemin du fichier dans "clean_path" puis on
# crée un dataframe avec le CSV nettoyé 
clean_path = Path("data/processed/etats_du_trafic_clean.csv")
df = pd.read_csv(clean_path, sep=";")

# On crée une colonne "heure" pour faire l'analyse temporelle
df["heure"] = pd.to_datetime(df["datetime"]).dt.hour


# 2) On prépare les valeurs disponibles pour les filtres du dashboard en retirant les
# valeurs manquantes puis en cherchant les valeurs minimal et maximal d'heure observé
statuses = sorted(df["trafficStatus"].dropna().unique()) 
heure_min, heure_max = int(df["heure"].min()), int(df["heure"].max()) 


# 3) Maintenant que tout est prêt, on lance l'application Dash pour créer une page en 
# html sur laquelle nos données seront affiché

app = Dash(__name__)  # Lancement de l'application Dash
app.title = "Trafic Rennes — Dashboard"   # Titre affiché dans l'onglet du navigateur

# On crée la structure visuelle de la page htm de la page en y applicant des filtres 
app.layout = html.Div(
    [
        html.H1("Trafic routier — Rennes Métropole"),  # Titre

        # Filtre 1 : Statut du trafic
        html.Div(
            [
                html.Label("Filtrer par statut du trafic"),   # Label affiché
                dcc.Dropdown(
                    id="status", # Identifiant du composant
                    options=[{"label": s, "value": s} for s in statuses],  # Liste des choix
                    value=statuses,  # Valeurs sélectionnées par défaut
                    multi=True, # Autorise plusieurs valeurs
                ),
            ],
            style={"marginBottom": "12px"},
        ),

        # Filtre 2 : Vitesse maximale autorisée
        html.Div(
            [
                html.Label("Filtrer par vitesse maximale autorisée"),
                dcc.Dropdown(
                    id="vmax",
                    options=[{"label": f"{int(v)} km/h", "value": v} 
                             for v in sorted(df["vitesse_maxi"].dropna().unique())],
                    value=sorted(df["vitesse_maxi"].dropna().unique()),
                    multi=True,
                ),
            ],
            style={"marginBottom": "12px"},
        ),

        # Filtre 3 : Vitesse minimale observée
        html.Div(
            [
                html.Label("Vitesse minimale (km/h)"),
                dcc.Slider(
                    id="vmin",
                    min=int(df["averageVehicleSpeed"].min()), # Valeur min possible
                    max=int(df["averageVehicleSpeed"].max()), # Valeur max possible
                    value=int(df["averageVehicleSpeed"].min()), # Valeur sélectionnée par défaut
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
            style={"marginBottom": "12px"},
        ),

        # Zone d'affichage des graphiques

        dcc.Graph(id="hist"),  # Histogramme
        dcc.Graph(id="map"),   # Carte interactive
    ],
    style={"maxWidth": 1000, "margin": "auto"},
)


# 4) On utilise un callback qui met à jour les graphiques automatiquement selon les filtres
@app.callback(
    Output("hist", "figure"),   # Mise à jour de l'histogramme
    Output("map", "figure"),    # Mise à jour de la carte
    Input("status", "value"),   # Filtre statut
    Input("vmin", "value"),     # Filtre vitesse min
    Input("vmax", "value"),     # Filtre vitesse max autorisée
)

def update(selected_status, vmin, vmax):
    """
    Met à jour les deux graphiques en fonction des valeurs sélectionnées
    dans les filtres du dashboard.
    """
    dff = df.copy()  # On travaille sur une copie pour ne pas modifier le dataframe d'origine

    # Filtre sur le statut du trafic
    if selected_status:
        dff = dff[dff["trafficStatus"].isin(selected_status)]

    # Filtre sur la vitesse maximale autorisée
    if vmax:
        dff = dff[dff["vitesse_maxi"].isin(vmax)]

    # Filtre sur la vitesse minimale observée
    dff = dff[dff["averageVehicleSpeed"] >= vmin]

    # Création d'un histogramme
    fig_hist = px.histogram(
        dff,
        x="averageVehicleSpeed",
        nbins=20,
        title="Distribution des vitesses moyennes (km/h)"
    )

    # Création d'une carte interactive
    fig_map = px.scatter_mapbox(
        dff,
        lat="lat", lon="lon", # Coordonnées déjà prêtes depuis clean_data()
        color="trafficStatus", # Couleur selon le niveau de trafic
        hover_name="denomination", # Nom de la voie affiché au survol
        hover_data={
            "averageVehicleSpeed": True,
            "vitesse_maxi": True,
            "lat": False,
            "lon": False
        },
        size="averageVehicleSpeed",
        size_max=15,
        zoom=10,
        title="Carte du trafic",
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=40, b=0))

    return fig_hist, fig_map


# Exécution de l'application
if __name__ == "__main__":
    app.run(debug=True)   # Lancement en mode local
