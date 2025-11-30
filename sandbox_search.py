import dash
from dash import html, Input, Output
import dash_bootstrap_components as dbc

from src.frontend.api_client import api

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container(
    [
        html.H2("Ask About Maharashtra Forts"),
        html.Br(),
        dbc.Input(
            type="text",
            id="qa-input",
            placeholder="Ask a question about forts...",
            style={"Height": "40px", "padding": "10px"},
        ),
        html.Br(),
        html.Button("Click for answer!", id="qa-btn", className="btn btn-primary ms-3"),
        html.Div(id="qa-output", className="mt-4", style={"padding": "10px"}),
    ],
    fluid=True,
    style={"text-align": "center"},
)


@app.callback(
    Output("qa-output", "children"),
    Input("qa-btn", "n_clicks"),
    Input("qa-input", "value"),
)
def ask(n, question):
    if not n:
        raise dash.exceptions.PreventUpdate

    if not question:
        return "Please enter a question."

    answers = api.rag_query(question)
    if not answers:
        return "No results found."

    return html.Div([
        html.Hr(),
        dbc.Card(
            dbc.CardBody([html.H6(answers)]),
            className="mb-3",
            style={"backgroundColor": "#82edb8"},
        ),
        html.Hr(),]
    )


if __name__ == "__main__":
    app.run_server(debug=False, port=8070)
