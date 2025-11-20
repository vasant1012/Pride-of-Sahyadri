import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MINTY],
    title="Pride of Sahyadri"
)

# ----------------------------------------------------------------
# Header Section
# ----------------------------------------------------------------
header = dbc.Navbar(
    dbc.Container([
        html.H2("🏰 Pride of Sahyadri", className="text-white mb-0"),
    ]),
    color="dark",
    className="mb-4", style={"textAlign": "center"}
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
            className="mb-2"
        ),

        # Fort type
        html.Label("Fort Type"),
        dcc.Dropdown(
            id="filter-type",
            placeholder="Select fort type",
            multi=False,
            className="mb-2"
        ),

        # Trek difficulty
        html.Label("Trek Difficulty"),
        dcc.Dropdown(
            id="filter-difficulty",
            placeholder="Select difficulty",
            multi=False,
            className="mb-2"
        ),

        # Season filter
        html.Label("Best Season"),
        dcc.Dropdown(
            id="filter-season",
            placeholder="Select season",
            multi=False,
            className="mb-4"
        ),

        # dbc.Button("Reset Filters", id="reset-btn",
        #            color="secondary", block=True)
        dbc.Button(
            "Reset Filters",
            id="reset-btn",
            color="secondary",
            className="w-100"   # full width
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
                    children=html.Div("Map will load here...",
                                      className="text-muted"),
                    style={"height": "400px", "background": "#f8f9fa",
                           "border": "1px solid #ddd"},
                    className="mb-4"
                ),

                # Fort card list placeholder
                html.Div(
                    id="fort-list",
                    children=[
                        html.Div("Fort list will appear here...",
                                 className="text-muted")
                    ],
                ),
            ]
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
                html.Div("Results will appear here...", id="nearby-container",
                         className="mb-4 text-muted"),

                # Similar
                html.H5("Similar Forts"),
                html.Div("Results will appear here...", id="similar-container",
                         className="text-muted"),
            ]
        ),

        # Insights Tab
        dbc.Tab(
            label="Insights",
            tab_id="tab-insights",
            children=[
                html.Br(),
                html.H4("Cluster Insights"),

                html.Div("Cluster charts will appear here...", id="cluster-container", # NOQA E501
                         className="text-muted")
            ]
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
                    placeholder="Ask anything... e.g. 'Which forts were important during the Maratha Empire?'", # NOQA E501
                    type="text",
                    className="mb-3"
                ),

                dbc.Button("Search", id="qa-btn",
                           color="primary", className="mb-3"),

                html.Div(id="qa-output",
                         children="Answers will appear here...",
                         className="text-muted")
            ]
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
    children=[
        header,

        dbc.Row([
            dbc.Col(sidebar, width=3),
            dbc.Col(tabs, width=9)
        ])
    ]
)

# ----------------------------------------------------------------
# Dash Starter (for local debugging)
# ----------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=False)
