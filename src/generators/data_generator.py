"""
Gerador de dados simulados para análise de mídias sociais
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import DATA_CONFIG, PLATFORMS, DEMOGRAPHICS

class SocialMediaDataGenerator:
    def __init__(self):
        self.start_date = datetime.strptime(DATA_CONFIG['start_date'], '%Y-%m-%d')
        self.end_date = datetime.strptime(DATA_CONFIG['end_date'], '%Y-%m-%d')
        
    def generate_date_range(self):
        """Gera range de datas para o período especificado"""
        dates = []
        current_date = self.start_date
        while current_date <= self.end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)
        return dates
    
    def generate_platform_data(self, platform_name, dates):
        """Gera dados para uma plataforma específica"""
        platform_config = PLATFORMS[platform_name]
        data = []
        
        # Valores base para cada métrica (simulando crescimento orgânico)
        base_values = {
            'followers': random.randint(10000, 50000),
            'impressions': random.randint(50000, 200000),
            'reach': random.randint(30000, 150000),
            'engagement': random.randint(5000, 25000),
            'likes': random.randint(2000, 15000),
            'comments': random.randint(100, 1000),
            'shares': random.randint(50, 500),
            'saves': random.randint(100, 800) if platform_name == 'instagram' else 0,
            'clicks': random.randint(200, 2000) if platform_name == 'facebook' else 0
        }
        
        for date in dates:
            # Simular crescimento e variação sazonal
            days_passed = (date - self.start_date).days
            growth_factor = 1 + (days_passed * 0.001)  # Crescimento de 0.1% por dia
            
            # Variação sazonal (maior engajamento em fins de semana)
            weekend_factor = 1.2 if date.weekday() >= 5 else 1.0
            
            # Variação aleatória
            random_factor = random.uniform(0.8, 1.2)
            
            row = {
                'date': date,
                'platform': platform_config['name'],
                'followers': int(base_values['followers'] * growth_factor * random_factor),
                'impressions': int(base_values['impressions'] * growth_factor * weekend_factor * random_factor),
                'reach': int(base_values['reach'] * growth_factor * weekend_factor * random_factor),
                'engagement': int(base_values['engagement'] * growth_factor * weekend_factor * random_factor),
                'likes': int(base_values['likes'] * growth_factor * weekend_factor * random_factor),
                'comments': int(base_values['comments'] * growth_factor * weekend_factor * random_factor),
                'shares': int(base_values['shares'] * growth_factor * weekend_factor * random_factor)
            }
            
            # Adicionar métricas específicas da plataforma
            if platform_name == 'instagram':
                row['saves'] = int(base_values['saves'] * growth_factor * weekend_factor * random_factor)
            elif platform_name == 'facebook':
                row['clicks'] = int(base_values['clicks'] * growth_factor * weekend_factor * random_factor)
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def generate_demographic_data(self, platform_name, sample_size=1000):
        """Gera dados demográficos do público"""
        platform_config = PLATFORMS[platform_name]
        data = []
        
        for _ in range(sample_size):
            row = {
                'platform': platform_config['name'],
                'age_group': random.choice(DEMOGRAPHICS['age_groups']),
                'gender': random.choice(DEMOGRAPHICS['genders']),
                'city': random.choice(DEMOGRAPHICS['cities']),
                'interest': random.choice(DEMOGRAPHICS['interests']),
                'engagement_rate': random.uniform(0.02, 0.08),  # 2% a 8%
                'time_spent_minutes': random.randint(5, 60)
            }
            data.append(row)
        
        return pd.DataFrame(data)
    
    def generate_campaign_data(self, platform_name, dates):
        """Gera dados de campanhas específicas"""
        platform_config = PLATFORMS[platform_name]
        data = []
        
        # Simular algumas campanhas ao longo do período
        campaign_dates = random.sample(dates, min(20, len(dates)))
        
        for date in campaign_dates:
            campaign_types = ['Promoção', 'Lançamento', 'Educativo', 'Entretenimento', 'Sazonal']
            campaign_type = random.choice(campaign_types)
            
            # Métricas específicas de campanha
            base_reach = random.randint(10000, 50000)
            base_engagement = random.randint(1000, 8000)
            
            campaign_names = [
                "Promoção - Black Friday", "Lançamento - Novo Produto", "Educativo - Tutorial",
                "Entretenimento - Desafio Viral", "Sazonal - Natal", "Promoção - Dia das Mães",
                "Lançamento - Campanha Verão", "Educativo - Dicas de Saúde", "Entretenimento - Memes",
                "Sazonal - Páscoa", "Promoção - Cyber Monday", "Lançamento - App Mobile"
            ]
            
            row = {
                'date': date,
                'platform': platform_config['name'],
                'campaign_type': campaign_type,
                'campaign_name': random.choice(campaign_names),
                'reach': base_reach,
                'engagement': base_engagement,
                'cost': random.randint(500, 5000),
                'conversions': random.randint(50, 500),
                'roi': random.uniform(1.5, 4.0)
            }
            data.append(row)
        
        return pd.DataFrame(data)
    
    def generate_all_data(self):
        """Gera todos os dados necessários para o projeto"""
        print("Gerando dados de mídias sociais...")
        
        dates = self.generate_date_range()
        
        # Dados principais das plataformas
        instagram_data = self.generate_platform_data('instagram', dates)
        facebook_data = self.generate_platform_data('facebook', dates)
        
        # Combinar dados das plataformas
        platform_data = pd.concat([instagram_data, facebook_data], ignore_index=True)
        
        # Dados demográficos
        instagram_demo = self.generate_demographic_data('instagram')
        facebook_demo = self.generate_demographic_data('facebook')
        demographic_data = pd.concat([instagram_demo, facebook_demo], ignore_index=True)
        
        # Dados de campanhas
        instagram_campaigns = self.generate_campaign_data('instagram', dates)
        facebook_campaigns = self.generate_campaign_data('facebook', dates)
        campaign_data = pd.concat([instagram_campaigns, facebook_campaigns], ignore_index=True)
        
        print(f"Dados gerados com sucesso!")
        print(f"- Dados das plataformas: {len(platform_data)} registros")
        print(f"- Dados demográficos: {len(demographic_data)} registros")
        print(f"- Dados de campanhas: {len(campaign_data)} registros")
        
        return platform_data, demographic_data, campaign_data

if __name__ == "__main__":
    generator = SocialMediaDataGenerator()
    platform_data, demographic_data, campaign_data = generator.generate_all_data()
    
    # Salvar dados em arquivos CSV
    platform_data.to_csv('data/platform_metrics.csv', index=False)
    demographic_data.to_csv('data/demographic_data.csv', index=False)
    campaign_data.to_csv('data/campaign_data.csv', index=False)
    
    print("\nDados salvos em arquivos CSV na pasta 'data/'")
