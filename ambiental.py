import pandas as pd
import plotly.express as px
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# Carregar a planilha
df = pd.read_excel("Cronograma_Ambiental_MCM-STX.xlsx", sheet_name="Sheet1")

# Transformar para formato longo
df_long = pd.melt(
    df,
    id_vars=["Item", "Atividades"],
    var_name="Cidade",
    value_name="Prazo"
)

# Remover linhas com Prazo vazio
df_long = df_long.dropna(subset=["Prazo"])

# Função para definir Status baseado no Prazo
def definir_status(prazo):
    if isinstance(prazo, str):
        prazo_lower = prazo.lower()
        if "julho" in prazo_lower or "agosto" in prazo_lower:
            return "Em andamento"
        elif any(mes in prazo_lower for mes in ["setembro", "outubro", "novembro", "dezembro"]):
            return "Próximos passos"
    return None

df_long["Status"] = df_long["Prazo"].apply(definir_status)

# Filtrar somente linhas com Status definido para evitar valores None no gráfico
df_status = df_long.dropna(subset=["Status"])

# Agrupar por Cidade e Status, contando as atividades
df_status_count = df_status.groupby(["Cidade", "Status"]).size().reset_index(name="Quantidade")

# Gráfico de barras agrupadas
fig1 = px.bar(
    df_status_count,
    y="Cidade",        # cidades no eixo vertical
    x="Quantidade",    # quantidade no eixo horizontal
    color="Status",
    title="Quantidade de Atividades por Cidade e Status",
    barmode="group",
    text="Quantidade",
    color_discrete_map={
        "Em andamento": "#FFA726",
        "Próximos passos": "#29B6F6"
    },
    orientation='h'    # importante para o gráfico horizontal
)

# Estilo do gráfico
fig1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#C2E0E7",
    title_font_size=16,
    title_x=0.5,
    margin=dict(l=20, r=20, t=50, b=20),
    font=dict(size=12)
)

# Tabela com dados originais
tabela = dbc.Card(
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'backgroundColor': '#192A35',
            'color': '#C2E0E7',
            'whiteSpace': 'normal',
            'height': 'auto',
            'padding': '5px'
        },
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': '#263640',
            'color': '#C2E0E7'
        }
    ),
    style={
        "backgroundColor": "#192A35",
        "borderRadius": "15px",
        "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
        "padding": "10px",
        "marginBottom": "20px"
    }
)

# Layout da página Ambiental
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("B.I PPGC - AMBIENTAL", className="text-center fw-bold text-light mb-4"))
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(figure=fig1),
                style={
                    "backgroundColor": "#192A35",
                    "borderRadius": "15px",
                    "boxShadow": "0 0 10px rgba(0, 255, 255, 0.2)",
                    "padding": "10px",
                    "marginBottom": "20px"
                }
            ), width=12
        )
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("Tabela de Dados", className="text-light fw-bold mb-3"),
            tabela
        ])
    ])
], fluid=True, style={"backgroundColor": "#121E26", "minHeight": "100vh", "padding": "20px"})
