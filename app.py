import requests
import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

API_BASE = "http://localhost:8000"  # Update if backend runs elsewhere

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# -------------------- Layout --------------------
app.layout = dbc.Container(
    [
        html.H2("Maharashtra Forts Dashboard", className="my-3 text-center"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("🔍 Search Forts"),
                        dcc.Input(
                            id="search-input",
                            type="text",
                            placeholder="Type fort name...",
                            className="form-control",
                            debounce=True,
                        ),
                        html.Br(),
                        dbc.Button(
                            "Search",
                            id="search-btn",
                            color="primary",
                            className="mt-2 w-100",
                        ),
                        html.Hr(),
                        html.Div(id="fort-list"),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.H5("🏰 Fort Details"),
                        html.Div(
                            id="fort-details", className="border p-3 bg-light rounded"
                        ),
                        html.Hr(),
                        html.H5("📍 Nearby Forts"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Input(
                                        id="lat-input",
                                        type="number",
                                        placeholder="Latitude",
                                        className="form-control",
                                    )
                                ),
                                dbc.Col(
                                    dcc.Input(
                                        id="lon-input",
                                        type="number",
                                        placeholder="Longitude",
                                        className="form-control",
                                    )
                                ),
                            ],
                            className="mb-2",
                        ),
                        dbc.Button(
                            "Find Nearby",
                            id="nearby-btn",
                            color="success",
                            className="w-100",
                        ),
                        html.Div(id="nearby-list", className="mt-3"),
                    ],
                    width=8,
                ),
            ]
        ),
    ],
    fluid=True,
)


# -------------------- Callbacks --------------------
@app.callback(
    Output("fort-list", "children"),
    Input("search-btn", "n_clicks"),
    State("search-input", "value"),
)
def search_forts(n, query):
    if not n:
        return "Type a fort name and click Search"
    if not query:
        return "Enter text to search"

    r = requests.get(f"{API_BASE}/forts", params={"q": query})
    data = r.json()

    if len(data) == 0:
        return "No forts found."

    buttons = []
    for f in data:
        btn = dbc.Button(
            f"{f['fort_id']}: {f['name']} ({f['district']})",
            id={"type": "fort-btn", "index": f["fort_id"]},
            color="secondary",
            size="sm",
            className="my-1 w-100",
        )
        buttons.append(btn)
    return buttons


@app.callback(
    Output("fort-details", "children"),
    Input({"type": "fort-btn", "index": dash.dependencies.ALL}, "n_clicks"),
)
def show_details(btn_clicks):
    if not btn_clicks:
        return "Select a fort from the left."

    # Identify which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Select a fort from the left."

    btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
    btn_id = eval(btn_id)  # {'type': 'fort-btn', 'index': id}
    fort_id = btn_id["index"]

    r = requests.get(f"{API_BASE}/forts/{fort_id}")
    f = r.json()

    return html.Div(
        [
            html.H4(f["name"]),
            html.P(f"District: {f.get('district', '-')}", className="mt-2"),
            html.P(f"Type: {f.get('type', '-')}", className="mt-1"),
            html.P(f"Elevation: {f.get('elevation_m', '-')}", className="mt-1"),
            html.P(f"Difficulty: {f.get('trek_difficulty', '-')}", className="mt-1"),
            html.P(f"Notes: {f.get('notes', '-')[:200]}...", className="mt-3"),
        ]
    )


@app.callback(
    Output("nearby-list", "children"),
    Input("nearby-btn", "n_clicks"),
    State("lat-input", "value"),
    State("lon-input", "value"),
)
def nearby(n, lat, lon):
    if not n:
        return "Enter coordinates to search nearby forts."
    if not lat or not lon:
        return "Provide both latitude and longitude."

    r = requests.get(
        f"{API_BASE}/recommend/nearby", params={"lat": lat, "lon": lon, "k": 5}
    )
    data = r.json()

    if len(data) == 0:
        return "No nearby forts found."

    return html.Ul([html.Li(f"{f['name']} — {f['distance_km']:.2f} km") for f in data])


# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(debug=False, port=8050)
