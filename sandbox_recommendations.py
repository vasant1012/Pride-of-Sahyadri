import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from src.frontend.api_client import api

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Fetch all forts
forts = api.get_forts()
df = pd.DataFrame(forts)

app.layout = dbc.Container([
    html.H2("Fort Recommendations"),

    dcc.Dropdown(
        id="rec-select",
        options=[{"label": f["name"], "value": f["name"]} for f in forts],
        placeholder="Select a fort..."
    ),

    html.Hr(),

    html.Div(id="rec-output"),

], fluid=True)


@app.callback(
    Output("rec-output", "children"),
    Input("rec-select", "value")
)
def load_similar(fort_name):
    if not fort_name:
        return "Choose a fort to see recommendations."

    fort = next((f for f in forts if f["name"] == fort_name), None)
    if not fort:
        return "Fort not found"

    similar = api.get_similar(fort_name, k=5)
    if not similar:
        return "No similar forts found."

    cards = []
    for s in similar:
        cards.append(
            dbc.Card(
                dbc.CardBody([
                    html.H5(s["name"]),
                    html.P(f"District: {s.get('district','-')}"),
                    html.P(f"Elevation: {s.get('elevation_m','-')} m"),
                ]), className="mb-3"
            )
        )

    return cards


if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
