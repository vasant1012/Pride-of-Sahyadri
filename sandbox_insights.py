import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import Input, Output

from src.frontend.api_client import api

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Fetch Sindhudurg Fort (fort_id = 301)
fort = api.get_fort("301")


app.layout = dbc.Container(
    [
        html.H2("Fort Insights Sandbox", className="mt-3"),
        html.Button(
            "Load Insights",
            id="load-btn",
            className="btn btn-primary mt-3",
            style={"backgroundColor": "#5ca782"},
        ),
        html.Div(id="insight-output", className="mt-4"),
    ],
    fluid=True, style={"backgroundColor": "#ddffee"}
)


@app.callback(
    Output("insight-output", "children"),
    Input("load-btn", "n_clicks"),
)
def load_insights(n):
    if not n:
        raise dash.exceptions.PreventUpdate

    if not fort:
        return html.Div("Unable to load fort details.", className="text-danger")

    name = fort.get("name", "Unknown Fort")
    fort_type = fort.get("type", "Unknown Type")
    elevation = fort.get("elevation_m", "N/A")
    key_events = fort.get("key_events", "N/A")
    trek_difficulty = fort.get("trek_difficulty", "N/A")
    trek_time_hours = fort.get("trek_time_hours", "N/A")
    best_season = fort.get("best_season", "N/A")
    accommodation = fort.get("accommodation", "N/A")
    notes = fort.get("notes", "N/A")

    return html.Div(
        [
            # ---------------------------
            # HERO CARD
            # ---------------------------
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H2(name, className="fw-bold", style={"color": "#143f29"}),
                        html.P(notes, className="text-muted mt-2"),
                        dbc.Badge(fort_type, color="primary", className="me-2"),
                        dbc.Badge(
                            f"Elevation: {elevation} m", color="info", className="me-2"
                        ),
                        dbc.Badge(
                            f"Difficulty: {trek_difficulty}",
                            color="warning",
                            className="me-2",
                        ),
                    ]
                ),
                className="shadow-sm mb-4",
                style={"backgroundColor": "#c0f6db"},
            ),
            # ---------------------------
            # SUMMARY CARDS ROW
            # ---------------------------
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Trek Duration", style={"color": "#143f29"}),
                                    html.H4(f"{trek_time_hours} hrs"),
                                ]
                            ),
                            className="shadow-sm mb-3",
                            style={"textAlign": "center", "backgroundColor": "#82edb8"},
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Best Season", style={"color": "#143f29"}),
                                    html.H4(best_season),
                                ]
                            ),
                            className="shadow-sm mb-3",
                            style={"textAlign": "center", "backgroundColor": "#82edb8"},
                        ),
                        width=6,
                    ),
                ],
                className="mt-2",
            ),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Accommodation", style={"color": "#143f29"}),
                            html.P(accommodation),
                        ]
                    ),
                    className="shadow-sm mb-3",
                    style={
                        "textAlign": "center",
                        "backgroundColor": "#9bf1c6",
                    },
                ),
                className="shadow-sm mb-4",
                style={
                        "padding": "15px",
                    }
            ),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Key Events", style={"color": "#143f29"}),
                            html.P(key_events),
                        ]
                    ),
                    className="shadow-sm mb-3",
                    style={
                        "textAlign": "center",
                        "padding": "15px",
                        "backgroundColor": "#9bf1c6",
                    },
                ),
                className="shadow-sm mb-4",
                style={
                        "padding": "15px",
                    }
            ),
        ],
        className="p-3",
    )


if __name__ == "__main__":
    app.run_server(debug=False, port=8060)
