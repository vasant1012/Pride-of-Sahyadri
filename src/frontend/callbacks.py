import json
from dash import html, Input, Output, State, ALL, callback_context
import dash
import dash_bootstrap_components as dbc
from src.frontend import app
from src.frontend.api_client import api


# ==================================================
# 1. Load Filters
# ==================================================
@app.dash.callback(
    Output("filter-district", "options"),
    Output("filter-type", "options"),
    Output("filter-difficulty", "options"),
    Output("filter-season", "options"),
    Input("main-tabs", "active_tab"),
)
def load_filters(_):
    forts = api.get_forts()
    if not forts:
        return [], [], [], []

    districts = sorted({f.get("district") or "Unknown" for f in forts})
    types = sorted({f.get("type") or "Unknown" for f in forts})
    difficulties = sorted({f.get("trek_difficulty") or "Unknown" for f in forts})  # NOQA E501
    seasons = sorted({f.get("best_season") or "Unknown" for f in forts})

    return (
        [{"label": d, "value": d} for d in districts],
        [{"label": t, "value": t} for t in types],
        [{"label": d, "value": d} for d in difficulties],
        [{"label": s, "value": s} for s in seasons],
    )


# ==================================================
# 2. Update Fort List
# ==================================================
@app.dash.callback(
    Output("fort-list", "children"),
    Input("search-input", "value"),
    Input("filter-district", "value"),
    Input("filter-type", "value"),
    Input("filter-difficulty", "value"),
    Input("filter-season", "value"),
)
def update_fort_list(q, district, ftype, difficulty, season):
    params = {}
    if q:
        params["q"] = q
    if district:
        params["district"] = district
    if ftype:
        params["type"] = ftype
    if difficulty:
        params["difficulty"] = difficulty
    if season:
        params["season"] = season

    forts = api.get_forts(params)
    if not forts:
        return html.Div("No forts found.", className="text-muted")

    cards = []
    for f in forts:
        fid = f.get("fort_id") or f.get("id") or f.get("name")

        card = dbc.Button(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(f.get("name", "-"), className="fw-bold"),
                        html.P(
                            f"{f.get('district', '-')} • {f.get('type', '-')}",
                            className="mb-1",
                        ),
                        html.Small(f"Trek: {f.get('trek_difficulty', '-')}"),
                    ]
                )
            ),
            id={"type": "fort-card", "index": fid},
            n_clicks=0,
            style={
                "width": "100%",
                "textAlign": "left",
                "padding": 0,
                "border": "none",
                "background": "none",
                "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
                "marginBottom": "10px",
                "cursor": "pointer",
            },
        )
        cards.append(card)

    return cards


# ==================================================
# 3. Fort Selection (Clickable Card → Set Store)
# ==================================================
@app.dash.callback(
    Output("selected-fort-id", "data"),
    Output("main-tabs", "active_tab"),
    Input({"type": "fort-card", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def select_fort(n_clicks_list):
    ctx = callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered = ctx.triggered[0]["prop_id"].split(".")[0]

    try:
        trigger_id = json.loads(triggered.replace("'", '"'))
    except Exception:
        trigger_id = eval(triggered)

    fort_id = trigger_id.get("index")
    return fort_id, "tab-recommend"


# ==================================================
# 4. Show Selected Fort Name
# ==================================================
@app.dash.callback(
    Output("recommend-selected-name", "children"),
    Input("selected-fort-id", "data"),
)
def show_selected_fort(fid):
    if not fid:
        return "No fort selected. Click a fort from Explore."

    fort = api.get_fort(fid)
    if not fort:
        return "Fort details unavailable."

    return f"{fort.get('name')} — {fort.get('district', '')}"


# ==================================================
# 5. Nearby Recommendations
# ==================================================
@app.dash.callback(
    Output("nearby-container", "children"),
    Input("selected-fort-id", "data"),
)
def load_nearby(fort_id):
    if not fort_id:
        return "Select a fort to see nearby recommendations."

    fort = api.get_fort(fort_id)
    if not fort:
        return "Fort data not loaded."

    lat = fort.get("latitude") or fort.get("lat")
    lon = fort.get("longitude") or fort.get("lon") or fort.get("lng")

    if lat is None or lon is None:
        return "No coordinates available."

    nearby = api.get_nearby(lat, lon, k=6)
    if not nearby:
        return "No nearby forts found."

    cards = []
    for f in nearby:
        cards.append(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H6(f.get("name", "-"), className="fw-bold"),
                        html.P(
                            f"{f.get('district', '-')} • {f.get('type', '-')}",
                            className="mb-1",
                        ),
                        html.Small(f"Trek: {f.get('trek_difficulty', '-')}"),
                    ]
                ),
                className="mb-2 shadow-sm",
            )
        )
    return cards


