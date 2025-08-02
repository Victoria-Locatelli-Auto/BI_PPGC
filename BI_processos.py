import pandas as pd
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app_instance import app

# Carregar dados
df = pd.read_excel("processos.xlsx")
df["% Concluído"] = pd.to_numeric(df["% Concluído"], errors='coerce')

layout = dbc.Container([
    # Título centralizado
    dbc.Row([
        dbc.Col(html.H2("ANDAMENTO EQUIPE DE PROCESSOS", className="text-center text-dark fw-bold mb-4"))
    ]),

    # Filtros na lateral (estilizado como sidebar)
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Label("Setor", className="fw-bold text-white mb-1"),
                dcc.Dropdown(
                    options=[{"label": s, "value": s} for s in sorted(df['Setores mapeados'].dropna().unique())],
                    id="filtro-setor", placeholder="Todos", multi=True, className="mb-3"
                ),
                html.Label("Responsável", className="fw-bold text-white mb-1"),
                dcc.Dropdown(
                    options=[{"label": r, "value": r} for r in sorted(df['Responsável'].dropna().unique())],
                    id="filtro-responsavel", placeholder="Todos", multi=True, className="mb-3"
                ),
                html.Label("Status Entrega", className="fw-bold text-white mb-1"),
                dcc.Dropdown(
                    options=[{"label": e, "value": e} for e in sorted(df['Status'].dropna().unique())],
                    id="filtro-status", placeholder="Todos", multi=True
                )
            ], style={"backgroundColor": "#007B8A", "padding": "15px", "borderRadius": "10px"})
        ], width=2),

        dbc.Col([
            # Tabela principal
            dash_table.DataTable(
                id="tabela-processos",
                columns=[
                    {"name": "ID", "id": "ID"},
                    {"name": "Setores mapeados", "id": "Setores mapeados"},
                    {"name": "Qtd Atividades mapeadas por setor", "id": "Atividades mapeadas"},
                    {"name": "Instruções reestruturadas", "id": "Instruçoes reestruturadas"},
                    {"name": "Qtd entrevistados", "id": "Qtd colaboradores entrevistados"},
                    {"name": "Responsável", "id": "Responsável"},
                    {"name": "% Concluído", "id": "% Concluído", "type": "numeric", "format": {"specifier": ".0f"}},
                    {"name": "Status Entrega", "id": "Status"}
                ],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'backgroundColor': '#f9f9f9', 'color': 'black'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#ffffff', 'color': 'black'},
            ),

            html.Hr(),

            # Gráficos
            dbc.Row([
                dbc.Col(dcc.Graph(id="grafico-atividades"), width=6),
                dbc.Col(dcc.Graph(id="grafico-instrucoes"), width=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="grafico-entregas"), width=6),
                dbc.Col(dcc.Graph(id="grafico-status"), width=6),
            ])
        ], width=10)
    ])
], fluid=True)

@app.callback(
    Output("tabela-processos", "data"),
    Output("grafico-atividades", "figure"),
    Output("grafico-instrucoes", "figure"),
    Output("grafico-entregas", "figure"),
    Output("grafico-status", "figure"),
    Input("filtro-setor", "value"),
    Input("filtro-responsavel", "value"),
    Input("filtro-status", "value")
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

    # Gráfico atividades por setor
    fig_ativ = px.bar(dff, x='Setores mapeados', y='Atividades mapeadas', title="Atividades Mapeadas por Setor")

    # Gráfico instruções reestruturadas por Status Entrega
    fig_instr = px.bar(dff, x='Instruçoes reestruturadas', y='Status', orientation='h', title="Instr. Reestruturadas por Status")

    # Gráfico entregas concluídas por Etapa
    fig_entregas = px.bar(dff, x='Status', title="Entregas Concluídas")

    # Composição Status
    fig_status = px.pie(dff, names='Status', hole=0.4, title="Composição Status")

    for fig in [fig_ativ, fig_instr, fig_entregas, fig_status]:
        fig.update_layout(plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font_color="#000")

    return tabela, fig_ativ, fig_instr, fig_entregas, fig_status
