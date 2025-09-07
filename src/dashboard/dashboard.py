"""
Dashboard interativo para análise de dados de mídias sociais usando Dash
"""

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import DASHBOARD_CONFIG, PLATFORMS

class SocialMediaDashboard:
    def __init__(self, platform_data, demographic_data, campaign_data):
        self.platform_data = platform_data
        self.demographic_data = demographic_data
        self.campaign_data = campaign_data
        
        # Converter colunas de data
        self.platform_data['date'] = pd.to_datetime(self.platform_data['date'])
        self.campaign_data['date'] = pd.to_datetime(self.campaign_data['date'])
        
        # Criar app Dash
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Configura o layout do dashboard"""
        self.app.layout = dbc.Container([
            # Cabeçalho
            dbc.Row([
                dbc.Col([
                    html.H1("📊 Dashboard de Marketing Digital", 
                           className="text-center text-primary mb-4"),
                    html.P("Análise e Visualização de Dados de Mídias Sociais", 
                          className="text-center text-muted mb-4")
                ])
            ]),
            
            # Filtros
            dbc.Row([
                dbc.Col([
                    html.Label("Selecionar Plataforma:"),
                    dcc.Dropdown(
                        id='platform-dropdown',
                        options=[
                            {'label': 'Todas as Plataformas', 'value': 'all'},
                            {'label': 'Instagram', 'value': 'Instagram'},
                            {'label': 'Facebook', 'value': 'Facebook'}
                        ],
                        value='all',
                        clearable=False
                    )
                ], width=4),
                dbc.Col([
                    html.Label("Período:"),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date=self.platform_data['date'].min(),
                        end_date=self.platform_data['date'].max(),
                        display_format='DD/MM/YYYY'
                    )
                ], width=4),
                dbc.Col([
                    html.Label("Métrica Principal:"),
                    dcc.Dropdown(
                        id='metric-dropdown',
                        options=[
                            {'label': 'Seguidores', 'value': 'followers'},
                            {'label': 'Impressões', 'value': 'impressions'},
                            {'label': 'Alcance', 'value': 'reach'},
                            {'label': 'Engajamento', 'value': 'engagement'}
                        ],
                        value='followers',
                        clearable=False
                    )
                ], width=4)
            ], className="mb-4"),
            
            # Cards de KPIs
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id="total-followers", className="card-title"),
                            html.P("Total de Seguidores", className="card-text")
                        ])
                    ], color="primary", outline=True)
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id="total-engagement", className="card-title"),
                            html.P("Engajamento Total", className="card-text")
                        ])
                    ], color="success", outline=True)
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id="avg-engagement-rate", className="card-title"),
                            html.P("Taxa de Engajamento", className="card-text")
                        ])
                    ], color="info", outline=True)
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id="total-reach", className="card-title"),
                            html.P("Alcance Total", className="card-text")
                        ])
                    ], color="warning", outline=True)
                ], width=3)
            ], className="mb-4"),
            
            # Gráficos principais
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='main-metric-chart')
                ], width=8),
                dbc.Col([
                    dcc.Graph(id='engagement-breakdown')
                ], width=4)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='demographic-chart')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='campaign-performance')
                ], width=6)
            ], className="mb-4"),
            
            # Tabela de dados
            dbc.Row([
                dbc.Col([
                    html.H4("Dados Detalhados"),
                    dash_table.DataTable(
                        id='data-table',
                        columns=[
                            {"name": "Data", "id": "date"},
                            {"name": "Plataforma", "id": "platform"},
                            {"name": "Seguidores", "id": "followers"},
                            {"name": "Impressões", "id": "impressions"},
                            {"name": "Alcance", "id": "reach"},
                            {"name": "Engajamento", "id": "engagement"}
                        ],
                        page_size=10,
                        style_cell={'textAlign': 'left'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                ])
            ])
            
        ], fluid=True)
    
    def setup_callbacks(self):
        """Configura os callbacks do dashboard"""
        
        @self.app.callback(
            [Output('total-followers', 'children'),
             Output('total-engagement', 'children'),
             Output('avg-engagement-rate', 'children'),
             Output('total-reach', 'children')],
            [Input('platform-dropdown', 'value'),
             Input('date-range', 'start_date'),
             Input('date-range', 'end_date')]
        )
        def update_kpi_cards(platform, start_date, end_date):
            # Filtrar dados
            filtered_data = self.filter_data(platform, start_date, end_date)
            
            # Calcular KPIs
            total_followers = filtered_data.groupby('platform')['followers'].last().sum()
            total_engagement = filtered_data['engagement'].sum()
            total_reach = filtered_data['reach'].sum()
            avg_engagement_rate = (total_engagement / total_reach * 100) if total_reach > 0 else 0
            
            return (
                f"{total_followers:,.0f}",
                f"{total_engagement:,.0f}",
                f"{avg_engagement_rate:.2f}%",
                f"{total_reach:,.0f}"
            )
        
        @self.app.callback(
            Output('main-metric-chart', 'figure'),
            [Input('platform-dropdown', 'value'),
             Input('date-range', 'start_date'),
             Input('date-range', 'end_date'),
             Input('metric-dropdown', 'value')]
        )
        def update_main_chart(platform, start_date, end_date, metric):
            filtered_data = self.filter_data(platform, start_date, end_date)
            
            fig = go.Figure()
            
            for platform_name in filtered_data['platform'].unique():
                platform_data = filtered_data[filtered_data['platform'] == platform_name]
                platform_data = platform_data.sort_values('date')
                
                color = PLATFORMS[platform_name.lower()]['color']
                
                fig.add_trace(go.Scatter(
                    x=platform_data['date'],
                    y=platform_data[metric],
                    mode='lines+markers',
                    name=platform_name,
                    line=dict(color=color, width=3),
                    marker=dict(size=6)
                ))
            
            fig.update_layout(
                title=f'Evolução de {metric.title()} por Plataforma',
                xaxis_title='Data',
                yaxis_title=metric.title(),
                hovermode='x unified',
                height=400
            )
            
            return fig
        
        @self.app.callback(
            Output('engagement-breakdown', 'figure'),
            [Input('platform-dropdown', 'value'),
             Input('date-range', 'start_date'),
             Input('date-range', 'end_date')]
        )
        def update_engagement_breakdown(platform, start_date, end_date):
            filtered_data = self.filter_data(platform, start_date, end_date)
            
            # Calcular breakdown de engajamento
            engagement_breakdown = filtered_data.groupby('platform').agg({
                'likes': 'sum',
                'comments': 'sum',
                'shares': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            engagement_types = ['likes', 'comments', 'shares']
            
            for i, engagement_type in enumerate(engagement_types):
                fig.add_trace(go.Bar(
                    x=engagement_breakdown['platform'],
                    y=engagement_breakdown[engagement_type],
                    name=engagement_type.title(),
                    marker_color=colors[i]
                ))
            
            fig.update_layout(
                title='Breakdown de Engajamento',
                barmode='stack',
                height=400
            )
            
            return fig
        
        @self.app.callback(
            Output('demographic-chart', 'figure'),
            [Input('platform-dropdown', 'value')]
        )
        def update_demographic_chart(platform):
            if platform == 'all':
                demo_data = self.demographic_data
            else:
                demo_data = self.demographic_data[self.demographic_data['platform'] == platform]
            
            # Distribuição por faixa etária
            age_dist = demo_data.groupby('age_group').size().reset_index(name='count')
            
            fig = px.pie(age_dist, values='count', names='age_group', 
                        title='Distribuição por Faixa Etária')
            
            return fig
        
        @self.app.callback(
            Output('campaign-performance', 'figure'),
            [Input('platform-dropdown', 'value')]
        )
        def update_campaign_chart(platform):
            if platform == 'all':
                campaign_data = self.campaign_data
            else:
                campaign_data = self.campaign_data[self.campaign_data['platform'] == platform]
            
            # ROI por tipo de campanha
            roi_data = campaign_data.groupby('campaign_type')['roi'].mean().reset_index()
            
            fig = px.bar(roi_data, x='campaign_type', y='roi',
                        title='ROI Médio por Tipo de Campanha',
                        color='roi', color_continuous_scale='Viridis')
            
            return fig
        
        @self.app.callback(
            Output('data-table', 'data'),
            [Input('platform-dropdown', 'value'),
             Input('date-range', 'start_date'),
             Input('date-range', 'end_date')]
        )
        def update_data_table(platform, start_date, end_date):
            filtered_data = self.filter_data(platform, start_date, end_date)
            
            # Formatar dados para a tabela
            table_data = filtered_data[['date', 'platform', 'followers', 'impressions', 'reach', 'engagement']].copy()
            table_data['date'] = table_data['date'].dt.strftime('%d/%m/%Y')
            
            return table_data.to_dict('records')
    
    def filter_data(self, platform, start_date, end_date):
        """Filtra dados baseado nos parâmetros selecionados"""
        filtered_data = self.platform_data.copy()
        
        # Filtrar por plataforma
        if platform != 'all':
            filtered_data = filtered_data[filtered_data['platform'] == platform]
        
        # Filtrar por data
        if start_date:
            filtered_data = filtered_data[filtered_data['date'] >= start_date]
        if end_date:
            filtered_data = filtered_data[filtered_data['date'] <= end_date]
        
        return filtered_data
    
    def run(self):
        """Executa o dashboard"""
        print(f"Iniciando dashboard em http://localhost:{DASHBOARD_CONFIG['port']}")
        self.app.run(
            debug=DASHBOARD_CONFIG['debug'],
            port=DASHBOARD_CONFIG['port']
        )

if __name__ == "__main__":
    # Carregar dados
    platform_data = pd.read_csv('data/platform_metrics.csv')
    demographic_data = pd.read_csv('data/demographic_data.csv')
    campaign_data = pd.read_csv('data/campaign_data.csv')
    
    # Criar e executar dashboard
    dashboard = SocialMediaDashboard(platform_data, demographic_data, campaign_data)
    dashboard.run()
