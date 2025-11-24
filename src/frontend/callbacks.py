import json
from dash import html, Input, Output, State, ALL, callback_context
import dash
import pandas as pd
import plotly.express as px
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
    difficulties = sorted({f.get("trek_difficulty") or "Unknown" for f in forts})
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
# 7. Cluster Analysis Callback
# =========================================================
@app.dash.callback(
    Output("ca-total-clusters", "children"),
    Output("ca-largest-cluster", "children"),
    Output("ca-smallest-cluster", "children"),
    Output("ca-bar", "figure"),
    Output("ca-pie", "figure"),
    Output("ca-scatter-elev", "figure"),
    Output("ca-scatter-time", "figure"),
    Output("ca-cluster-profile", "children"),
    Input("main-tabs", "active_tab"),
)
def update_cluster_analysis(active_tab):
    if active_tab != "tab-cluster":
        raise dash.exceptions.PreventUpdate

    # ---- Fetch Data from API ----
    clusters = api.get_clusters()  # {0: 50, 1: 40, ...}
    points = api.get_clustered_forts()  # each fort with cluster label

    df = pd.DataFrame(points)

    # ---- Convert numeric columns ----
    df["elevation_m"] = pd.to_numeric(df["elevation_m"], errors="coerce")
    df["trek_time_hours"] = pd.to_numeric(df["trek_time_hours"], errors="coerce")
    df["difficulty_num"] = pd.to_numeric(df["difficulty_num"], errors="coerce")

    # ---- Summary Numbers ----
    total_clusters = len(clusters)

    largest_cluster_id = max(clusters, key=lambda k: clusters[k])
    smallest_cluster_id = min(clusters, key=lambda k: clusters[k])

    largest_text = (
        f"Cluster {largest_cluster_id} ({clusters[largest_cluster_id]} forts)"
    )
    smallest_text = (
        f"Cluster {smallest_cluster_id} ({clusters[smallest_cluster_id]} forts)"
    )

    # ---- Bar Chart ----
    fig_bar = px.bar(
        x=list(clusters.keys()),
        y=list(clusters.values()),
        labels={"x": "Cluster ID", "y": "Count"},
        title="Forts Per Cluster",
    )

    # ---- Pie Chart ----
    fig_pie = px.pie(
        names=list(clusters.keys()),
        values=list(clusters.values()),
        title="Cluster Distribution",
    )

    # ---- Scatter: Elevation vs Cluster ----
    fig_scatter_elev = px.scatter(
        df,
        x="cluster",
        y="elevation_m",
        color="cluster",
        hover_data=["name", "district"],
        title="Elevation by Cluster",
    )

    # ---- Scatter: Trek Time vs Cluster ----
    fig_scatter_time = px.scatter(
        df,
        x="cluster",
        y="trek_time_hours",
        color="cluster",
        hover_data=["name", "district"],
        title="Trek Time by Cluster",
    )

    # ---- Cluster Profile Table ----
    profile_rows = []
    for cid in sorted(clusters.keys()):
        subset = df[df["cluster"] == cid]

        avg_elev = round(subset["elevation_m"].mean(), 1)
        avg_time = round(subset["trek_time_hours"].mean(), 2)
        avg_diff = round(subset["difficulty_num"].mean(), 2)

        common_type = subset["type"].value_counts().idxmax()
        common_district = subset["district"].value_counts().idxmax()

        profile_rows.append(
            html.Tr(
                [
                    html.Td(cid),
                    html.Td(clusters[cid]),
                    html.Td(avg_elev),
                    html.Td(avg_time),
                    html.Td(avg_diff),
                    html.Td(common_type),
                    html.Td(common_district),
                ]
            )
        )

    profile_table = dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Cluster"),
                        html.Th("Size"),
                        html.Th("Avg Elevation"),
                        html.Th("Avg Trek Time"),
                        html.Th("Avg Difficulty"),
                        html.Th("Most Common Type"),
                        html.Th("Top District"),
                    ]
                )
            ),
            html.Tbody(profile_rows),
        ],
        bordered=True,
        striped=True,
        hover=True,
        className="mt-3",
    )

    return (
        total_clusters,
        largest_text,
        smallest_text,
        fig_bar,
        fig_pie,
        fig_scatter_elev,
        fig_scatter_time,
        profile_table,
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
