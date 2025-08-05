from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app_instance import app
from sidebar import sidebar
import BI_projetos
import BI_processos
import ambiental

# Conteúdo principal da página
content = html.Div(
    id="page-content",
    style={
        "margin-left": "18rem",
        "padding": "2rem 1rem",
        "transition": "margin-left 0.3s"
    }
)

# Layout principal do app
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        content
    ],
    style={
        "backgroundImage": "url('/assets/background.jpg')",
        "backgroundSize": "cover",
        "backgroundRepeat": "no-repeat",
        "backgroundPosition": "center",
        "minHeight": "100vh",
        "overflow": "hidden"  # remove o scroll
    }
)

# Callback para recolher/expandir a sidebar
@app.callback(
    Output("sidebar", "style"),
    Output("page-content", "style"),
    Input("btn-toggle", "n_clicks"),
    State("sidebar", "style"),
    State("page-content", "style"),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, sidebar_style, content_style):
    is_open = sidebar_style.get("left") == "0rem"
    if is_open:
        sidebar_style["left"] = "-16rem"
        content_style["margin-left"] = "0rem"
    else:
        sidebar_style["left"] = "0rem"
        content_style["margin-left"] = "18rem"
    return sidebar_style, content_style

# Callback de navegação entre páginas
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/projetos":
        return BI_projetos.layout
    elif pathname == "/processos":
        return BI_processos.layout
    elif pathname == "/ambiental":
        return ambiental.layout  # usa o layout definido em ambiental.py
    else:
        # Página inicial com imagem de fundo full screen
        return html.Div(
            html.Img(
                src="/assets/home.png",
                style={
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "width": "100%",
                    "height": "100%",
                    "objectFit": "cover",
                    "zIndex": "0"
                }
            ),
            style={
                "position": "relative",
                "width": "100%",
                "height": "100vh",
                "overflow": "hidden",
                "padding": "0",
                "margin": "0"
            }
        )

# Rodar o servidor acessível por IP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
