import pandas as pd
import plotly.express as px 
from dash import Dash, dcc, html, Input, Output 
from pathlib import Path 
from src.utils.clean_data import clean_data

# 1) Chargement du fichier CSV déjà nettoyé
clean_path = Path("data/processed/etat_du_trafic_clean.csv")

# Si le fichier nettoyé n'existe pas → on le crée
if not clean_path.exists():
    print("Fichier nettoyé introuvable — génération en cours...")
    clean_data()

df = pd.read_csv(clean_path, sep=";")

# 1.b) S'assurer que les colonnes lat / lon existent
# Si clean_data() ne les a pas créées, on les calcule à partir de "Geo Point"
if "lat" not in df.columns or "lon" not in df.columns:
    df[["lat", "lon"]] = df["Geo Point"].str.split(",", n=1, expand=True)
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)

# 2) Préparation des valeurs possibles pour les filtres
statuses = sorted(df["trafficStatus"].dropna().unique())

# 3) Création de l'application Dash
app = Dash(__name__)  # Lancement de l'application Dash
app.title = "Trafic Rennes — Dashboard"   # Titre affiché dans l'onglet du navigateur

app.layout = html.Div(
    [
        html.H1("Trafic routier — Rennes Métropole"),  # Titre

        # Filtre 1 : Statut du trafic
        html.Div(
            [
                html.Label("Filtrer par statut du trafic"),
                dcc.Dropdown(
                    id="status",
                    options=[{"label": s, "value": s} for s in statuses],
                    value=statuses,          # sélectionne tout par défaut
                    multi=True,
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
                    options=[
                        {"label": f"{int(v)} km/h", "value": v}
                        for v in sorted(df["vitesse_maxi"].dropna().unique())
                    ],
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
                    min=int(df["averageVehicleSpeed"].min()),
                    max=int(df["averageVehicleSpeed"].max()),
                    value=int(df["averageVehicleSpeed"].min()),
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

# 4) Callback : met à jour les graphiques selon les filtres
@app.callback(
    Output("hist", "figure"),
    Output("map", "figure"),
    Input("status", "value"),
    Input("vmin", "value"),
    Input("vmax", "value"),
)
def update(selected_status, vmin, vmax):
    """
    Met à jour les deux graphiques en fonction des valeurs
    sélectionnées dans les filtres du dashboard.
    """
    dff = df.copy()

    # Filtre sur le statut du trafic
    if selected_status:
        dff = dff[dff["trafficStatus"].isin(selected_status)]

    # Filtre sur la vitesse maximale autorisée
    if vmax:
        dff = dff[dff["vitesse_maxi"].isin(vmax)]

    # Filtre sur la vitesse minimale observée
    dff = dff[dff["averageVehicleSpeed"] >= vmin]

    # Histogramme
    fig_hist = px.histogram(
        dff,
        x="averageVehicleSpeed",
        nbins=20,
        title="Distribution des vitesses moyennes (km/h)",
    )

    # Carte interactive
    fig_map = px.scatter_mapbox(
        dff,
        lat="lat",
        lon="lon",
        color="trafficStatus",
        hover_name="denomination",
        hover_data={
            "averageVehicleSpeed": True,
            "vitesse_maxi": True,
            "lat": False,
            "lon": False,
        },
        size="averageVehicleSpeed",
        size_max=15,
        zoom=10,
        title="Carte du trafic",
    )
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig_hist, fig_map

# 5) Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