# ==================================================
# 6. Similar Recommendations
# ==================================================
@app.dash.callback(
    Output("similar-container", "children"),
    Input("selected-fort-id", "data"),
)
def load_similar(fort_id):
    if not fort_id:
        return "Select a fort to see similar forts."

    similar = api.get_similar(fort_id, k=6)
    if not similar:
        return "No similar forts found."

    cards = []
    for f in similar:
        cards.append(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H6(f.get("name", "-"), className="fw-bold"),
                        html.P(
                            f"{f.get('district', '-')} • {f.get('type', '-')}",
                            className="mb-1",
                        ),
                        html.Small(f"Trek: {f.get('trek_difficulty', '-')}"),
                    ]
                ),
                className="mb-2 shadow-sm",
            )
        )
    return cards


# =========================================================
# 7. Insight Callback
# =========================================================
@app.dash.callback(
    Output("insight-fort-dropdown", "options"),
    Input("tabs", "value"),
    Input("search-input", "value")  # Add this
)
def load_forts_for_insight(tab, search_query):
    if tab != "insight-tab":
        raise dash.exceptions.PreventUpdate

    forts = api.get_forts()

    # Filter by search query if provided
    if search_query:
        forts = [f for f in forts if search_query.lower() in f["name"].lower()]

    return [{"label": f["name"], "value": f["fort_id"]} for f in forts]


@app.dash.callback(
    Output("insight-content", "children"),
    Input("insight-fort-dropdown", "value"),
)
def load_insight(fort_id):
    if not fort_id:
        return html.Div("Select a fort to view insights.", className="text-muted")  # NOQA E501

    fort = api.get_fort(fort_id)

    if not fort:
        return html.Div("Fort not found.", className="text-danger")

    # Extract fields
    name = fort.get("name", "Unknown Fort")
    description = fort.get("description", "No description available.")
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
            # HERO
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H3(name, className="fw-bold"),
                            html.P(description, className="text-muted"),
                            dbc.Badge(fort_type, color="primary",
                                      className="me-2"),
                            dbc.Badge(
                                f"⛰ Elevation: {elevation} m",
                                color="info",
                                className="me-2",
                            ),
                            dbc.Badge(
                                f"⚠ Difficulty: {trek_difficulty}", color="warning"  # NOQA E501
                            ),
                        ]
                    )
                ],
                className="mb-4 shadow-sm",
            ),
            # METRICS
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("🕒 Trek Time"),
                                    html.H4(f"{trek_time_hours} hrs"),
                                ]
                            )
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [html.H6("🌦 Best Season"),
                                 html.H4(best_season)]
                            )
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [html.H6("🏨 Accommodation"),
                                 html.H5(accommodation)]
                            )
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [html.H6("🔑 Key Events"), html.P(key_events)])
                        ),
                        width=3,
                    ),
                ]
            ),
            # NOTES
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5("Notes"),
                            html.Hr(),
                            html.P(notes, style={"whiteSpace": "pre-wrap"}),
                        ]
                    )
                ],
                className="mt-4 shadow-sm",
            ),
        ]
    )


# ==================================================
# 8. Q&A (RAG Query)
# ==================================================
@app.dash.callback(
    Output("qa-output", "children"),
    Input("qa-btn", "n_clicks"),
    State("qa-input", "value"),
)
def qa_callback(n, query):
    if not n:
        raise dash.exceptions.PreventUpdate

    if not query:
        return "Please enter a question."

    answers = api.rag_query(query)
    if not answers:
        return "No results found."

    cards = []
    for a in answers:
        cards.append(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(a.get("name", "-"), className="fw-bold"),
                        html.P(a.get("notes", "No notes available")),
                    ]
                ),
                className="mb-3",
            )
        )
    return cards


# ==================================================
# 9. Reset Filters
# ==================================================
@app.dash.callback(
    Output("search-input", "value"),
    Output("filter-district", "value"),
    Output("filter-type", "value"),
    Output("filter-difficulty", "value"),
    Output("filter-season", "value"),
    Input("reset-btn", "n_clicks"),
)
def reset_filters(n):
    if not n:
        raise dash.exceptions.PreventUpdate

    return "", None, None, None, None
