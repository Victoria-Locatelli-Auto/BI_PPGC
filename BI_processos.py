import pandas as pd
from dash import dcc, html, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app_instance import app

# Carregar dados
df = pd.read_excel("processos.xlsx")
df["% Concluído"] = pd.to_numeric(df["% Concluído"], errors='coerce')

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("B.I PPGC - PROCESSOS", className="text-center fw-bold text-light mb-4"))
    ]),

    dbc.Row([
        # Sidebar
        dbc.Col([
            html.Div([
                html.Label("Setor", className="fw-bold text-light"),
                dcc.Dropdown(
                    options=[{"label": s, "value": s} for s in sorted(df['Setores mapeados'].dropna().unique())],
                    id="filtro-setor-processos", placeholder="Todos", multi=True, className="mb-3"
                ),
                html.Label("Responsável", className="fw-bold text-light"),
                dcc.Dropdown(
                    options=[{"label": r, "value": r} for r in sorted(df['Responsável'].dropna().unique())],
                    id="filtro-responsavel-processos", placeholder="Todos", multi=True, className="mb-3"
                ),
                html.Label("Status Entrega", className="fw-bold text-light"),
                dcc.Dropdown(
                    options=[{"label": e, "value": e} for e in sorted(df['Status'].dropna().unique())],
                    id="filtro-status-processos", placeholder="Todos", multi=True
                )
            ], style={"backgroundColor": "#0E1A21", "padding": "20px", "borderRadius": "10px"})
        ], width=2),

        # Conteúdo principal
        dbc.Col([
            # Tabela
            dbc.Card(
                dash_table.DataTable(
                    id="tabela-processos",
                    columns=[
                        {"name": "ID", "id": "ID"},
                        {"name": "Setores mapeados", "id": "Setores mapeados"},
                        {"name": "Atividades mapeadas por setor", "id": "Atividades mapeadas"},
                        {"name": "Instruções feitas pelo setor", "id": "Instruçoes feitas"},
                        {"name": "Instruções reestruturadas", "id": "Instruçoes reestruturadas"},
                        {"name": "Entrevistados", "id": "Qtd colaboradores entrevistados"},
                        {"name": "% Concluído", "id": "% Concluído", "type": "numeric"},
                        {"name": "Status Entrega", "id": "Status"},
                        {"name": "Etapa / Entrega", "id": "Etapa / Entrega"},
                    ],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'center', 'backgroundColor': '#192A35', 'color': '#C2E0E7', 'whiteSpace': 'normal', 'height': 'auto'},
                    style_header={'fontWeight': 'bold', 'backgroundColor': '#263640', 'color': '#C2E0E7'},
                ),
                style={
                    "backgroundColor": "#192A35",
                    "borderRadius": "15px",
                    "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                    "padding": "10px",
                    "marginBottom": "20px"
                }
            ),

            # Gráficos
            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id="grafico-atividades-processos"), style={
                    "backgroundColor": "#192A35",
                    "borderRadius": "15px",
                    "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                    "padding": "10px",
                    "marginBottom": "20px"
                }), width=6),
                dbc.Col(dbc.Card(dcc.Graph(id="grafico-instrucoes-processos"), style={
                    "backgroundColor": "#192A35",
                    "borderRadius": "15px",
                    "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                    "padding": "10px",
                    "marginBottom": "20px"
                }), width=6),
            ]),

            dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id="grafico-entregas-processos"), style={
                    "backgroundColor": "#192A35",
                    "borderRadius": "15px",
                    "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                    "padding": "10px",
                    "marginBottom": "20px"
                }), width=6),
                dbc.Col(dbc.Card(dcc.Graph(id="grafico-status-processos"), style={
                    "backgroundColor": "#192A35",
                    "borderRadius": "15px",
                    "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                    "padding": "10px",
                    "marginBottom": "20px"
                }), width=6),
            ])
        ], width=10)
    ])
], fluid=True, style={"backgroundColor": "#121E26", "minHeight": "100vh", "padding": "20px"})


# CALLBACKS
@app.callback(
    Output("tabela-processos", "data"),
    Output("grafico-atividades-processos", "figure"),
    Output("grafico-instrucoes-processos", "figure"),
    Output("grafico-entregas-processos", "figure"),
    Output("grafico-status-processos", "figure"),
    Input("filtro-setor-processos", "value"),
    Input("filtro-responsavel-processos", "value"),
    Input("filtro-status-processos", "value")
)
def atualizar_tudo(f_setor, f_resp, f_status):
    dff = df.copy()
    if f_setor:
        dff = dff[dff['Setores mapeados'].isin(f_setor)]
    if f_resp:
        dff = dff[dff['Responsável'].isin(f_resp)]
    if f_status:
        dff = dff[dff['Status'].isin(f_status)]

    tabela = dff.to_dict('records')

    # Gráfico Atividades Mapeadas por Setor
    fig_ativ = px.bar(
        dff, x='Setores mapeados', y='Atividades mapeadas',
        title="Atividades Mapeadas por Setor", color='Setores mapeados',
        text_auto=True, color_discrete_sequence=px.colors.sequential.Teal
    )

    # Gráfico Instruções Reestruturadas
    fig_instr = px.bar(
        dff, x='Instruçoes reestruturadas', y='Status', orientation='h',
        title="Instr. Reestruturadas por Status", color='Status',
        color_discrete_sequence=px.colors.sequential.Teal
    )

    # Gráfico Entregas Concluídas por Etapa
    fig_entregas = px.bar(
        dff, x='Etapa / Entrega', title="Entregas Concluídas",
        color='Etapa / Entrega',
        color_discrete_sequence=px.colors.sequential.Teal
    )

    # Gráfico Composição Status
    fig_status = px.pie(
        dff, names='Status', hole=0.5,
        title="Composição Status",
        color_discrete_sequence=px.colors.sequential.Teal
    )

    # Estilo dos Gráficos (Dark Theme)
    for fig in [fig_ativ, fig_instr, fig_entregas, fig_status]:
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#C2E0E7",
            title_font_size=16,
            title_x=0.5,
            margin=dict(l=20, r=20, t=50, b=20),
            font=dict(size=12)
        )

    return tabela, fig_ativ, fig_instr, fig_entregas, fig_status
