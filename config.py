"""
Configurações do projeto de análise de dados de mídias sociais
"""

# Configurações de data
DATA_CONFIG = {
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'timezone': 'America/Sao_Paulo'
}

# Configurações das plataformas
PLATFORMS = {
    'instagram': {
        'name': 'Instagram',
        'color': '#E4405F',
        'metrics': ['followers', 'impressions', 'reach', 'engagement', 'likes', 'comments', 'shares', 'saves']
    },
    'facebook': {
        'name': 'Facebook',
        'color': '#1877F2',
        'metrics': ['followers', 'impressions', 'reach', 'engagement', 'likes', 'comments', 'shares', 'clicks']
    }
}

# Configurações demográficas
DEMOGRAPHICS = {
    'age_groups': ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
    'genders': ['Masculino', 'Feminino', 'Outro'],
    'cities': [
        'São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília',
        'Fortaleza', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre',
        'Goiânia', 'Belém', 'Guarulhos', 'Campinas', 'São Luís'
    ],
    'interests': [
        'Tecnologia', 'Moda', 'Esportes', 'Culinária', 'Viagem',
        'Música', 'Arte', 'Fitness', 'Beleza', 'Negócios',
        'Educação', 'Entretenimento', 'Saúde', 'Automóveis', 'Casa e Decoração'
    ]
}

# Configurações de visualização
VISUALIZATION_CONFIG = {
    'figure_size': (12, 8),
    'dpi': 300,
    'style': 'seaborn-v0_8',
    'color_palette': 'Set2',
    'font_size': 12,
    'title_size': 16
}

# Configurações do dashboard
DASHBOARD_CONFIG = {
    'title': 'Dashboard de Marketing Digital - Mídias Sociais',
    'theme': 'BOOTSTRAP',
    'port': 8050,
    'debug': True
}

