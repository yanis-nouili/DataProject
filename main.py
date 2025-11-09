import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from pathlib import Path

# ✅ On importe les fonctions dans utils
from utils.get_data import get_data
from utils.clean_data import clean_data


# --- Exécution des étapes de pipeline ---
print("📥 Téléchargement des données...")
get_data()

print("🧹 Nettoyage des données...")
clean_data()

# --- Chargement du fichier nettoyé ---
clean_path = Path("data/processed/etats_du_trafic_clean.csv")
df = pd.read_csv(clean_path, sep=";")

# Nettoyages complémentaires
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
df["hour"] = df["datetime"].dt.hour

# Séparer lat/lon
df[["lat", "lon"]] = df["Geo Point"].str.split(",", n=1, expand=True)
df["lat"] = df["lat"].astype(float)
df["lon"] = df["lon"].astype(float)

# Valeurs pour filtres
statuses = sorted(df["trafficStatus"].dropna().unique())
hour_min, hour_max = int(df["hour"].min()), int(df["hour"].max())

# --- APP DASH ---
app = Dash(__name__)
app.title = "Trafic Rennes — Dashboard"

app.layout = html.Div(
    [
        html.H1("Trafic routier — Rennes Métropole"),
        html.Div(
            [
                html.Label("Filtrer par statut du trafic"),
                dcc.Dropdown(
                    id="status",
                    options=[{"label": s, "value": s} for s in statuses],
                    value=statuses,
                    multi=True,
                ),
            ],
            style={"marginBottom": "12px"},
        ),
        html.Div([
            html.Label("Filtrer par vitesse maximale autorisée"),
            dcc.Dropdown(
                id="vmax",
                options=[{"label": f"{int(v)} km/h", "value": v} for v in sorted(df["vitesse_maxi"].dropna().unique())],
                value=sorted(df["vitesse_maxi"].dropna().unique()),
                multi=True,
            ),
        ], style={"marginBottom": "12px"}),

        html.Div([
            html.Label("Vitesse minimale (km/h)"),
            dcc.Slider(
                id="vmin",
                min=int(df["averageVehicleSpeed"].min()),
                max=int(df["averageVehicleSpeed"].max()),
                value=int(df["averageVehicleSpeed"].min()),
                step=1,
                tooltip={"placement": "bottom", "always_visible": True},
            ),
        ], style={"marginBottom": "12px"}),

        dcc.Graph(id="hist"),
        dcc.Graph(id="map"),
    ],
    style={"maxWidth": 1000, "margin": "auto"},
)


@app.callback(
    Output("hist", "figure"),
    Output("map", "figure"),
    Input("status", "value"),
    Input("vmin", "value"),
    Input("vmax", "value"),
)
def update(selected_status, vmin, vmax):
    dff = df.copy()

    if selected_status:
        dff = dff[dff["trafficStatus"].isin(selected_status)]
    if vmax:
        dff = dff[dff["vitesse_maxi"].isin(vmax)]
    dff = dff[dff["averageVehicleSpeed"] >= vmin]

    fig_hist = px.histogram(
        dff, x="averageVehicleSpeed", nbins=20,
        title="Distribution des vitesses moyennes (km/h)"
    )

    fig_map = px.scatter_mapbox(
        dff,
        lat="lat", lon="lon",
        color="trafficStatus",
        hover_name="denomination",
        hover_data={"averageVehicleSpeed": True, "vitesse_maxi": True, "lat": False, "lon": False},
        size="averageVehicleSpeed", size_max=15, zoom=10,
        title="Carte du trafic",
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=40, b=0))
    return fig_hist, fig_map


if __name__ == "__main__":
    app.run(debug=True)
