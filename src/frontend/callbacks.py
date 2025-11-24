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
# Robust Cluster Analysis callback (drop-in replacement)
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
    
    # Only run when insights tab active
    if active_tab != "tab-cluster":
        raise dash.exceptions.PreventUpdate

    # Fetch cluster counts and clustered forts
    clusters = api.get_clusters() or {}
    points = api.get_clustered_forts() or []

    # Defensive: ensure clusters is dict-like
    if not isinstance(clusters, dict):
        try:
            clusters = dict(clusters)
        except Exception:
            clusters = {}

    # Placeholder empty figure
    def empty_fig(title="No data"):
        import plotly.graph_objects as go

        fig = go.Figure()
        fig.add_annotation(text=title, x=0.5, y=0.5, showarrow=False)
        fig.update_layout(
            xaxis={"visible": False}, yaxis={"visible": False}, title=title
        )
        return fig

    if len(clusters) == 0 and len(points) == 0:
        # nothing to show
        return (
            "0",
            "N/A",
            "N/A",
            empty_fig("No cluster counts available"),
            empty_fig("No cluster counts available"),
            empty_fig("No data"),
            empty_fig("No data"),
            html.Div("No cluster data available.", className="text-muted"),
        )

    # Build DataFrame safely
    df = pd.DataFrame(points)

    # SAFELY get numeric columns with fallbacks
    def safe_numeric(col_candidates):
        """Return series coerced numeric from first existing candidate column name or None."""
        for c in col_candidates:
            if c in df.columns:
                return pd.to_numeric(df[c], errors="coerce")
        return None

    # Common fallbacks
    df["elevation_m"] = safe_numeric(
        ["elevation_m", "elevation", "height", "height_m"]
    ) or pd.Series([pd.NA] * len(df))
    df["trek_time_hours"] = safe_numeric(
        ["trek_time_hours", "trek_time", "time_hours", "trek_time_h"]
    ) or pd.Series([pd.NA] * len(df))
    df["difficulty_num"] = safe_numeric(
        ["difficulty_num", "difficulty", "trek_difficulty", "difficulty_value"]
    ) or pd.Series([pd.NA] * len(df))

    # Ensure cluster column exists (could be str or int)
    if "cluster" not in df.columns:
        # try other names
        if "cluster_id" in df.columns:
            df["cluster"] = df["cluster_id"]
        else:
            # attempt to derive cluster from API clusters: if `points` empty or has no cluster, fallback to None
            df["cluster"] = pd.Series([pd.NA] * len(df))

    # Coerce cluster to int where possible
    try:
        df["cluster"] = pd.to_numeric(df["cluster"], errors="coerce").astype("Int64")
    except Exception:
        # keep as-is when cannot coerce
        pass

    # Use clusters dict if provided; otherwise derive from df
    if len(clusters) == 0 and "cluster" in df.columns:
        counts_series = df["cluster"].value_counts(dropna=True).sort_index()
        clusters = {int(k): int(v) for k, v in counts_series.to_dict().items()}

    # Summary numbers
    total_clusters = len(clusters)

    # Compute largest/smallest cluster texts safely
    if clusters:
        # cluster keys might be strings, keep stable ordering
        try:
            largest_cluster_id = max(clusters, key=lambda k: clusters[k])
            smallest_cluster_id = min(clusters, key=lambda k: clusters[k])
            largest_text = (
                f"Cluster {largest_cluster_id} ({clusters[largest_cluster_id]} forts)"
            )
            smallest_text = (
                f"Cluster {smallest_cluster_id} ({clusters[smallest_cluster_id]} forts)"
            )
        except Exception:
            largest_text = "N/A"
            smallest_text = "N/A"
    else:
        largest_text = "N/A"
        smallest_text = "N/A"

    # -------- Charts --------
    # Bar & Pie based on clusters dict (if empty, fallback to df counts)
    try:
        bar_x = list(clusters.keys())
        bar_y = list(clusters.values())
        fig_bar = px.bar(
            x=bar_x,
            y=bar_y,
            labels={"x": "Cluster ID", "y": "Count"},
            title="Forts Per Cluster",
        )
        fig_pie = px.pie(names=bar_x, values=bar_y, title="Cluster Distribution")
    except Exception:
        fig_bar = empty_fig("No cluster distribution")
        fig_pie = empty_fig("No cluster distribution")

    # Scatter: elevation vs cluster
    if (
        "elevation_m" in df.columns
        and df["elevation_m"].notna().sum() > 3
        and "cluster" in df.columns
        and df["cluster"].notna().sum() > 0
    ):
        try:
            fig_scatter_elev = px.scatter(
                df.dropna(subset=["elevation_m", "cluster"]),
                x="cluster",
                y="elevation_m",
                color="cluster",
                hover_data=["name", "district"],
                title="Elevation by Cluster",
            )
        except Exception:
            fig_scatter_elev = empty_fig("Elevation scatter not available")
    else:
        fig_scatter_elev = empty_fig("Insufficient elevation data")

    # Scatter: trek time vs cluster
    if (
        "trek_time_hours" in df.columns
        and df["trek_time_hours"].notna().sum() > 3
        and "cluster" in df.columns
        and df["cluster"].notna().sum() > 0
    ):
        try:
            fig_scatter_time = px.scatter(
                df.dropna(subset=["trek_time_hours", "cluster"]),
                x="cluster",
                y="trek_time_hours",
                color="cluster",
                hover_data=["name", "district"],
                title="Trek Time by Cluster",
            )
        except Exception:
            fig_scatter_time = empty_fig("Trek time scatter not available")
    else:
        fig_scatter_time = empty_fig("Insufficient trek time data")

    # -------- Cluster Profile Table --------
    if not df.empty and "cluster" in df.columns and df["cluster"].notna().any():
        profile_rows = []
        keys_sorted = sorted(
            [k for k in clusters.keys()],
            key=lambda x: int(x) if str(x).isdigit() else str(x),
        )
        for cid in keys_sorted:
            # filter subset safely
            subset = df[df["cluster"].astype(str) == str(cid)]
            if subset.empty:
                avg_elev = "N/A"
                avg_time = "N/A"
                avg_diff = "N/A"
                common_type = "N/A"
                common_district = "N/A"
            else:
                avg_elev = (
                    round(subset["elevation_m"].dropna().mean(), 1)
                    if subset["elevation_m"].notna().any()
                    else "N/A"
                )
                avg_time = (
                    round(subset["trek_time_hours"].dropna().mean(), 2)
                    if subset["trek_time_hours"].notna().any()
                    else "N/A"
                )
                avg_diff = (
                    round(subset["difficulty_num"].dropna().mean(), 2)
                    if subset["difficulty_num"].notna().any()
                    else "N/A"
                )
                common_type = (
                    subset["type"].mode().iloc[0]
                    if "type" in subset.columns and not subset["type"].mode().empty
                    else "N/A"
                )
                common_district = (
                    subset["district"].mode().iloc[0]
                    if "district" in subset.columns
                    and not subset["district"].mode().empty
                    else "N/A"
                )

            profile_rows.append(
                html.Tr(
                    [
                        html.Td(str(cid)),
                        html.Td(str(clusters.get(cid, 0))),
                        html.Td(str(avg_elev)),
                        html.Td(str(avg_time)),
                        html.Td(str(avg_diff)),
                        html.Td(str(common_type)),
                        html.Td(str(common_district)),
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
    else:
        profile_table = html.Div(
            "No cluster profile available.", className="text-muted"
        )

    return (
        str(total_clusters),
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
