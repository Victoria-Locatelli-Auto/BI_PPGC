import pandas as pd
from dash import dcc, html, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app_instance import app

# Cores do tema
COR_FUNDO = "#121E26"
COR_CARD = "#192A35"
COR_TEXTO = "#C2E0E7"
COR_GRAFICO = px.colors.sequential.Oranges

# Carregar dados
df = pd.read_excel("Projetos.xlsx")

# Garantir que a coluna '% Concluído' seja numérica
df["% Concluído"] = pd.to_numeric(df["% Concluído"], errors='coerce')

# Layout da página
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("B.I PPGC - PROJETOS", className="text-center fw-bold text-light mb-4"))
    ]),

    dbc.Row([
        # Filtros laterais
        dbc.Col([
            html.Div([
                html.Label("Status", className="fw-bold text-light"),
                dcc.Dropdown(
                    options=[{"label": s, "value": s} for s in sorted(df['Status'].dropna().unique())],
                    id="filtro-status",
                    placeholder="Todos",
                    multi=True,
                    className="mb-3"
                ),
            ], style={"backgroundColor": COR_CARD, "padding": "20px", "borderRadius": "10px"})
        ], width=2),

        # Conteúdo principal: tabela + gráficos
        dbc.Col([
            dbc.Card(
                dash_table.DataTable(
                    id="tabela-projetos",
                    columns=[
                        {"name": "ID", "id": "ID"},
                        {"name": "Nome do Projeto", "id": "Nome do Projeto"},
                        {"name": "Início", "id": "Início"},
                        {"name": "Status", "id": "Status"},
                        {"name": "% Concluído", "id": "% Concluído", "type": "numeric"},
                    ],
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'center',
                        'backgroundColor': COR_CARD,
                        'color': COR_TEXTO,
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    },
                    style_header={
                        'fontWeight': 'bold',
                        'backgroundColor': "#263640",
                        'color': COR_TEXTO
                    },
                    
                ),
                style={
                    "backgroundColor": COR_CARD,
                    "borderRadius": "15px",
                    "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                    "padding": "10px",
                    "marginBottom": "20px"
                }
            ),

            dbc.Row([
                # Gráfico de Rosca (Status)
                dbc.Col(
                    dbc.Card(
                        dcc.Graph(id="grafico-distribuicao"),
                        style={
                            "backgroundColor": COR_CARD,
                            "borderRadius": "15px",
                            "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                            "padding": "10px",
                            "marginBottom": "20px"
                        }
                    ),
                    width=6
                ),
                # Gráfico de Barras (Status)
                dbc.Col(
                    dbc.Card(
                        dcc.Graph(id="grafico-status"),
                        style={
                            "backgroundColor": COR_CARD,
                            "borderRadius": "15px",
                            "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                            "padding": "10px",
                            "marginBottom": "20px"
                        }
                    ),
                    width=6
                )
            ]),

            dbc.Row([
                # Gráfico Percentual de Conclusão
                dbc.Col(
                    dbc.Card(
                        dcc.Graph(id="grafico-percentual"),
                        style={
                            "backgroundColor": COR_CARD,
                            "borderRadius": "15px",
                            "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                            "padding": "10px",
                            "marginBottom": "20px"
                        }
                    ),
                    width=12
                )
            ])
        ], width=10)
    ])
], fluid=True, style={"backgroundColor": COR_FUNDO, "minHeight": "100vh", "padding": "20px"})

# CALLBACKS

@app.callback(
    Output("tabela-projetos", "data"),
    Input("filtro-status", "value")
)
def filtrar_tabela(f_status):
    dff = df.copy()
    if f_status:
        dff = dff[dff['Status'].isin(f_status)]
    return dff.to_dict('records')

@app.callback(
    Output("grafico-status", "figure"),
    Output("grafico-distribuicao", "figure"),
    Output("grafico-percentual", "figure"),
    Input("tabela-projetos", "data"),
)
def atualizar_graficos(dados_tabela):
    df_filtrado = pd.DataFrame(dados_tabela)

    if df_filtrado.empty:
        empty_fig = px.scatter()
        empty_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=COR_TEXTO,
            title_font_size=16,
            title_x=0.5,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(size=12)
        )
        return empty_fig, empty_fig, empty_fig

    # Contagem status para gráfico de barras
    contagem_status = df_filtrado["Status"].value_counts().reset_index()
    contagem_status.columns = ["Status", "Quantidade"]

    fig_status = px.bar(
        contagem_status,
        x="Status",
        y="Quantidade",
        labels={"Status": "Status", "Quantidade": "Quantidade"},
        title="Composição de Status dos Projetos",
        color_discrete_sequence=["#FB8C00", "#FB8C00", "#F57C00", "#EF6C00", "#E65100"]
    )

    fig_distribuicao = px.pie(
        df_filtrado,
        names="Status",
        hole=0.5,
        title="Distribuição de Projetos por Status",
        color_discrete_sequence=["#FFA726", "#FB8C00", "#F57C00", "#EF6C00", "#E65100"]
    )

    fig_percentual = px.bar(
        df_filtrado,
        x="Nome do Projeto",
        y="% Concluído",
        title="Percentual de Conclusão por Projeto",
        color_discrete_sequence=COR_GRAFICO
    )
    fig_percentual.update_layout(xaxis_tickangle=-45)

    for fig in [fig_status, fig_distribuicao, fig_percentual]:
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color=COR_TEXTO,
            title_font_size=16,
            title_x=0.5,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(size=12)
        )

    return fig_status, fig_distribuicao, fig_percentual
