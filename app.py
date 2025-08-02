from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app_instance import app
from sidebar import sidebar
from BI_projetos import layout as projetos_layout
from BI_processos import layout as processos_layout  # Quando pronto

# Ícone de menu no topo
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Button("☰", id="btn-toggle", color="primary", className="me-2"),
   
    ]),
    
    dark=True,
    fixed="top",
    className="shadow-sm"
)

# Área de conteúdo
content = html.Div(id="page-content", style={"margin-left": "18rem", "padding": "2rem 1rem", "transition": "margin-left 0.3s"})

# Layout geral com navbar + sidebar + conteúdo
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    sidebar,
    content
])

# Callback: alternar visibilidade do menu
@app.callback(
    Output("sidebar", "style"),
    Output("page-content", "style"),
    Input("btn-toggle", "n_clicks"),
    State("sidebar", "style"),
    State("page-content", "style"),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, sidebar_style, content_style):
    # Detectar estado atual (visível ou oculto)
    is_open = sidebar_style.get("left") == "0rem"
    if is_open:
        # Ocultar sidebar
        sidebar_style["left"] = "-16rem"
        content_style["margin-left"] = "0rem"
    else:
        # Mostrar sidebar
        sidebar_style["left"] = "0rem"
        content_style["margin-left"] = "18rem"
    return sidebar_style, content_style

# Callback para trocar conteúdo da página
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/projetos":
        return projetos_layout
    elif pathname == "/processos":
        return processos_layout
    else:
        return dbc.Container([
            html.H1("404: Página não encontrada", className="text-danger"),
            html.Hr(),
            html.P(f"A página '{pathname}' não existe."),
        ], style={"margin-left": "18rem", "padding": "2rem 1rem"})

if __name__ == "__main__":
    app.run(debug=True)
