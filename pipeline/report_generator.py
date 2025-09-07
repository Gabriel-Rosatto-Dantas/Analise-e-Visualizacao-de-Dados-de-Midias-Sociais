"""
Gerador de relatório em PDF para análise de dados de mídias sociais
"""

import pandas as pd
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import os
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import VISUALIZATION_CONFIG

class ReportGenerator:
    def __init__(self, platform_data, demographic_data, campaign_data, insights_generator):
        self.platform_data = platform_data
        self.demographic_data = demographic_data
        self.campaign_data = campaign_data
        self.insights_generator = insights_generator
        
        # Configurar matplotlib para português
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['figure.figsize'] = (10, 6)
        
        # Criar pasta para imagens temporárias
        self.temp_dir = 'temp_images'
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def create_summary_chart(self):
        """Cria gráfico de resumo para o relatório"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Crescimento de seguidores
        for platform in self.platform_data['platform'].unique():
            platform_data = self.platform_data[self.platform_data['platform'] == platform]
            platform_data = platform_data.sort_values('date')
            ax1.plot(platform_data['date'], platform_data['followers'], 
                    label=platform, linewidth=2, marker='o', markersize=4)
        
        ax1.set_title('Crescimento de Seguidores', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Data')
        ax1.set_ylabel('Seguidores')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Taxa de engajamento
        platform_engagement = self.platform_data.groupby('platform').agg({
            'engagement': 'sum',
            'reach': 'sum'
        })
        platform_engagement['engagement_rate'] = (platform_engagement['engagement'] / platform_engagement['reach']) * 100
        
        colors = ['#FF6B6B', '#4ECDC4']
        bars = ax2.bar(platform_engagement.index, platform_engagement['engagement_rate'], color=colors)
        ax2.set_title('Taxa de Engajamento por Plataforma', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Taxa de Engajamento (%)')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%', ha='center', va='bottom')
        
        # 3. Distribuição demográfica
        age_dist = self.demographic_data.groupby('age_group').size()
        ax3.pie(age_dist.values, labels=age_dist.index, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Distribuição por Faixa Etária', fontsize=14, fontweight='bold')
        
        # 4. ROI das campanhas
        campaign_roi = self.campaign_data.groupby('campaign_type')['roi'].mean().sort_values(ascending=True)
        ax4.barh(campaign_roi.index, campaign_roi.values, color='#96CEB4')
        ax4.set_title('ROI Médio por Tipo de Campanha', fontsize=14, fontweight='bold')
        ax4.set_xlabel('ROI')
        
        plt.tight_layout()
        
        # Salvar gráfico
        chart_path = os.path.join(self.temp_dir, 'summary_chart.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def create_kpi_table(self):
        """Cria tabela de KPIs principais"""
        kpi_summary = self.insights_generator.generate_kpi_summary()
        
        data = [['Plataforma', 'Seguidores', 'Taxa de Crescimento', 'Engajamento Total', 'Taxa de Engajamento']]
        
        for platform, metrics in kpi_summary.items():
            data.append([
                platform,
                f"{metrics['total_followers']:,.0f}",
                f"{metrics['followers_growth_rate']:.2f}%",
                f"{metrics['avg_daily_engagement']:,.0f}",
                f"{metrics['avg_engagement_rate']:.2f}%"
            ])
        
        return data
    
    def create_insights_table(self):
        """Cria tabela de insights"""
        insights = self.insights_generator.generate_all_insights()
        
        data = [['Tipo', 'Título', 'Prioridade', 'Recomendação']]
        
        for insight in insights[:10]:  # Top 10 insights
            data.append([
                insight['tipo'],
                insight['titulo'],
                insight['prioridade'],
                insight['recomendacao'][:100] + '...' if len(insight['recomendacao']) > 100 else insight['recomendacao']
            ])
        
        return data
    
    def generate_report(self, filename='relatorio_marketing_digital.pdf'):
        """Gera o relatório completo em PDF"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Criar estilos customizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.darkgreen
        )
        
        # Conteúdo do relatório
        story = []
        
        # Título
        story.append(Paragraph("Relatório de Marketing Digital", title_style))
        story.append(Paragraph("Análise e Visualização de Dados de Mídias Sociais", 
                              styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Data de geração
        story.append(Paragraph(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                              styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Resumo Executivo
        story.append(Paragraph("Resumo Executivo", heading_style))
        story.append(Paragraph(
            "Este relatório apresenta uma análise abrangente dos dados de mídias sociais, "
            "incluindo métricas de performance, análise demográfica do público e insights "
            "estratégicos para otimização de campanhas de marketing digital.",
            styles['Normal']
        ))
        story.append(Spacer(1, 20))
        
        # Gráfico de Resumo
        story.append(Paragraph("Visão Geral das Métricas", heading_style))
        chart_path = self.create_summary_chart()
        story.append(Image(chart_path, width=7*inch, height=5.8*inch))
        story.append(Spacer(1, 20))
        
        # KPIs Principais
        story.append(Paragraph("KPIs Principais", heading_style))
        kpi_data = self.create_kpi_table()
        kpi_table = Table(kpi_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 20))
        
        # Análise Demográfica
        story.append(Paragraph("Análise Demográfica", heading_style))
        
        # Estatísticas demográficas
        total_users = len(self.demographic_data)
        avg_engagement = self.demographic_data['engagement_rate'].mean()
        avg_time_spent = self.demographic_data['time_spent_minutes'].mean()
        
        story.append(Paragraph("Principais Estatísticas:", subheading_style))
        story.append(Paragraph(f"• Total de usuários analisados: {total_users:,}", styles['Normal']))
        story.append(Paragraph(f"• Taxa de engajamento média: {avg_engagement:.2f}%", styles['Normal']))
        story.append(Paragraph(f"• Tempo médio de permanência: {avg_time_spent:.1f} minutos", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Top cidades e interesses
        top_cities = self.demographic_data.groupby('city')['engagement_rate'].mean().sort_values(ascending=False).head(5)
        top_interests = self.demographic_data.groupby('interest')['engagement_rate'].mean().sort_values(ascending=False).head(5)
        
        story.append(Paragraph("Top 5 Cidades por Engajamento:", subheading_style))
        for city, rate in top_cities.items():
            story.append(Paragraph(f"• {city}: {rate:.2f}%", styles['Normal']))
        
        story.append(Spacer(1, 12))
        story.append(Paragraph("Top 5 Interesses por Engajamento:", subheading_style))
        for interest, rate in top_interests.items():
            story.append(Paragraph(f"• {interest}: {rate:.2f}%", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Análise de Campanhas
        story.append(Paragraph("Análise de Campanhas", heading_style))
        
        total_campaigns = len(self.campaign_data)
        avg_roi = self.campaign_data['roi'].mean()
        total_cost = self.campaign_data['cost'].sum()
        total_conversions = self.campaign_data['conversions'].sum()
        
        story.append(Paragraph("Métricas de Campanhas:", subheading_style))
        story.append(Paragraph(f"• Total de campanhas analisadas: {total_campaigns}", styles['Normal']))
        story.append(Paragraph(f"• ROI médio: {avg_roi:.2f}", styles['Normal']))
        story.append(Paragraph(f"• Investimento total: R$ {total_cost:,.2f}", styles['Normal']))
        story.append(Paragraph(f"• Total de conversões: {total_conversions:,}", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Insights e Recomendações
        story.append(Paragraph("Insights e Recomendações", heading_style))
        
        insights_table_data = self.create_insights_table()
        insights_table = Table(insights_table_data, colWidths=[1*inch, 2*inch, 0.8*inch, 2.2*inch])
        insights_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(insights_table)
        story.append(Spacer(1, 20))
        
        # Recomendações Estratégicas
        story.append(Paragraph("Recomendações Estratégicas", heading_style))
        
        recommendations = self.insights_generator.generate_recommendations()
        
        for prazo, recs in recommendations.items():
            prazo_title = prazo.replace('_', ' ').title()
            story.append(Paragraph(f"{prazo_title}:", subheading_style))
            
            for rec in recs:
                story.append(Paragraph(f"• {rec['acao']}", styles['Normal']))
                story.append(Paragraph(f"  Justificativa: {rec['justificativa']}", 
                                      styles['Normal']))
                story.append(Paragraph(f"  Impacto Esperado: {rec['impacto_esperado']}", 
                                      styles['Normal']))
                story.append(Spacer(1, 8))
        
        # Conclusão
        story.append(Paragraph("Conclusão", heading_style))
        story.append(Paragraph(
            "A análise dos dados de mídias sociais revela oportunidades significativas "
            "para otimização da estratégia de marketing digital. As recomendações apresentadas "
            "devem ser implementadas de forma gradual, com monitoramento contínuo dos resultados "
            "para ajustes futuros.",
            styles['Normal']
        ))
        
        story.append(Spacer(1, 20))
        story.append(Paragraph(
            "Este relatório foi gerado automaticamente pelo sistema de análise de dados de mídias sociais. "
            "Para mais informações ou análises específicas, entre em contato com a equipe de marketing digital.",
            styles['Normal']
        ))
        
        # Construir PDF
        doc.build(story)
        
        # Limpar arquivos temporários
        if os.path.exists(chart_path):
            os.remove(chart_path)
        
        print(f"Relatório gerado com sucesso: {filename}")

if __name__ == "__main__":
    # Carregar dados
    platform_data = pd.read_csv('data/platform_metrics.csv')
    demographic_data = pd.read_csv('data/demographic_data.csv')
    campaign_data = pd.read_csv('data/campaign_data.csv')
    
    # Criar gerador de insights
    from insights_generator import InsightsGenerator
    insights_generator = InsightsGenerator(platform_data, demographic_data, campaign_data)
    
    # Criar e gerar relatório
    report_generator = ReportGenerator(platform_data, demographic_data, campaign_data, insights_generator)
    report_generator.generate_report()
