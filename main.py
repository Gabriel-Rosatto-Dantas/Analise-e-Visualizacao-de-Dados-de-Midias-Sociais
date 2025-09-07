"""
Sistema Principal de Análise e Visualização de Dados de Mídias Sociais
"""

import pandas as pd
import os
import sys
from datetime import datetime

# Adicionar src ao path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.generators.data_generator import SocialMediaDataGenerator
from src.analyzers.kpi_analyzer import KPIAnalyzer
from src.visualizers.visualizations import SocialMediaVisualizer
from src.analyzers.insights_generator import InsightsGenerator
from pipeline.report_generator import ReportGenerator
from src.dashboard.dashboard import SocialMediaDashboard

def main():
    """Função principal do sistema"""
    print("=" * 60)
    print("📊 SISTEMA DE ANÁLISE DE DADOS DE MÍDIAS SOCIAIS")
    print("=" * 60)
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Verificar se os dados já existem
    data_files = ['data/platform_metrics.csv', 'data/demographic_data.csv', 'data/campaign_data.csv']
    data_exists = all(os.path.exists(file) for file in data_files)
    
    if not data_exists:
        print("🔄 Gerando dados simulados...")
        generator = SocialMediaDataGenerator()
        platform_data, demographic_data, campaign_data = generator.generate_all_data()
    else:
        print("📁 Carregando dados existentes...")
        platform_data = pd.read_csv('data/platform_metrics.csv')
        demographic_data = pd.read_csv('data/demographic_data.csv')
        campaign_data = pd.read_csv('data/campaign_data.csv')
    
    print(f"✅ Dados carregados:")
    print(f"   - Métricas das plataformas: {len(platform_data)} registros")
    print(f"   - Dados demográficos: {len(demographic_data)} registros")
    print(f"   - Dados de campanhas: {len(campaign_data)} registros")
    print()
    
    # Menu principal
    while True:
        print("=" * 40)
        print("📋 MENU PRINCIPAL")
        print("=" * 40)
        print("1. 📈 Análise de KPIs")
        print("2. 📊 Gerar Visualizações")
        print("3. 💡 Gerar Insights Automáticos")
        print("4. 📄 Criar Relatório PDF")
        print("5. 🖥️  Abrir Dashboard Interativo")
        print("6. 🔄 Regenerar Dados")
        print("7. ❌ Sair")
        print("=" * 40)
        
        try:
            opcao = input("Escolha uma opção (1-7): ").strip()
            
            if opcao == '1':
                print("\n📈 Executando análise de KPIs...")
                analyzer = KPIAnalyzer(platform_data, demographic_data, campaign_data)
                
                # Executar análises
                kpi_summary = analyzer.generate_kpi_summary()
                trends = analyzer.identify_trends()
                
                print("\n=== RESUMO DOS KPIs ===")
                for platform, metrics in kpi_summary.items():
                    print(f"\n{platform}:")
                    print(f"  Seguidores: {metrics['total_followers']:,}")
                    print(f"  Taxa de Crescimento: {metrics['followers_growth_rate']:.2f}%")
                    print(f"  Impressões Diárias: {metrics['avg_daily_impressions']:,.0f}")
                    print(f"  Alcance Diário: {metrics['avg_daily_reach']:,.0f}")
                    print(f"  Engajamento Diário: {metrics['avg_daily_engagement']:,.0f}")
                    print(f"  Taxa de Engajamento: {metrics['avg_engagement_rate']:.2f}%")
                
                print("\n=== TENDÊNCIAS ===")
                for platform, trend_data in trends.items():
                    print(f"\n{platform}:")
                    print(f"  Tendência de Seguidores: {trend_data['follower_trend']:.2f}%")
                    print(f"  Tendência de Engajamento: {trend_data['engagement_trend']:.2f}%")
                    print(f"  Tendência Geral: {trend_data['overall_trend']}")
                
                input("\nPressione Enter para continuar...")
            
            elif opcao == '2':
                print("\n📊 Gerando visualizações...")
                visualizer = SocialMediaVisualizer(platform_data, demographic_data, campaign_data)
                visualizer.save_all_visualizations()
                print("✅ Visualizações salvas na pasta 'visualizations/'")
                input("\nPressione Enter para continuar...")
            
            elif opcao == '3':
                print("\n💡 Gerando insights automáticos...")
                insights_generator = InsightsGenerator(platform_data, demographic_data, campaign_data)
                insights = insights_generator.generate_all_insights()
                
                print("\n=== INSIGHTS AUTOMÁTICOS ===\n")
                for i, insight in enumerate(insights, 1):
                    print(f"{i}. [{insight['tipo']}] {insight['titulo']}")
                    print(f"   {insight['descricao']}")
                    print(f"   Recomendação: {insight['recomendacao']}")
                    print(f"   Prioridade: {insight['prioridade']}\n")
                
                # Mostrar recomendações estratégicas
                print("=== RECOMENDAÇÕES ESTRATÉGICAS ===\n")
                recommendations = insights_generator.generate_recommendations()
                
                for prazo, recs in recommendations.items():
                    print(f"{prazo.upper().replace('_', ' ')}:")
                    for rec in recs:
                        print(f"  • {rec['acao']}")
                        print(f"    Justificativa: {rec['justificativa']}")
                        print(f"    Impacto Esperado: {rec['impacto_esperado']}\n")
                
                input("\nPressione Enter para continuar...")
            
            elif opcao == '4':
                print("\n📄 Gerando relatório PDF...")
                insights_generator = InsightsGenerator(platform_data, demographic_data, campaign_data)
                report_generator = ReportGenerator(platform_data, demographic_data, campaign_data, insights_generator)
                
                filename = f"relatorio_marketing_digital_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                report_generator.generate_report(filename)
                print(f"✅ Relatório salvo como: {filename}")
                input("\nPressione Enter para continuar...")
            
            elif opcao == '5':
                print("\n🖥️  Iniciando dashboard interativo...")
                print("O dashboard será aberto no seu navegador.")
                print("Para parar o dashboard, pressione Ctrl+C no terminal.")
                print()
                
                dashboard = SocialMediaDashboard(platform_data, demographic_data, campaign_data)
                try:
                    dashboard.run()
                except KeyboardInterrupt:
                    print("\n✅ Dashboard encerrado.")
                    input("\nPressione Enter para continuar...")
            
            elif opcao == '6':
                print("\n🔄 Regenerando dados...")
                generator = SocialMediaDataGenerator()
                platform_data, demographic_data, campaign_data = generator.generate_all_data()
                print("✅ Dados regenerados com sucesso!")
                input("\nPressione Enter para continuar...")
            
            elif opcao == '7':
                print("\n👋 Obrigado por usar o Sistema de Análise de Dados de Mídias Sociais!")
                print("Desenvolvido para demonstrar análise e visualização de dados.")
                break
            
            else:
                print("\n❌ Opção inválida! Escolha um número de 1 a 7.")
                input("\nPressione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"\n❌ Erro: {str(e)}")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
