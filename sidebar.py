import dash_bootstrap_components as dbc
from dash import html

# Sidebar recolhível
sidebar = html.Div(
    id="sidebar",  # ID necessário para controlar via callback
    
    children=[
        html.H2("Menu", className="display-5", style={"color": "white", "padding": "10px"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("BI Projetos", href="/projetos", active="exact"),
                dbc.NavLink("BI Processos", href="/processos", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#00183F",
        "color": "white",
        "transition": "left 0.3s",
    },
)
