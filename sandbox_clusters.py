import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output
import pandas as pd
import plotly.express as px

from src.frontend.api_client import api

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    html.H2("Cluster Analysis Dashboard"),

    html.Button("Load Clusters", id="load-btn",
                className="btn btn-primary mt-3"),
    html.Div(id="cluster-stats", className="mt-4"),

    dcc.Graph(id="cluster-bar"),
    dcc.Graph(id="cluster-pie"),
    dcc.Graph(id="cluster-scatter"),

], fluid=True)


@app.callback(
    Output("cluster-stats", "children"),
    Output("cluster-bar", "figure"),
    Output("cluster-pie", "figure"),
    Output("cluster-scatter", "figure"),
    Input("load-btn", "n_clicks"),
)
def load_cluster_analysis(n):
    if not n:
        raise dash.exceptions.PreventUpdate

    clusters = api.get_clusters() or {}
    forts = api.get_clustered_forts() or []
    df = pd.DataFrame(forts)

    # Summary
    stats = html.Div([
        html.P(f"Total Clusters: {len(clusters)}"),
        html.P(f"Cluster Counts: {clusters}")
    ])

    # Bar chart
    fig_bar = px.bar(
        x=list(clusters.keys()),
        y=list(clusters.values()),
        labels={"x": "Cluster", "y": "Count"},
        title="Forts Per Cluster"
    )

    # Pie chart
    fig_pie = px.pie(
        names=list(clusters.keys()),
        values=list(clusters.values()),
        title="Cluster Distribution"
    )

    # Scatter
    fig_scatter = px.scatter(
        df,
        x="elevation_m",
        y="trek_time_hours",
        color="cluster",
        hover_data=["name", "district"],
        title="Elevation vs Trek Time"
    )

    return stats, fig_bar, fig_pie, fig_scatter


if __name__ == "__main__":
    app.run_server(debug=True, port=8053)
