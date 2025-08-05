import dash_bootstrap_components as dbc
from dash import html

# Sidebar recolhível
sidebar = html.Div(
    id="sidebar",  # ID necessário para controlar via callback
    
    children=[
        html.H2("Menu", className="display-5", style={"color": "#E88032", "padding": "10px"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Projetos", href="/projetos", active="exact", style={"color": "#E88032", "padding": "10px"}),
                dbc.NavLink("Processos", href="/processos", active="exact", style={"color": "#E88032", "padding": "10px"}),
                dbc.NavLink("Compliance", href="https://app.powerbi.com/groups/897b27a6-6ec1-476e-961c-a780cf4c1493/reports/0bc6ce78-dbd3-4c05-9486-2129d7009d61/1f7e8b154a13bc197669?experience=power-bi",external_link=True, target="_blank", style={"color": "#E88032", "padding": "10px"}),
                dbc.NavLink("Ambiental", href="/ambiental", active="exact", style={"color": "#E88032", "padding": "10px"}),
                dbc.NavLink("Análise IA", href="/ia", active="exact", style={"color": "#E88032", "padding": "10px"}),
                dbc.NavLink("Planejamento", href="/planejamento", active="exact", style={"color": "#E88032", "padding": "10px"}),
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
