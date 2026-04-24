from dash import html, dcc
import dash_bootstrap_components as dbc


def create_header():
    return dbc.Container(
        [
            html.Br(),
            html.H2("🏰 Pride of Sahyadri", className="text-white mb-0",
                    style={'textAlign': 'center'}),
            html.Br(),
        ], style={'backgroundColor': '#554124'}, fluid=True
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
                , style={"color": "#FFFFFF", "backgroundColor": "#3C2515"}
            ),
            # Type Filter
            html.Label("Fort Type"),
            dcc.Dropdown(
                id="filter-type", placeholder="Select fort type", className="mb-2"  # NOQA E501
                , style={"color": "#FFFFFF", "backgroundColor": "#3C2515"}
            ),
            # Difficulty Filter
            html.Label("Trek Difficulty"),
            dcc.Dropdown(
                id="filter-difficulty",
                placeholder="Select difficulty",
                className="mb-2",
                style={"color": "#FFFFFF", "backgroundColor": "#3C2515"}
            ),
            # Season Filter
            html.Label("Best Season"),
            dcc.Dropdown(
                id="filter-season", placeholder="Select season", className="mb-4"  # NOQA E501
                , style={"color": "#FFFFFF", "backgroundColor": "#3C2515"}
            ),
            # Reset Button
            dbc.Button(
                "Reset Filters",
                id="reset-btn",
                style={"color": "#FFFFFF", "backgroundColor": "#3C2515"}
            ),
        ],
        body=True,
        style={
            "color": "#FFFFFF",
            "backgroundColor": "#23904F",
            "height": "100vh",
            "overflowY": "auto",
        },
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
                    html.H4("Explore Forts", className="text-center"),  # NOQA E501
                    html.Div(id="fort-list", className="mt-3"),
                ], style={"color": "#3C2515"}
            ),
            # ======================================================
            # Recommendations Tab
            # ======================================================
            dbc.Tab(
                label="Recommendations",
                tab_id="tab-recommend",
                children=[
                    html.Br(),
                    html.H4("Recommended Forts", className="text-center"),  # NOQA E501
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
                ], style={"color": "#3C2515"}
            ),
            # ================================
            # Insights Tab
            # ================================
            dbc.Tab(
                label="Insights",
                tab_id="tab-insights",
                children=[
                    html.Br(),
                    html.H3("Fort Insights", className="text-center mb-4"),  # NOQA E501
                    dbc.Container(
                        [

                            # -------- Insight Output --------
                            html.Div(
                                id="insight-output",
                                className="mt-3"
                            ),

                        ],
                        fluid=True,
                    ),
                ], style={"color": "#3C2515"}
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
                        , style={"color": "#FFFFFF", "backgroundColor": "#3C2515"} # NOQA E501
                    ),
                    html.Div(id="qa-output", className="text-muted"),
                ], style={"color": "#3C2515"}
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
        ],  style={"backgroundColor": "#47DA74"}
    )
