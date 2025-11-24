import dash
import dash_bootstrap_components as dbc
from src.frontend.layout import create_layout
import src.frontend.callbacks  # noqa: F401 (registers callbacks on import)


# ============================
# Dash App Initialization
# ============================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    title="Pride of Sahyadri",
)


# Assign layout
app.layout = create_layout()


# Expose server to run.py
server = app.server
