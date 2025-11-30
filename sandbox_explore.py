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
    html.H2("Explore Maharashtra Forts"),

    dcc.Dropdown(
        id="explore-dropdown",
        options=[{"label": f["name"], "value": f["name"]} for f in forts],
        placeholder="Select a fort..."
    ),

    html.Div(id="explore-output", className="mt-4"),

], fluid=True)


@app.callback(
    Output("explore-output", "children"),
    Input("explore-dropdown", "value")
)
def show_fort_details(name):
    if not name:
        return "Select a fort to view details."

    fort = next((f for f in forts if f["name"] == name), None)
    if not fort:
        return "Fort not found."

    return dbc.Card([
        dbc.CardBody([
            html.H4(fort["name"]),
            html.P(f"District: {fort.get('district', '-') }"),
            html.P(f"Type: {fort.get('type', '-') }"),
            html.P(f"Elevation: {fort.get('elevation_m', '-') } m"),
            html.P(f"Trek Difficulty: {fort.get('trek_difficulty', '-') }"),
            html.P(f"Notes: {fort.get('notes', '-') }"),
        ])
    ], className="mt-3")


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
