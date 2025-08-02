import pandas as pd 
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import datetime

from app_instance import app  # CERTO (importa o app sem ciclo)

# Carrega dados
df = pd.read_excel("projeto.xlsx")
df['Início'] = pd.to_datetime(df['Início'])
df['Dias desde início'] = (datetime.today() - df['Início']).dt.days
df['Atualizado em'] = datetime.today().strftime('%d/%m/%y')

# Cores por status
cores_status = {
    "Em Andamento": "#E48817",
    "Concluído": "#71A54A",
    "Atrasado": "#CE053C",
    "Não iniciado": "#D6A78D"
}
ordem_status = ["Em Andamento", "Concluído", "Atrasado", "Não iniciado"]

def hex_to_rgba(hex_color, opacity):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {opacity})'

# Layout exportado para uso no app.py
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("📊 Visão Geral de Projetos", style={"color": "orange", "font-family":"system-ui"}),
            html.Span(f"Dados atualizados em {df['Atualizado em'].iloc[0]}", style={"color": "orange"})
        ], width=9),
        dbc.Col(html.Img(src="assets/mcm_logo.webp", height="50px"),
                width=3, className="d-flex justify-content-end align-items-center")
    ], className="my-3"),

    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por Status:", className="text-light"),
            dcc.Dropdown(
                options=[{"label": s, "value": s} for s in sorted(df['Status'].unique())],
                id="filtro-status", placeholder="Todos os Status", multi=True
            ),
        ], width=6),
        dbc.Col([
            html.Label("Filtrar por Projeto:", className="text-light"),
            dcc.Dropdown(
                options=[{"label": n, "value": n} for n in sorted(df['Nome do Projeto'].unique())],
                id="filtro-projeto", placeholder="Todos os Projetos", multi=True
            ),
        ], width=6),
    ], className="mb-4"),

    dbc.Row(id="kpis", className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="grafico-barra"), width=6),
        dbc.Col(dcc.Graph(id="grafico-rosca"), width=6),
    ], className="mb-4"),

    dash_table.DataTable(
        id="tabela-projetos",
        columns=[{"name": col, "id": col} for col in ['ID','Nome do Projeto','Início','Status', '% Concluído']],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'backgroundColor': '#00183F', 'color': 'white'},
        style_header={'fontWeight': 'bold', 'backgroundColor': '#00183F', 'color': 'white'},
    ),
    html.Div(id="total-projetos", className="text-end mt-2 fw-bold text-light")
], fluid=True, style={"backgroundColor": "#00183F", "minHeight": "100vh", "padding": "20px"})

# Callback que será registrado no app principal
@app.callback(
    Output("grafico-barra", "figure"),
    Output("grafico-rosca", "figure"),
    Output("kpis", "children"),
    Output("tabela-projetos", "data"),
    Output("total-projetos", "children"),
    Input("filtro-status", "value"),
    Input("filtro-projeto", "value"),
    Input("grafico-barra", "clickData"),
    Input("grafico-rosca", "clickData")
)
def atualizar_tudo(f_status, f_projeto, click_barra, click_rosca):
    dff = df.copy()
    if f_status:
        dff = dff[dff['Status'].isin(f_status)]
    if f_projeto:
        dff = dff[dff['Nome do Projeto'].isin(f_projeto)]

    dff['% Concluído'] = dff['% Concluído'].astype(str).str.replace('%', '').str.strip()
    dff['% Concluído'] = pd.to_numeric(dff['% Concluído'], errors='coerce')

    contagem = dff['Status'].value_counts().reindex(ordem_status).fillna(0).astype(int).reset_index()
    contagem.columns = ['Status', 'Contagem']

    status_clicado = None
    if click_barra and 'points' in click_barra:
        status_clicado = click_barra['points'][0]['y']
    elif click_rosca and 'points' in click_rosca:
        status_clicado = click_rosca['points'][0]['label']

    cores_barras = []
    cores_rosca = {}
    for status in contagem['Status']:
        cor_base = cores_status.get(status, "#1f77b4")
        if status == status_clicado:
            cores_barras.append(cor_base)
            cores_rosca[status] = cor_base
        else:
            cor_opaca = hex_to_rgba(cor_base, 0.7)
            cores_barras.append(cor_opaca)
            cores_rosca[status] = cor_opaca

    fig_barra = go.Figure()
    fig_barra.add_trace(go.Bar(
        x=contagem['Contagem'],
        y=contagem['Status'],
        orientation='h',
        text=contagem['Contagem'],
        textposition='auto',
        marker_color=cores_barras
    ))
    fig_barra.update_layout(
        title="Contagem de ID por Status",
        plot_bgcolor="#00183F",
        paper_bgcolor="#00183F",
        font_color="#ffffff",
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False
    )

    fig_rosca = px.pie(contagem, names='Status', values='Contagem',
                       hole=0.5, title="Contagem de ID por Status",
                       color='Status', color_discrete_map=cores_rosca)
    fig_rosca.update_traces(textinfo='percent+value')
    fig_rosca.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#00183F",
        font_color="#ffffff",
        legend_title_text="Status"
    )

    total = dff.shape[0]
    media_concluido = dff['% Concluído'].mean() if total > 0 else 0
    media_dias = dff['Dias desde início'].mean() if total > 0 else 0

    kpis = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Total de Projetos", className="text-muted"),
            html.H3(f"{total}", className="text-primary")
        ])), width=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("% Projetos Concluído", className="text-muted"),
            html.H3(f"{media_concluido:.1f}%", className="text-success")
        ])), width=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Tempo médio desde início", className="text-muted"),
            html.H3(f"{media_dias:.0f} dias", className="text-info")
        ])), width=4),
    ])

    tabela = dff[['ID', 'Nome do Projeto', 'Início', 'Status', '% Concluído']].to_dict('records')
    for linha in tabela:
        if isinstance(linha['Início'], pd.Timestamp):
            linha['Início'] = linha['Início'].strftime('%d/%m/%y')
        else:
            linha['Início'] = str(linha['Início'])

    total_texto = f"Total: {total}"

    return fig_barra, fig_rosca, kpis, tabela, total_texto
