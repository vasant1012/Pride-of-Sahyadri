from dash import html, dcc
import dash_bootstrap_components as dbc


def create_header():
    return dbc.Navbar(
        dbc.Container(
            [
                html.H2("🏰 Pride of Sahyadri", className="text-white mb-0"),
            ]
        ),
        color="dark",
        className="mb-4",
    )


def create_sidebar():
    return dbc.Card(
        [
            html.H5("🔎 Search & Filters", className="card-title"),
            html.Hr(),
            # Search Bar
            dbc.Input(
                id="search-input",
                type="text",
                placeholder="Search forts by name or keyword...",
                className="mb-3",
            ),
            # District Filter
            html.Label("District"),
            dcc.Dropdown(
                id="filter-district", placeholder="Select district", className="mb-2"
            ),
            # Type Filter
            html.Label("Fort Type"),
            dcc.Dropdown(
                id="filter-type", placeholder="Select fort type", className="mb-2"
            ),
            # Difficulty Filter
            html.Label("Trek Difficulty"),
            dcc.Dropdown(
                id="filter-difficulty",
                placeholder="Select difficulty",
                className="mb-2",
            ),
            # Season Filter
            html.Label("Best Season"),
            dcc.Dropdown(
                id="filter-season", placeholder="Select season", className="mb-4"
            ),
            # Reset Button
            dbc.Button(
                "Reset Filters",
                id="reset-btn",
                color="secondary",
                className="w-100 mb-3",
            ),
        ],
        body=True,
        style={"height": "100vh", "overflowY": "auto"},
    )


def create_tabs():
    return dbc.Tabs(
        id="main-tabs",
        active_tab="tab-explore",
        children=[
            # ======================================================
            # Explore Tab
            # ======================================================
            dbc.Tab(
                label="Explore",
                tab_id="tab-explore",
                children=[
                    html.Br(),
                    html.H4("Explore Forts", className="text-center"),
                    html.Div(id="fort-list", className="mt-3"),
                ],
            ),
            # ======================================================
            # Recommendations Tab
            # ======================================================
            dbc.Tab(
                label="Recommendations",
                tab_id="tab-recommend",
                children=[
                    html.Br(),
                    html.H4("Recommended Forts", className="text-center"),
                    html.Div(
                        [
                            html.Label("Selected Fort:"),
                            html.Div(
                                id="recommend-selected-name",
                                className="mb-2 text-muted",
                            ),
                        ]
                    ),
                    html.H5("Nearby Forts"),
                    html.Div(id="nearby-container", className="text-muted mb-4"),
                    html.H5("Similar Forts"),
                    html.Div(id="similar-container", className="text-muted"),
                ],
            ),
            # ================================
            # Cluster Analysis Tab
            # ================================
            dbc.Tab(
                label="Cluster Analysis",
                tab_id="tab-cluster",
                children=[
                    html.Br(),
                    html.H3("ML Cluster Analysis", className="text-center mb-4"),

                    # -------- Summary Cards --------
                    dbc.Row([
                        dbc.Col(dbc.Card(dbc.CardBody([
                            html.H6("Total Clusters"),
                            html.H3(id="ca-total-clusters")
                        ])), width=3),

                        dbc.Col(dbc.Card(dbc.CardBody([
                            html.H6("Largest Cluster"),
                            html.H4(id="ca-largest-cluster")
                        ])), width=4),

                        dbc.Col(dbc.Card(dbc.CardBody([
                            html.H6("Smallest Cluster"),
                            html.H4(id="ca-smallest-cluster")
                        ])), width=4),
                    ], className="mb-4"),

                    # -------- Charts Row 1 --------
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="ca-bar"), width=6),
                        dbc.Col(dcc.Graph(id="ca-pie"), width=6),
                    ], className="mb-4"),

                    # -------- Charts Row 2 --------
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="ca-scatter-elev"), width=6),
                        dbc.Col(dcc.Graph(id="ca-scatter-time"), width=6),
                    ], className="mb-4"),

                    # -------- Cluster Profile Table --------
                    html.H4("Cluster Profile Summary", className="mt-4"),
                    html.Div(id="ca-cluster-profile"),
                ],
            ),
            # ======================================================
            # Q&A Tab
            # ======================================================
            dbc.Tab(
                label="Q&A",
                tab_id="tab-qa",
                children=[
                    html.Br(),
                    html.H4(
                        "Ask a question about Maharashtra Forts",
                        className="text-center",
                    ),
                    dbc.Input(
                        id="qa-input",
                        placeholder="Ask anything...",
                        type="text",
                        className="mb-3",
                    ),
                    dbc.Button(
                        "Search", id="qa-btn", color="primary", className="mb-3"
                    ),
                    html.Div(id="qa-output", className="text-muted"),
                ],
            ),
        ],
    )


def create_layout():
    return dbc.Container(
        fluid=True,
        children=[
            create_header(),
            # Store for selected fort
            dcc.Store(id="selected-fort-id"),
            dbc.Row(
                [
                    dbc.Col(create_sidebar(), width=3),
                    dbc.Col(create_tabs(), width=9),
                ]
            ),
        ],
    )
