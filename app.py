import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from src.frontend.api_client import (
    get_forts,
    # get_fort,
    rag_query,
    get_clusters,
    # predict_cluster,
    get_nearby,
    get_similar,
)

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.MINTY], title="Pride of Sahyadri"
)

# ----------------------------------------------------------------
# Header Section
# ----------------------------------------------------------------
header = dbc.Navbar(
    dbc.Container(
        [
            html.H2(
                "🏰 Pride of Sahyadri",
                className="text-white mb-0",
                style={"textAlign": "center"},
            ),
        ]
    ),
    color="dark",
    className="mb-4",
)

# ----------------------------------------------------------------
# Sidebar (Left Panel)
# ----------------------------------------------------------------
sidebar = dbc.Card(
    [
        html.H5("🔎 Search & Filters", className="card-title"),
        html.Hr(),
        # Search input
        dbc.Input(
            id="search-input",
            type="text",
            placeholder="Search forts by name, keyword...",
            className="mb-3",
        ),
        # District filter
        html.Label("District"),
        dcc.Dropdown(
            id="filter-district",
            placeholder="Select district",
            multi=False,
            className="mb-2",
        ),
        # Fort type
        html.Label("Fort Type"),
        dcc.Dropdown(
            id="filter-type",
            placeholder="Select fort type",
            multi=False,
            className="mb-2",
        ),
        # Trek difficulty
        html.Label("Trek Difficulty"),
        dcc.Dropdown(
            id="filter-difficulty",
            placeholder="Select difficulty",
            multi=False,
            className="mb-2",
        ),
        # Season filter
        html.Label("Best Season"),
        dcc.Dropdown(
            id="filter-season",
            placeholder="Select season",
            multi=False,
            className="mb-4",
        ),
        # dbc.Button("Reset Filters", id="reset-btn",
        #            color="secondary", block=True)
        dbc.Button(
            "Reset Filters",
            id="reset-btn",
            color="secondary",
            className="w-100",  # full width
        ),
    ],
    body=True,
    className="shadow-sm",
    style={"height": "100vh", "overflowY": "auto"},
)

# ----------------------------------------------------------------
# Main Content Tabs (Right Panel)
# ----------------------------------------------------------------
tabs = dbc.Tabs(
    [
        # Explore Tab
        dbc.Tab(
            label="Explore",
            tab_id="tab-explore",
            children=[
                html.Br(),
                html.H4("Explore Forts"),
                # Map placeholder
                html.Div(
                    id="map-container",
                    children=html.Div("Map will load here...", className="text-muted"),
                    style={
                        "height": "400px",
                        "background": "#f8f9fa",
                        "border": "1px solid #ddd",
                    },
                    className="mb-4",
                ),
                # Fort card list placeholder
                html.Div(
                    id="fort-list",
                    children=[
                        html.Div(
                            "Fort list will appear here...", className="text-muted"
                        )
                    ],
                ),
            ],
        ),
        # Recommendations Tab
        dbc.Tab(
            label="Recommendations",
            tab_id="tab-recommend",
            children=[
                html.Br(),
                html.H4("Recommended Forts"),
                # Nearby
                html.H5("Nearby Forts"),
                html.Div(
                    "Results will appear here...",
                    id="nearby-container",
                    className="mb-4 text-muted",
                ),
                # Similar
                html.H5("Similar Forts"),
                html.Div(
                    "Results will appear here...",
                    id="similar-container",
                    className="text-muted",
                ),
            ],
        ),
        # Insights Tab
        dbc.Tab(
            label="Insights",
            tab_id="tab-insights",
            children=[
                html.Br(),
                html.H4("Cluster Insights"),
                html.Div(
                    "Cluster charts will appear here...",
                    id="cluster-container",  # NOQA E501
                    className="text-muted",
                ),
            ],
        ),
        # RAG Q/A Tab
        dbc.Tab(
            label="Q&A",
            tab_id="tab-qa",
            children=[
                html.Br(),
                html.H4("Ask a question about Maharashtra Forts"),
                dbc.Input(
                    id="qa-input",
                    placeholder="Ask anything... e.g. 'Which forts were important during the Maratha Empire?'",  # NOQA E501
                    type="text",
                    className="mb-3",
                ),
                dbc.Button("Search", id="qa-btn", color="primary", className="mb-3"),
                html.Div(
                    id="qa-output",
                    children="Answers will appear here...",
                    className="text-muted",
                ),
            ],
        ),
    ],
    id="main-tabs",
    active_tab="tab-explore",
)

# ----------------------------------------------------------------
# Layout Grid
# ----------------------------------------------------------------
app.layout = dbc.Container(
    fluid=True,
    children=[header, dbc.Row([dbc.Col(sidebar, width=3), dbc.Col(tabs, width=9)])],
)


@app.callback(
    Output("filter-district", "options"),
    Output("filter-type", "options"),
    Output("filter-difficulty", "options"),
    Output("filter-season", "options"),
    Input("main-tabs", "value"),  # triggers once on page render
)
def load_filters(_):
    forts = get_forts()

    districts = sorted({f["district"] for f in forts})
    types = sorted({f["type"] for f in forts})
    difficulty = sorted({f["trek_difficulty"] for f in forts})
    seasons = sorted({f["best_season"] for f in forts})

    return (
        [{"label": d, "value": d} for d in districts],
        [{"label": t, "value": t} for t in types],
        [{"label": d, "value": d} for d in difficulty],
        [{"label": s, "value": s} for s in seasons],
    )


@app.callback(
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

    forts = get_forts(params)

    if not forts:
        return html.Div("No forts found.", className="text-muted")

    cards = []
    for f in forts:
        cards.append(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(f["name"], className="fw-bold"),
                        html.P(f"{f['district']} • {f['type']}"),
                        html.Small(f"Trek: {f['trek_difficulty']}"),
                    ]
                ),
                className="mb-3 shadow-sm",
            )
        )

    return cards


@app.callback(
    Output("nearby-container", "children"),
    Input("selected-lat", "data"),
    Input("selected-lon", "data"),
)
def load_nearby(lat, lon):
    if not lat or not lon:
        return "Select a fort first."

    res = get_nearby(lat, lon, k=5)
    return [html.P(f["name"]) for f in res]


@app.callback(
    Output("similar-container", "children"), Input("selected-fort-id", "data")
)
def load_similar(fort_id):
    if not fort_id:
        return "Select a fort first."

    res = get_similar(fort_id, k=5)
    return [html.P(f["name"]) for f in res]


@app.callback(Output("cluster-container", "children"), Input("main-tabs", "value"))
def load_cluster_info(tab):
    if tab != "tab-insights":
        return dash.no_update

    clusters = get_clusters()
    return html.Pre(str(clusters))


@app.callback(
    Output("qa-output", "children"),
    Input("qa-btn", "n_clicks"),
    State("qa-input", "value"),
)
def perform_qa(n, query):
    if not n:
        return dash.no_update
    if not query:
        return "Please enter a question."

    answers = rag_query(query)
    return [
        html.Div(
            [
                html.H6(a["name"], className="fw-bold"),
                html.P(a["notes"] or "No notes available"),
            ]
        )
        for a in answers
    ]


# ----------------------------------------------------------------
# Dash Starter (for local debugging)
# ----------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=False)
