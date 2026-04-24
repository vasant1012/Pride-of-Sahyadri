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
                id="filter-district", placeholder="Select district", className="mb-2"  # NOQA E501
            ),
            # Type Filter
            html.Label("Fort Type"),
            dcc.Dropdown(
                id="filter-type", placeholder="Select fort type", className="mb-2"  # NOQA E501
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
                id="filter-season", placeholder="Select season", className="mb-4"  # NOQA E501
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
                    html.Div(id="nearby-container",
                             className="text-muted mb-4"),
                    html.H5("Similar Forts"),
                    html.Div(id="similar-container", className="text-muted"),
                ],
            ),
            # ================================
            # Insights Tab
            # ================================
            dbc.Tab(
                label="Insights",
                tab_id="tab-insights",
                children=[
                    html.Br(),
                    html.H3("Fort Insights", className="text-center mb-4"),

                    dbc.Container(
                        [

                            # -------- Fort Selector --------
                            html.Label("Select Fort"),
                            dcc.Dropdown(
                                id="insight-fort-dropdown",
                                placeholder="Select a fort to view insights",
                                className="mb-4",
                            ),

                            # -------- Insight Output --------
                            html.Div(
                                id="insight-output",
                                className="mt-3"
                            ),

                        ],
                        fluid=True,
                    ),
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
                        "Search", id="qa-btn", color="primary", className="mb-3"  # NOQA E501
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
