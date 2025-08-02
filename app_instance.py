import dash
import dash_bootstrap_components as dbc

# Criação única da instância do app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
app.title = "BI PPGC"
