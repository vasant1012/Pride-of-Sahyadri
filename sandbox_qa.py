import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from src.frontend.api_client import api

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    html.H2("Ask About Maharashtra Forts"),

    dcc.Input(
        id="qa-input",
        type="text",
        placeholder="Ask a question about forts...",
        style={"width": "80%", "padding": "10px"}
    ),
    html.Button("Ask", id="qa-btn", className="btn btn-primary ms-3"),

    html.Div(id="qa-output", className="mt-4"),

], fluid=True)


@app.callback(
    Output("qa-output", "children"),
    Input("qa-btn", "n_clicks"),
    Input("qa-input", "value")
)
def ask(n, question):
    if not n:
        raise dash.exceptions.PreventUpdate

    if not question:
        return "Please enter a question."

    answers = api.rag_query(question)
    if not answers:
        return "No results found."

    cards = []
    for a in answers:
        cards.append(
            dbc.Card(
                dbc.CardBody([
                    html.H5(a.get("name", "-")),
                    html.P(a.get("notes", "")),
                ]), className="mb-3"
            )
        )

    return cards


if __name__ == "__main__":
    app.run_server(debug=True, port=8054)
