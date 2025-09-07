"""
Exemplo de uso do Sistema de Análise de Dados de Mídias Sociais
"""

import pandas as pd
import sys
import os

# Adicionar src ao path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.generators.data_generator import SocialMediaDataGenerator
from src.analyzers.kpi_analyzer import KPIAnalyzer
from src.visualizers.visualizations import SocialMediaVisualizer
from src.analyzers.insights_generator import InsightsGenerator
from pipeline.report_generator import ReportGenerator

def exemplo_completo():
    """Exemplo completo de uso do sistema"""
    print("🚀 EXEMPLO DE USO DO SISTEMA DE ANÁLISE DE DADOS DE MÍDIAS SOCIAIS")
    print("=" * 70)
    
    # 1. Gerar dados simulados
    print("\n1️⃣ Gerando dados simulados...")
    generator = SocialMediaDataGenerator()
    platform_data, demographic_data, campaign_data = generator.generate_all_data()
    
    print(f"✅ Dados gerados:")
    print(f"   - Métricas das plataformas: {len(platform_data)} registros")
    print(f"   - Dados demográficos: {len(demographic_data)} registros")
    print(f"   - Dados de campanhas: {len(campaign_data)} registros")
    
    # 2. Análise de KPIs
    print("\n2️⃣ Executando análise de KPIs...")
    analyzer = KPIAnalyzer(platform_data, demographic_data, campaign_data)
    kpi_summary = analyzer.generate_kpi_summary()
    trends = analyzer.identify_trends()
    
    print("\n📊 RESUMO DOS KPIs:")
    for platform, metrics in kpi_summary.items():
        print(f"\n{platform}:")
        print(f"  Seguidores: {metrics['total_followers']:,}")
        print(f"  Taxa de Crescimento: {metrics['followers_growth_rate']:.2f}%")
        print(f"  Taxa de Engajamento: {metrics['avg_engagement_rate']:.2f}%")
    
    # 3. Gerar visualizações
    print("\n3️⃣ Criando visualizações...")
    visualizer = SocialMediaVisualizer(platform_data, demographic_data, campaign_data)
    visualizer.save_all_visualizations()
    print("✅ Visualizações salvas na pasta 'visualizations/'")
    
    # 4. Gerar insights automáticos
    print("\n4️⃣ Gerando insights automáticos...")
    insights_generator = InsightsGenerator(platform_data, demographic_data, campaign_data)
    insights = insights_generator.generate_all_insights()
    
    print(f"\n💡 INSIGHTS GERADOS ({len(insights)} insights):")
    for i, insight in enumerate(insights[:5], 1):  # Mostrar apenas os 5 primeiros
        print(f"\n{i}. [{insight['tipo']}] {insight['titulo']}")
        print(f"   {insight['descricao']}")
        print(f"   Recomendação: {insight['recomendacao']}")
        print(f"   Prioridade: {insight['prioridade']}")
    
    # 5. Gerar relatório PDF
    print("\n5️⃣ Gerando relatório PDF...")
    report_generator = ReportGenerator(platform_data, demographic_data, campaign_data, insights_generator)
    filename = "exemplo_relatorio_marketing.pdf"
    report_generator.generate_report(filename)
    print(f"✅ Relatório salvo como: {filename}")
    
    # 6. Resumo final
    print("\n🎯 RESUMO DO EXEMPLO:")
    print("✅ Dados simulados gerados")
    print("✅ Análise de KPIs executada")
    print("✅ Visualizações criadas")
    print("✅ Insights automáticos gerados")
    print("✅ Relatório PDF criado")
    
    print("\n📁 ARQUIVOS GERADOS:")
    print("   - data/platform_metrics.csv")
    print("   - data/demographic_data.csv")
    print("   - data/campaign_data.csv")
    print("   - visualizations/ (pasta com gráficos)")
    print(f"   - {filename}")
    
    print("\n🚀 Para usar o dashboard interativo, execute:")
    print("   python dashboard.py")
    
    print("\n📖 Para mais informações, consulte o README.md")

def exemplo_analise_rapida():
    """Exemplo de análise rápida"""
    print("\n⚡ EXEMPLO DE ANÁLISE RÁPIDA")
    print("=" * 40)
    
    # Carregar dados existentes
    platform_data = pd.read_csv('data/platform_metrics.csv')
    demographic_data = pd.read_csv('data/demographic_data.csv')
    campaign_data = pd.read_csv('data/campaign_data.csv')
    
    # Análise rápida de engajamento
    print("\n📈 Análise de Engajamento por Plataforma:")
    engagement_by_platform = platform_data.groupby('platform').agg({
        'engagement': 'sum',
        'reach': 'sum',
        'followers': 'last'
    })
    
    engagement_by_platform['engagement_rate'] = (engagement_by_platform['engagement'] / engagement_by_platform['reach']) * 100
    
    for platform, data in engagement_by_platform.iterrows():
        print(f"\n{platform}:")
        print(f"  Seguidores: {data['followers']:,}")
        print(f"  Engajamento Total: {data['engagement']:,}")
        print(f"  Taxa de Engajamento: {data['engagement_rate']:.2f}%")
    
    # Top interesses
    print("\n🎯 Top 5 Interesses por Engajamento:")
    top_interests = demographic_data.groupby('interest')['engagement_rate'].mean().sort_values(ascending=False).head(5)
    for interest, rate in top_interests.items():
        print(f"  • {interest}: {rate:.2f}%")
    
    # ROI das campanhas
    print("\n💰 ROI Médio por Tipo de Campanha:")
    roi_by_type = campaign_data.groupby('campaign_type')['roi'].mean().sort_values(ascending=False)
    for campaign_type, roi in roi_by_type.items():
        print(f"  • {campaign_type}: {roi:.2f}")

if __name__ == "__main__":
    # Executar exemplo completo
    exemplo_completo()
    
    # Executar análise rápida
    exemplo_analise_rapida()
    
    print("\n🎉 Exemplo concluído com sucesso!")
    print("Para executar o sistema completo, use: python main.py")
