import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import requests

# =============================
# API Client Helpers
# =============================
API_BASE = "http://localhost:8000"


def get_forts(params=None):
    return requests.get(f"{API_BASE}/forts", params=params).json()


def get_fort(fort_id):
    return requests.get(f"{API_BASE}/forts/{fort_id}").json()


def rag_query(q):
    return requests.get(f"{API_BASE}/search/semantic_search", params={"q": q}).json()


def get_clusters():
    return requests.get(f"{API_BASE}/clusters").json()


def predict_cluster(lat, lon):
    return requests.get(
        f"{API_BASE}/clusters/predict", params={"lat": lat, "lon": lon}
    ).json()


def get_nearby(lat, lon, k=5):
    return requests.get(
        f"{API_BASE}/recommend/nearby", params={"lat": lat, "lon": lon, "k": k}
    ).json()


def get_similar(fort_id, k=5):
    return requests.get(
        f"{API_BASE}/recommend/similar/{fort_id}", params={"k": k}
    ).json()


# =============================
# Dash App Initialization
# =============================
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Pride of Sahyadri"
)

# =============================
# Layout Components
# =============================
header = dbc.Navbar(
    dbc.Container([html.H2("🏰 Pride of Sahyadri", className="text-white mb-0")]),
    color="dark",
    className="mb-4",
)

sidebar = dbc.Card(
    [
        html.H5("🔎 Search & Filters", className="card-title"),
        html.Hr(),
        dbc.Input(
            id="search-input",
            type="text",
            placeholder="Search forts...",
            className="mb-3",
        ),
        html.Label("District"),
        dcc.Dropdown(
            id="filter-district", placeholder="Select district", className="mb-2"
        ),
        html.Label("Fort Type"),
        dcc.Dropdown(
            id="filter-type", placeholder="Select fort type", className="mb-2"
        ),
        html.Label("Trek Difficulty"),
        dcc.Dropdown(
            id="filter-difficulty", placeholder="Select difficulty", className="mb-2"
        ),
        html.Label("Best Season"),
        dcc.Dropdown(id="filter-season", placeholder="Select season", className="mb-4"),
        dbc.Button(
            "Reset Filters", id="reset-btn", color="secondary", className="w-100 mb-3"
        ),
    ],
    body=True,
    style={"height": "100vh", "overflowY": "auto"},
)

tabs = dbc.Tabs(
    [
        dbc.Tab(
            label="Explore",
            tab_id="tab-explore",
            children=[
                html.Br(),
                html.H4("Explore Forts", className="text-center"),
                html.Div(
                    id="fort-list",
                    children="Fort list will appear here...",
                    className="mt-3",
                ),
            ],
        ),
        dbc.Tab(
            label="Recommendations",
            tab_id="tab-recommend",
            children=[
                html.Br(),
                html.H4("Recommended Forts", className="text-center"),
                html.H5("Nearby Forts"),
                html.Div(id="nearby-container", className="text-muted mb-4"),
                html.H5("Similar Forts"),
                html.Div(id="similar-container", className="text-muted"),
            ],
        ),
        dbc.Tab(
            label="Insights",
            tab_id="tab-insights",
            children=[
                html.Br(),
                html.H4("Cluster Insights", className="text-center"),
                html.Div(id="cluster-container", className="text-muted"),
            ],
        ),
        dbc.Tab(
            label="Q&A",
            tab_id="tab-qa",
            children=[
                html.Br(),
                html.H4(
                    "Ask a question about Maharashtra Forts", className="text-center"
                ),
                dbc.Input(
                    id="qa-input",
                    placeholder="Ask anything...",
                    type="text",
                    className="mb-3",
                ),
                dbc.Button("Search", id="qa-btn", color="primary", className="mb-3"),
                html.Div(id="qa-output", className="text-muted"),
            ],
        ),
    ],
    id="main-tabs",
    active_tab="tab-explore",
)

app.layout = dbc.Container(
    fluid=True,
    children=[header, dbc.Row([dbc.Col(sidebar, width=3), dbc.Col(tabs, width=9)])],
)


# =============================
# Callbacks
# =============================
@app.callback(
    Output("filter-district", "options"),
    Output("filter-type", "options"),
    Output("filter-difficulty", "options"),
    Output("filter-season", "options"),
    Input("main-tabs", "active_tab"),
)
def load_filters(_):
    forts = get_forts()

    return (
        [{"label": d, "value": d} for d in sorted({f["district"] for f in forts})],
        [{"label": t, "value": t} for t in sorted({f["type"] for f in forts})],
        [
            {"label": d, "value": d}
            for d in sorted({f["trek_difficulty"] for f in forts})
        ],
        [{"label": s, "value": s} for s in sorted({f["best_season"] for f in forts})],
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
    Input("filter-district", "value"),
)
def load_nearby(district):
    # Placeholder logic — replace with user-selected fort
    return "Nearby API integration ready."


@app.callback(
    Output("similar-container", "children"),
    Input("filter-type", "value"),
)
def load_similar(ftype):
    return "Similar forts API integration ready."


@app.callback(
    Output("cluster-container", "children"),
    Input("main-tabs", "tab_id"),
)
def load_clusters(tab):
    if tab != "tab-insights":
        return dash.no_update
    return str(get_clusters())


@app.callback(
    Output("qa-output", "children"),
    Input("qa-btn", "n_clicks"),
    State("qa-input", "value"),
)
def qa_callback(n, query):
    if not n:
        return dash.no_update
    if not query:
        return "Please enter a question."

    answers = rag_query(query)
    return [
        html.Div(
            [
                html.H6(a["name"], className="fw-bold"),
                html.P(a.get("notes") or "No notes available"),
            ]
        )
        for a in answers
    ]


# =============================
# Run App
# =============================
if __name__ == "__main__":
    app.run_server(debug=False)
