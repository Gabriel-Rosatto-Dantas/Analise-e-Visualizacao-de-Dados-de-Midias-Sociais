"""
Analisador de KPIs para dados de mídias sociais
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import VISUALIZATION_CONFIG, PLATFORMS

# Configurar estilo das visualizações
plt.style.use(VISUALIZATION_CONFIG['style'])
sns.set_palette(VISUALIZATION_CONFIG['color_palette'])

class KPIAnalyzer:
    def __init__(self, platform_data, demographic_data, campaign_data):
        self.platform_data = platform_data
        self.demographic_data = demographic_data
        self.campaign_data = campaign_data
        
        # Converter coluna de data
        self.platform_data['date'] = pd.to_datetime(self.platform_data['date'])
        self.campaign_data['date'] = pd.to_datetime(self.campaign_data['date'])
    
    def calculate_growth_metrics(self):
        """Calcula métricas de crescimento para cada plataforma"""
        growth_metrics = {}
        
        for platform in self.platform_data['platform'].unique():
            platform_df = self.platform_data[self.platform_data['platform'] == platform].copy()
            platform_df = platform_df.sort_values('date')
            
            # Calcular crescimento mensal
            monthly_data = platform_df.groupby(platform_df['date'].dt.to_period('M')).agg({
                'followers': 'last',
                'impressions': 'sum',
                'reach': 'sum',
                'engagement': 'sum',
                'likes': 'sum',
                'comments': 'sum',
                'shares': 'sum'
            }).reset_index()
            
            # Calcular taxas de crescimento
            monthly_data['followers_growth'] = monthly_data['followers'].pct_change() * 100
            monthly_data['engagement_rate'] = (monthly_data['engagement'] / monthly_data['reach']) * 100
            monthly_data['impression_reach_ratio'] = monthly_data['impressions'] / monthly_data['reach']
            
            growth_metrics[platform] = monthly_data
        
        return growth_metrics
    
    def calculate_engagement_metrics(self):
        """Calcula métricas de engajamento"""
        engagement_metrics = {}
        
        for platform in self.platform_data['platform'].unique():
            platform_df = self.platform_data[self.platform_data['platform'] == platform]
            
            # Métricas de engajamento
            total_engagement = platform_df['engagement'].sum()
            total_reach = platform_df['reach'].sum()
            total_impressions = platform_df['impressions'].sum()
            
            avg_engagement_rate = (total_engagement / total_reach) * 100 if total_reach > 0 else 0
            avg_impression_rate = (total_reach / total_impressions) * 100 if total_impressions > 0 else 0
            
            # Engajamento por tipo de interação
            total_likes = platform_df['likes'].sum()
            total_comments = platform_df['comments'].sum()
            total_shares = platform_df['shares'].sum()
            
            engagement_metrics[platform] = {
                'total_engagement': total_engagement,
                'avg_engagement_rate': avg_engagement_rate,
                'avg_impression_rate': avg_impression_rate,
                'likes_percentage': (total_likes / total_engagement) * 100 if total_engagement > 0 else 0,
                'comments_percentage': (total_comments / total_engagement) * 100 if total_engagement > 0 else 0,
                'shares_percentage': (total_shares / total_engagement) * 100 if total_engagement > 0 else 0
            }
        
        return engagement_metrics
    
    def analyze_demographic_performance(self):
        """Analisa performance por segmentos demográficos"""
        demo_performance = {}
        
        for platform in self.demographic_data['platform'].unique():
            platform_demo = self.demographic_data[self.demographic_data['platform'] == platform]
            
            # Performance por faixa etária
            age_performance = platform_demo.groupby('age_group').agg({
                'engagement_rate': 'mean',
                'time_spent_minutes': 'mean'
            }).reset_index()
            
            # Performance por gênero
            gender_performance = platform_demo.groupby('gender').agg({
                'engagement_rate': 'mean',
                'time_spent_minutes': 'mean'
            }).reset_index()
            
            # Performance por cidade (top 10)
            city_performance = platform_demo.groupby('city').agg({
                'engagement_rate': 'mean',
                'time_spent_minutes': 'mean'
            }).reset_index().sort_values('engagement_rate', ascending=False).head(10)
            
            # Performance por interesse (top 10)
            interest_performance = platform_demo.groupby('interest').agg({
                'engagement_rate': 'mean',
                'time_spent_minutes': 'mean'
            }).reset_index().sort_values('engagement_rate', ascending=False).head(10)
            
            demo_performance[platform] = {
                'age_performance': age_performance,
                'gender_performance': gender_performance,
                'city_performance': city_performance,
                'interest_performance': interest_performance
            }
        
        return demo_performance
    
    def analyze_campaign_performance(self):
        """Analisa performance das campanhas"""
        campaign_performance = {}
        
        for platform in self.campaign_data['platform'].unique():
            platform_campaigns = self.campaign_data[self.campaign_data['platform'] == platform]
            
            # Performance por tipo de campanha
            campaign_type_performance = platform_campaigns.groupby('campaign_type').agg({
                'reach': 'mean',
                'engagement': 'mean',
                'cost': 'mean',
                'conversions': 'mean',
                'roi': 'mean'
            }).reset_index()
            
            # ROI por campanha
            campaign_roi = platform_campaigns.sort_values('roi', ascending=False)
            
            # Análise de custo-benefício
            platform_campaigns['cost_per_reach'] = platform_campaigns['cost'] / platform_campaigns['reach']
            platform_campaigns['cost_per_engagement'] = platform_campaigns['cost'] / platform_campaigns['engagement']
            
            campaign_performance[platform] = {
                'campaign_type_performance': campaign_type_performance,
                'top_campaigns_by_roi': campaign_roi.head(10),
                'cost_efficiency': platform_campaigns[['campaign_name', 'cost_per_reach', 'cost_per_engagement', 'roi']]
            }
        
        return campaign_performance
    
    def generate_kpi_summary(self):
        """Gera resumo dos KPIs principais"""
        growth_metrics = self.calculate_growth_metrics()
        engagement_metrics = self.calculate_engagement_metrics()
        
        summary = {}
        
        for platform in self.platform_data['platform'].unique():
            platform_data = self.platform_data[self.platform_data['platform'] == platform]
            
            # KPIs principais
            total_followers = platform_data['followers'].iloc[-1]  # Último valor
            avg_daily_impressions = platform_data['impressions'].mean()
            avg_daily_reach = platform_data['reach'].mean()
            avg_daily_engagement = platform_data['engagement'].mean()
            
            # Crescimento de seguidores
            followers_growth = growth_metrics[platform]['followers_growth'].iloc[-1] if len(growth_metrics[platform]) > 1 else 0
            
            summary[platform] = {
                'total_followers': total_followers,
                'followers_growth_rate': followers_growth,
                'avg_daily_impressions': avg_daily_impressions,
                'avg_daily_reach': avg_daily_reach,
                'avg_daily_engagement': avg_daily_engagement,
                'avg_engagement_rate': engagement_metrics[platform]['avg_engagement_rate'],
                'avg_impression_rate': engagement_metrics[platform]['avg_impression_rate']
            }
        
        return summary
    
    def identify_trends(self):
        """Identifica tendências nos dados"""
        trends = {}
        
        for platform in self.platform_data['platform'].unique():
            platform_data = self.platform_data[self.platform_data['platform'] == platform].copy()
            platform_data = platform_data.sort_values('date')
            
            # Tendência de seguidores (últimos 30 dias vs primeiros 30 dias)
            recent_followers = platform_data.tail(30)['followers'].mean()
            early_followers = platform_data.head(30)['followers'].mean()
            follower_trend = ((recent_followers - early_followers) / early_followers) * 100
            
            # Tendência de engajamento
            recent_engagement = platform_data.tail(30)['engagement'].mean()
            early_engagement = platform_data.head(30)['engagement'].mean()
            engagement_trend = ((recent_engagement - early_engagement) / early_engagement) * 100
            
            # Identificar dias de maior performance
            platform_data['engagement_rate'] = (platform_data['engagement'] / platform_data['reach']) * 100
            best_performance_days = platform_data.nlargest(5, 'engagement_rate')[['date', 'engagement_rate']]
            
            trends[platform] = {
                'follower_trend': follower_trend,
                'engagement_trend': engagement_trend,
                'best_performance_days': best_performance_days,
                'overall_trend': 'Crescimento' if follower_trend > 0 else 'Declínio'
            }
        
        return trends

if __name__ == "__main__":
    # Carregar dados
    platform_data = pd.read_csv('data/platform_metrics.csv')
    demographic_data = pd.read_csv('data/demographic_data.csv')
    campaign_data = pd.read_csv('data/campaign_data.csv')
    
    # Criar analisador
    analyzer = KPIAnalyzer(platform_data, demographic_data, campaign_data)
    
    # Gerar análises
    print("=== RESUMO DOS KPIs ===")
    kpi_summary = analyzer.generate_kpi_summary()
    for platform, metrics in kpi_summary.items():
        print(f"\n{platform}:")
        print(f"  Seguidores: {metrics['total_followers']:,}")
        print(f"  Taxa de Crescimento: {metrics['followers_growth_rate']:.2f}%")
        print(f"  Impressões Diárias: {metrics['avg_daily_impressions']:,.0f}")
        print(f"  Alcance Diário: {metrics['avg_daily_reach']:,.0f}")
        print(f"  Engajamento Diário: {metrics['avg_daily_engagement']:,.0f}")
        print(f"  Taxa de Engajamento: {metrics['avg_engagement_rate']:.2f}%")
    
    print("\n=== TENDÊNCIAS ===")
    trends = analyzer.identify_trends()
    for platform, trend_data in trends.items():
        print(f"\n{platform}:")
        print(f"  Tendência de Seguidores: {trend_data['follower_trend']:.2f}%")
        print(f"  Tendência de Engajamento: {trend_data['engagement_trend']:.2f}%")
        print(f"  Tendência Geral: {trend_data['overall_trend']}")
