import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime
from dash.dependencies import Input, Output

# Carregar base
df = pd.read_excel("projeto.xlsx")
df['Início'] = pd.to_datetime(df['Início'])
df['Mês'] = df['Início'].dt.strftime('%b/%y')  # Ex: Jan/24
df['Dias desde início'] = (datetime.today() - df['Início']).dt.days

# Dash app com tema claro
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Dashboard de Projetos"

card_style = {"backgroundColor": "#191970", "border": "1px solid #dee2e6"}

# Layout com logo + filtros + gráficos
app.layout = dbc.Container([
    # Cabeçalho com logo MCM
    dbc.Row([
        dbc.Col(html.H2("📊 Visão Geral de Projetos", className="my-4 text-start"), width=9),
        dbc.Col(html.Img(src="assets/mcm_logo.webp", height="60px"),
                width=3, className="d-flex justify-content-end align-items-center")
    ], className="mb-4"),

    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por Status:"),
            dcc.Dropdown(
                options=[{"label": s, "value": s} for s in sorted(df['Status'].unique())],
                id="filtro-status", placeholder="Todos os Status", multi=True
            ),
        ], width=6),

        dbc.Col([
            html.Label("Filtrar por Projeto:"),
            dcc.Dropdown(
                options=[{"label": n, "value": n} for n in sorted(df['Nome do Projeto'].unique())],
                id="filtro-projeto", placeholder="Todos os Projetos", multi=True
            ),
        ], width=6),
    ], className="mb-4"),

    # KPIs dinâmicos
    dbc.Row(id="kpi-cards", className="mb-4"),

    # Gráficos dinâmicos
    dbc.Row([
        dbc.Col(dcc.Graph(id="grafico-linha"), width=6),
        dbc.Col(dcc.Graph(id="grafico-barra"), width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="grafico-pizza"), width=6),
        dbc.Col(dcc.Graph(id="grafico-gantt"), width=6),
    ])
], fluid=True)

# Callback para atualizar KPIs e gráficos
@app.callback(
    Output("kpi-cards", "children"),
    Output("grafico-linha", "figure"),
    Output("grafico-barra", "figure"),
    Output("grafico-pizza", "figure"),
    Output("grafico-gantt", "figure"),
    Input("filtro-status", "value"),
    Input("filtro-projeto", "value")
)
def atualizar_dashboard(status_selecionado, projeto_selecionado):
    dff = df.copy()
    if status_selecionado:
        dff = dff[dff["Status"].isin(status_selecionado)]
    if projeto_selecionado:
        dff = dff[dff["Nome do Projeto"].isin(projeto_selecionado)]

    # Recalcular KPIs
    total = dff.shape[0]
    media_concluido = dff['% Concluído'].mean() if total > 0 else 0
    media_dias = dff['Dias desde início'].mean() if total > 0 else 0

    kpis = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Total de Projetos", className="text-muted"),
            html.H3(f"{total}", className="text-primary")
        ]), style=card_style), width=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("% Médio Concluído", className="text-muted"),
            html.H3(f"{media_concluido:.1f}%", className="text-success")
        ]), style=card_style), width=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Tempo médio desde início", className="text-muted"),
            html.H3(f"{media_dias:.0f} dias", className="text-info")
        ]), style=card_style), width=4),
    ])

    # Gráfico de linha (Projetos por Mês)
    linha_df = dff.groupby('Mês').size().reset_index(name='Projetos')
    fig_linha = px.line(linha_df, x='Mês', y='Projetos', markers=True,
                        title="Projetos Iniciados por Mês")

    # Gráfico de barra (% Concluído por Projeto)
    fig_barra = px.bar(
        dff.sort_values(by='% Concluído', ascending=False),
        x='% Concluído', y='Nome do Projeto',
        orientation='h', title="Conclusão por Projeto",
        color='% Concluído', color_continuous_scale='Teal'
    )

    # Gráfico de pizza (Status)
    fig_pizza = px.pie(dff, names='Status', title="Distribuição por Status")

    # Gráfico Gantt simplificado (dias desde início)
    fig_gantt = px.bar(
        dff, x='Dias desde início', y='Nome do Projeto',
        orientation='h', title="Dias desde Início por Projeto",
        color='Dias desde início', color_continuous_scale='Blues',
        hover_data=['Início', '% Concluído', 'Status']
    )

    return kpis, fig_linha, fig_barra, fig_pizza, fig_gantt

if __name__ == '__main__':
    app.run(debug=True)
