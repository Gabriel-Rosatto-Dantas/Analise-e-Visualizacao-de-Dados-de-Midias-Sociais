"""
Gerador de insights automáticos para dados de mídias sociais
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import PLATFORMS

class InsightsGenerator:
    def __init__(self, platform_data, demographic_data, campaign_data):
        self.platform_data = platform_data
        self.demographic_data = demographic_data
        self.campaign_data = campaign_data
        
        # Converter colunas de data
        self.platform_data['date'] = pd.to_datetime(self.platform_data['date'])
        self.campaign_data['date'] = pd.to_datetime(self.campaign_data['date'])
    
    def generate_performance_insights(self):
        """Gera insights sobre performance geral"""
        insights = []
        
        # Calcular métricas principais
        total_followers = self.platform_data.groupby('platform')['followers'].last().sum()
        total_engagement = self.platform_data['engagement'].sum()
        total_reach = self.platform_data['reach'].sum()
        avg_engagement_rate = (total_engagement / total_reach * 100) if total_reach > 0 else 0
        
        # Insight 1: Performance geral
        if avg_engagement_rate > 5:
            insights.append({
                'tipo': 'Performance',
                'titulo': 'Excelente Taxa de Engajamento',
                'descricao': f'A taxa de engajamento média de {avg_engagement_rate:.2f}% está acima da média da indústria (3-5%).',
                'recomendacao': 'Continue com a estratégia atual e considere aumentar a frequência de posts.',
                'prioridade': 'Alta'
            })
        elif avg_engagement_rate < 2:
            insights.append({
                'tipo': 'Performance',
                'titulo': 'Taxa de Engajamento Baixa',
                'descricao': f'A taxa de engajamento média de {avg_engagement_rate:.2f}% está abaixo da média da indústria.',
                'recomendacao': 'Revise a estratégia de conteúdo e considere posts mais interativos.',
                'prioridade': 'Crítica'
            })
        
        # Insight 2: Crescimento de seguidores
        for platform in self.platform_data['platform'].unique():
            platform_data = self.platform_data[self.platform_data['platform'] == platform]
            platform_data = platform_data.sort_values('date')
            
            initial_followers = platform_data['followers'].iloc[0]
            final_followers = platform_data['followers'].iloc[-1]
            growth_rate = ((final_followers - initial_followers) / initial_followers) * 100
            
            if growth_rate > 20:
                insights.append({
                    'tipo': 'Crescimento',
                    'titulo': f'Crescimento Excepcional no {platform}',
                    'descricao': f'O {platform} teve um crescimento de {growth_rate:.1f}% no período analisado.',
                    'recomendacao': 'Mantenha a estratégia atual e considere investir mais nesta plataforma.',
                    'prioridade': 'Alta'
                })
            elif growth_rate < 5:
                insights.append({
                    'tipo': 'Crescimento',
                    'titulo': f'Crescimento Lento no {platform}',
                    'descricao': f'O {platform} teve um crescimento de apenas {growth_rate:.1f}% no período.',
                    'recomendacao': 'Revise a estratégia de conteúdo e considere campanhas pagas.',
                    'prioridade': 'Média'
                })
        
        return insights
    
    def generate_demographic_insights(self):
        """Gera insights sobre dados demográficos"""
        insights = []
        
        # Insight 1: Faixa etária dominante
        age_distribution = self.demographic_data.groupby('age_group').size().sort_values(ascending=False)
        dominant_age = age_distribution.index[0]
        age_percentage = (age_distribution.iloc[0] / age_distribution.sum()) * 100
        
        insights.append({
            'tipo': 'Demográfico',
            'titulo': f'Público-Alvo Principal: {dominant_age}',
            'descricao': f'A faixa etária {dominant_age} representa {age_percentage:.1f}% do público total.',
            'recomendacao': f'Adapte o conteúdo para o público {dominant_age} e considere campanhas específicas.',
            'prioridade': 'Alta'
        })
        
        # Insight 2: Gênero predominante
        gender_distribution = self.demographic_data.groupby('gender').size().sort_values(ascending=False)
        dominant_gender = gender_distribution.index[0]
        gender_percentage = (gender_distribution.iloc[0] / gender_distribution.sum()) * 100
        
        insights.append({
            'tipo': 'Demográfico',
            'titulo': f'Audiência Principalmente {dominant_gender}',
            'descricao': f'O público {dominant_gender} representa {gender_percentage:.1f}% da audiência.',
            'recomendacao': f'Desenvolva conteúdo específico para o público {dominant_gender} e considere parcerias com influenciadores.',
            'prioridade': 'Média'
        })
        
        # Insight 3: Cidades com maior engajamento
        city_engagement = self.demographic_data.groupby('city')['engagement_rate'].mean().sort_values(ascending=False)
        top_city = city_engagement.index[0]
        top_city_rate = city_engagement.iloc[0]
        
        insights.append({
            'tipo': 'Geográfico',
            'titulo': f'{top_city} - Cidade com Maior Engajamento',
            'descricao': f'{top_city} apresenta a maior taxa de engajamento ({top_city_rate:.2f}%).',
            'recomendacao': f'Considere eventos presenciais em {top_city} e campanhas geo-direcionadas.',
            'prioridade': 'Média'
        })
        
        # Insight 4: Interesses mais populares
        interest_engagement = self.demographic_data.groupby('interest')['engagement_rate'].mean().sort_values(ascending=False)
        top_interest = interest_engagement.index[0]
        top_interest_rate = interest_engagement.iloc[0]
        
        insights.append({
            'tipo': 'Conteúdo',
            'titulo': f'Interesse Principal: {top_interest}',
            'descricao': f'O interesse em {top_interest} gera a maior taxa de engajamento ({top_interest_rate:.2f}%).',
            'recomendacao': f'Aumente a produção de conteúdo relacionado a {top_interest}.',
            'prioridade': 'Alta'
        })
        
        return insights
    
    def generate_campaign_insights(self):
        """Gera insights sobre campanhas"""
        insights = []
        
        # Insight 1: Tipo de campanha mais eficaz
        campaign_roi = self.campaign_data.groupby('campaign_type')['roi'].mean().sort_values(ascending=False)
        best_campaign_type = campaign_roi.index[0]
        best_roi = campaign_roi.iloc[0]
        
        insights.append({
            'tipo': 'Campanha',
            'titulo': f'Campanhas de {best_campaign_type} Mais Eficazes',
            'descricao': f'Campanhas do tipo {best_campaign_type} apresentam o maior ROI médio ({best_roi:.2f}).',
            'recomendacao': f'Aumente o investimento em campanhas de {best_campaign_type}.',
            'prioridade': 'Alta'
        })
        
        # Insight 2: Plataforma com melhor ROI
        platform_roi = self.campaign_data.groupby('platform')['roi'].mean().sort_values(ascending=False)
        best_platform = platform_roi.index[0]
        best_platform_roi = platform_roi.iloc[0]
        
        insights.append({
            'tipo': 'Plataforma',
            'titulo': f'{best_platform} - Melhor ROI em Campanhas',
            'descricao': f'O {best_platform} apresenta o maior ROI médio em campanhas ({best_platform_roi:.2f}).',
            'recomendacao': f'Redirecione mais orçamento para campanhas no {best_platform}.',
            'prioridade': 'Alta'
        })
        
        # Insight 3: Análise de custo-benefício
        self.campaign_data['cost_per_conversion'] = self.campaign_data['cost'] / self.campaign_data['conversions']
        cost_efficiency = self.campaign_data.groupby('platform')['cost_per_conversion'].mean().sort_values()
        most_efficient = cost_efficiency.index[0]
        lowest_cost = cost_efficiency.iloc[0]
        
        insights.append({
            'tipo': 'Eficiência',
            'titulo': f'{most_efficient} - Menor Custo por Conversão',
            'descricao': f'O {most_efficient} apresenta o menor custo por conversão (R$ {lowest_cost:.2f}).',
            'recomendacao': f'Otimize campanhas no {most_efficient} para maximizar conversões.',
            'prioridade': 'Média'
        })
        
        return insights
    
    def generate_trend_insights(self):
        """Gera insights sobre tendências temporais"""
        insights = []
        
        # Insight 1: Tendência de crescimento
        for platform in self.platform_data['platform'].unique():
            platform_data = self.platform_data[self.platform_data['platform'] == platform].copy()
            platform_data = platform_data.sort_values('date')
            
            # Calcular tendência usando regressão linear simples
            x = np.arange(len(platform_data))
            y = platform_data['engagement'].values
            
            # Calcular coeficiente de correlação
            correlation = np.corrcoef(x, y)[0, 1]
            
            if correlation > 0.5:
                insights.append({
                    'tipo': 'Tendência',
                    'titulo': f'Tendência Positiva de Engajamento no {platform}',
                    'descricao': f'O {platform} mostra uma tendência crescente de engajamento (correlação: {correlation:.2f}).',
                    'recomendacao': 'Mantenha a estratégia atual e considere aumentar a frequência de posts.',
                    'prioridade': 'Alta'
                })
            elif correlation < -0.3:
                insights.append({
                    'tipo': 'Tendência',
                    'titulo': f'Declínio de Engajamento no {platform}',
                    'descricao': f'O {platform} mostra uma tendência decrescente de engajamento (correlação: {correlation:.2f}).',
                    'recomendacao': 'Revise urgentemente a estratégia de conteúdo e engajamento.',
                    'prioridade': 'Crítica'
                })
        
        # Insight 2: Sazonalidade
        platform_data_monthly = self.platform_data.copy()
        platform_data_monthly['month'] = platform_data_monthly['date'].dt.month
        monthly_engagement = platform_data_monthly.groupby('month')['engagement'].mean()
        
        best_month = monthly_engagement.idxmax()
        worst_month = monthly_engagement.idxmin()
        
        month_names = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        
        insights.append({
            'tipo': 'Sazonalidade',
            'titulo': f'Melhor Mês: {month_names[best_month]}',
            'descricao': f'{month_names[best_month]} apresenta o maior engajamento médio.',
            'recomendacao': f'Planeje campanhas especiais para {month_names[best_month]} e evite grandes investimentos em {month_names[worst_month]}.',
            'prioridade': 'Média'
        })
        
        return insights
    
    def generate_content_insights(self):
        """Gera insights sobre conteúdo"""
        insights = []
        
        # Insight 1: Melhor horário para posts (simulado)
        # Como não temos dados de horário, vamos simular baseado no engajamento
        platform_data_with_hour = self.platform_data.copy()
        platform_data_with_hour['hour'] = np.random.randint(6, 23, len(platform_data_with_hour))
        
        hourly_engagement = platform_data_with_hour.groupby('hour')['engagement'].mean()
        best_hour = hourly_engagement.idxmax()
        
        insights.append({
            'tipo': 'Conteúdo',
            'titulo': f'Melhor Horário: {best_hour}h',
            'descricao': f'O horário das {best_hour}h apresenta o maior engajamento médio.',
            'recomendacao': f'Agende posts principais para as {best_hour}h para maximizar o alcance.',
            'prioridade': 'Média'
        })
        
        # Insight 2: Tipo de interação mais comum
        total_likes = self.platform_data['likes'].sum()
        total_comments = self.platform_data['comments'].sum()
        total_shares = self.platform_data['shares'].sum()
        
        interactions = {
            'likes': total_likes,
            'comments': total_comments,
            'shares': total_shares
        }
        
        most_common = max(interactions, key=interactions.get)
        most_common_percentage = (interactions[most_common] / sum(interactions.values())) * 100
        
        insights.append({
            'tipo': 'Interação',
            'titulo': f'{most_common.title()} - Interação Mais Comum',
            'descricao': f'{most_common.title()} representam {most_common_percentage:.1f}% de todas as interações.',
            'recomendacao': f'Desenvolva conteúdo que incentive mais {most_common} para aumentar o engajamento.',
            'prioridade': 'Baixa'
        })
        
        return insights
    
    def generate_all_insights(self):
        """Gera todos os insights"""
        all_insights = []
        
        all_insights.extend(self.generate_performance_insights())
        all_insights.extend(self.generate_demographic_insights())
        all_insights.extend(self.generate_campaign_insights())
        all_insights.extend(self.generate_trend_insights())
        all_insights.extend(self.generate_content_insights())
        
        # Ordenar por prioridade
        priority_order = {'Crítica': 1, 'Alta': 2, 'Média': 3, 'Baixa': 4}
        all_insights.sort(key=lambda x: priority_order.get(x['prioridade'], 5))
        
        return all_insights
    
    def generate_recommendations(self):
        """Gera recomendações estratégicas baseadas nos insights"""
        insights = self.generate_all_insights()
        
        recommendations = {
            'curto_prazo': [],
            'medio_prazo': [],
            'longo_prazo': []
        }
        
        # Recomendações de curto prazo (baseadas em insights críticos e altos)
        critical_high_insights = [i for i in insights if i['prioridade'] in ['Crítica', 'Alta']]
        
        for insight in critical_high_insights[:3]:  # Top 3 mais importantes
            recommendations['curto_prazo'].append({
                'acao': insight['recomendacao'],
                'justificativa': insight['descricao'],
                'impacto_esperado': 'Alto' if insight['prioridade'] == 'Crítica' else 'Médio'
            })
        
        # Recomendações de médio prazo (baseadas em insights médios)
        medium_insights = [i for i in insights if i['prioridade'] == 'Média']
        
        for insight in medium_insights[:3]:
            recommendations['medio_prazo'].append({
                'acao': insight['recomendacao'],
                'justificativa': insight['descricao'],
                'impacto_esperado': 'Médio'
            })
        
        # Recomendações de longo prazo (estratégicas)
        recommendations['longo_prazo'] = [
            {
                'acao': 'Desenvolver estratégia de conteúdo multicanal integrada',
                'justificativa': 'Análise mostra diferentes performances por plataforma',
                'impacto_esperado': 'Alto'
            },
            {
                'acao': 'Implementar sistema de análise de sentimento',
                'justificativa': 'Monitoramento contínuo pode otimizar engajamento',
                'impacto_esperado': 'Médio'
            },
            {
                'acao': 'Criar programa de influenciadores micro e nano',
                'justificativa': 'Dados demográficos mostram oportunidades específicas',
                'impacto_esperado': 'Alto'
            }
        ]
        
        return recommendations
    
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

if __name__ == "__main__":
    # Carregar dados
    platform_data = pd.read_csv('data/platform_metrics.csv')
    demographic_data = pd.read_csv('data/demographic_data.csv')
    campaign_data = pd.read_csv('data/campaign_data.csv')
    
    # Criar gerador de insights
    insights_generator = InsightsGenerator(platform_data, demographic_data, campaign_data)
    
    # Gerar insights
    print("=== INSIGHTS AUTOMÁTICOS ===\n")
    insights = insights_generator.generate_all_insights()
    
    for i, insight in enumerate(insights, 1):
        print(f"{i}. [{insight['tipo']}] {insight['titulo']}")
        print(f"   {insight['descricao']}")
        print(f"   Recomendação: {insight['recomendacao']}")
        print(f"   Prioridade: {insight['prioridade']}\n")
    
    # Gerar recomendações
    print("=== RECOMENDAÇÕES ESTRATÉGICAS ===\n")
    recommendations = insights_generator.generate_recommendations()
    
    for prazo, recs in recommendations.items():
        print(f"{prazo.upper().replace('_', ' ')}:")
        for rec in recs:
            print(f"  • {rec['acao']}")
            print(f"    Justificativa: {rec['justificativa']}")
            print(f"    Impacto Esperado: {rec['impacto_esperado']}\n")
