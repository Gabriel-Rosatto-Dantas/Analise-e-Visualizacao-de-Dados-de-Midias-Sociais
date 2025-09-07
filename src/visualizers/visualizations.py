"""
Módulo de visualizações para dados de mídias sociais
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import VISUALIZATION_CONFIG, PLATFORMS

# Configurar matplotlib para português
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = VISUALIZATION_CONFIG['figure_size']
plt.rcParams['figure.dpi'] = VISUALIZATION_CONFIG['dpi']

class SocialMediaVisualizer:
    def __init__(self, platform_data, demographic_data, campaign_data):
        self.platform_data = platform_data
        self.demographic_data = demographic_data
        self.campaign_data = campaign_data
        
        # Converter colunas de data
        self.platform_data['date'] = pd.to_datetime(self.platform_data['date'])
        self.campaign_data['date'] = pd.to_datetime(self.campaign_data['date'])
    
    def create_followers_growth_chart(self):
        """Cria gráfico de crescimento de seguidores"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for platform in self.platform_data['platform'].unique():
            platform_data = self.platform_data[self.platform_data['platform'] == platform]
            platform_data = platform_data.sort_values('date')
            
            color = PLATFORMS[platform.lower()]['color']
            ax.plot(platform_data['date'], platform_data['followers'], 
                   label=platform, color=color, linewidth=2, marker='o', markersize=4)
        
        ax.set_title('Crescimento de Seguidores por Plataforma', fontsize=16, fontweight='bold')
        ax.set_xlabel('Data', fontsize=12)
        ax.set_ylabel('Número de Seguidores', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Formatar eixo Y com separadores de milhares
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
        
        plt.tight_layout()
        return fig
    
    def create_engagement_comparison(self):
        """Cria gráfico de comparação de engajamento"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico 1: Engajamento total por plataforma
        engagement_by_platform = self.platform_data.groupby('platform')['engagement'].sum()
        colors = [PLATFORMS[platform.lower()]['color'] for platform in engagement_by_platform.index]
        
        bars1 = ax1.bar(engagement_by_platform.index, engagement_by_platform.values, color=colors)
        ax1.set_title('Engajamento Total por Plataforma', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Engajamento Total')
        
        # Adicionar valores nas barras
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:,.0f}', ha='center', va='bottom')
        
        # Gráfico 2: Taxa de engajamento média
        platform_data_grouped = self.platform_data.groupby('platform').agg({
            'engagement': 'sum',
            'reach': 'sum'
        })
        platform_data_grouped['engagement_rate'] = (platform_data_grouped['engagement'] / platform_data_grouped['reach']) * 100
        
        bars2 = ax2.bar(platform_data_grouped.index, platform_data_grouped['engagement_rate'], color=colors)
        ax2.set_title('Taxa de Engajamento Média por Plataforma', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Taxa de Engajamento (%)')
        
        # Adicionar valores nas barras
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    def create_demographic_analysis(self):
        """Cria análise demográfica do público"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Distribuição por faixa etária
        age_dist = self.demographic_data.groupby(['platform', 'age_group']).size().unstack(fill_value=0)
        age_dist.plot(kind='bar', ax=ax1, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
        ax1.set_title('Distribuição do Público por Faixa Etária', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Plataforma')
        ax1.set_ylabel('Número de Usuários')
        ax1.legend(title='Faixa Etária', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Distribuição por gênero
        gender_dist = self.demographic_data.groupby(['platform', 'gender']).size().unstack(fill_value=0)
        gender_dist.plot(kind='bar', ax=ax2, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        ax2.set_title('Distribuição do Público por Gênero', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Plataforma')
        ax2.set_ylabel('Número de Usuários')
        ax2.legend(title='Gênero')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Top 10 cidades com maior engajamento
        city_engagement = self.demographic_data.groupby('city')['engagement_rate'].mean().sort_values(ascending=True).tail(10)
        city_engagement.plot(kind='barh', ax=ax3, color='#96CEB4')
        ax3.set_title('Top 10 Cidades por Taxa de Engajamento', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Taxa de Engajamento (%)')
        
        # 4. Top 10 interesses com maior engajamento
        interest_engagement = self.demographic_data.groupby('interest')['engagement_rate'].mean().sort_values(ascending=True).tail(10)
        interest_engagement.plot(kind='barh', ax=ax4, color='#FFEAA7')
        ax4.set_title('Top 10 Interesses por Taxa de Engajamento', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Taxa de Engajamento (%)')
        
        plt.tight_layout()
        return fig
    
    def create_campaign_performance_chart(self):
        """Cria gráfico de performance das campanhas"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico 1: ROI por tipo de campanha
        campaign_roi = self.campaign_data.groupby(['platform', 'campaign_type'])['roi'].mean().unstack(fill_value=0)
        campaign_roi.plot(kind='bar', ax=ax1, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        ax1.set_title('ROI Médio por Tipo de Campanha', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Plataforma')
        ax1.set_ylabel('ROI')
        ax1.legend(title='Tipo de Campanha', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico 2: Custo vs Conversões
        for platform in self.campaign_data['platform'].unique():
            platform_campaigns = self.campaign_data[self.campaign_data['platform'] == platform]
            color = PLATFORMS[platform.lower()]['color']
            ax2.scatter(platform_campaigns['cost'], platform_campaigns['conversions'], 
                       label=platform, color=color, alpha=0.7, s=100)
        
        ax2.set_title('Custo vs Conversões por Plataforma', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Custo da Campanha (R$)')
        ax2.set_ylabel('Número de Conversões')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_interactive_dashboard(self):
        """Cria dashboard interativo com Plotly"""
        # Criar subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Crescimento de Seguidores', 'Taxa de Engajamento',
                           'Distribuição por Idade', 'Performance de Campanhas',
                           'Top Cidades', 'ROI por Tipo de Campanha'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Crescimento de seguidores
        for platform in self.platform_data['platform'].unique():
            platform_data = self.platform_data[self.platform_data['platform'] == platform]
            platform_data = platform_data.sort_values('date')
            color = PLATFORMS[platform.lower()]['color']
            
            fig.add_trace(
                go.Scatter(x=platform_data['date'], y=platform_data['followers'],
                          mode='lines+markers', name=platform, line=dict(color=color)),
                row=1, col=1
            )
        
        # 2. Taxa de engajamento
        platform_engagement = self.platform_data.groupby('platform').agg({
            'engagement': 'sum',
            'reach': 'sum'
        })
        platform_engagement['engagement_rate'] = (platform_engagement['engagement'] / platform_engagement['reach']) * 100
        
        colors = [PLATFORMS[platform.lower()]['color'] for platform in platform_engagement.index]
        fig.add_trace(
            go.Bar(x=platform_engagement.index, y=platform_engagement['engagement_rate'],
                  name='Taxa de Engajamento', marker_color=colors),
            row=1, col=2
        )
        
        # 3. Distribuição por idade
        age_dist = self.demographic_data.groupby(['platform', 'age_group']).size().unstack(fill_value=0)
        for age_group in age_dist.columns:
            fig.add_trace(
                go.Bar(x=age_dist.index, y=age_dist[age_group], name=age_group),
                row=2, col=1
            )
        
        # 4. Performance de campanhas (Custo vs Conversões)
        for platform in self.campaign_data['platform'].unique():
            platform_campaigns = self.campaign_data[self.campaign_data['platform'] == platform]
            color = PLATFORMS[platform.lower()]['color']
            
            fig.add_trace(
                go.Scatter(x=platform_campaigns['cost'], y=platform_campaigns['conversions'],
                          mode='markers', name=f'{platform} Campanhas', 
                          marker=dict(color=color, size=10)),
                row=2, col=2
            )
        
        # 5. Top cidades
        city_engagement = self.demographic_data.groupby('city')['engagement_rate'].mean().sort_values(ascending=True).tail(10)
        fig.add_trace(
            go.Bar(y=city_engagement.index, x=city_engagement.values, orientation='h',
                  name='Top Cidades', marker_color='#96CEB4'),
            row=3, col=1
        )
        
        # 6. ROI por tipo de campanha
        campaign_roi = self.campaign_data.groupby('campaign_type')['roi'].mean().sort_values(ascending=True)
        fig.add_trace(
            go.Bar(y=campaign_roi.index, x=campaign_roi.values, orientation='h',
                  name='ROI por Tipo', marker_color='#FFEAA7'),
            row=3, col=2
        )
        
        # Atualizar layout
        fig.update_layout(
            title_text="Dashboard de Marketing Digital - Mídias Sociais",
            title_x=0.5,
            height=1200,
            showlegend=True
        )
        
        return fig
    
    def create_heatmap_correlation(self):
        """Cria mapa de calor de correlação entre métricas"""
        # Selecionar apenas colunas numéricas
        numeric_columns = ['followers', 'impressions', 'reach', 'engagement', 'likes', 'comments', 'shares']
        
        # Calcular correlação por plataforma
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        for i, platform in enumerate(self.platform_data['platform'].unique()):
            platform_data = self.platform_data[self.platform_data['platform'] == platform]
            correlation_matrix = platform_data[numeric_columns].corr()
            
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, ax=axes[i], cbar_kws={'shrink': 0.8})
            axes[i].set_title(f'Correlação de Métricas - {platform}', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def save_all_visualizations(self, output_dir='visualizations'):
        """Salva todas as visualizações em arquivos"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Criar e salvar visualizações estáticas
        charts = {
            'crescimento_seguidores': self.create_followers_growth_chart(),
            'comparacao_engajamento': self.create_engagement_comparison(),
            'analise_demografica': self.create_demographic_analysis(),
            'performance_campanhas': self.create_campaign_performance_chart(),
            'correlacao_metricas': self.create_heatmap_correlation()
        }
        
        for name, fig in charts.items():
            fig.savefig(f'{output_dir}/{name}.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
        
        # Salvar dashboard interativo
        interactive_dashboard = self.create_interactive_dashboard()
        interactive_dashboard.write_html(f'{output_dir}/dashboard_interativo.html')
        
        print(f"Visualizações salvas na pasta '{output_dir}/'")

if __name__ == "__main__":
    # Carregar dados
    platform_data = pd.read_csv('data/platform_metrics.csv')
    demographic_data = pd.read_csv('data/demographic_data.csv')
    campaign_data = pd.read_csv('data/campaign_data.csv')
    
    # Criar visualizador
    visualizer = SocialMediaVisualizer(platform_data, demographic_data, campaign_data)
    
    # Salvar todas as visualizações
    visualizer.save_all_visualizations()
    
    print("Visualizações criadas com sucesso!")
