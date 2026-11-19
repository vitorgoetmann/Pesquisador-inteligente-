#!/usr/bin/env python
"""Script para criar dados de exemplo (seed) para demonstração"""
import os
import sys
import django

# Adicionar o diretório pai ao path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pesquisador_project.settings')
django.setup()

from pesquisador_app.models import SearchQuery, Article, Summary

def create_seed_data():
    # Criar SearchQuery de exemplo
    query = SearchQuery.objects.create(termo="energia solar")
    print(f"✓ Query criada: #{query.id} - {query.termo}")
    
    # Dados de exemplo de artigos
    articles_data = [
        {
            "url": "https://www.portalsolar.com.br/energia-solar",
            "title": "Energia Solar: O que é, como funciona e suas vantagens",
            "content": """A energia solar é a conversão da luz do sol em eletricidade, seja diretamente usando energia fotovoltaica (PV), 
            ou indiretamente usando energia solar concentrada (CSP). Os sistemas de energia solar fotovoltaica usam painéis solares 
            compostos de células solares que convertem a luz solar em eletricidade. A energia solar é uma fonte de energia limpa, 
            renovável e abundante. O Brasil tem um dos maiores potenciais de energia solar do mundo devido à sua localização geográfica 
            privilegiada. A instalação de painéis solares residenciais pode reduzir significativamente os custos com energia elétrica 
            e contribuir para a sustentabilidade ambiental.""",
            "summary": "Energia solar converte luz do sol em eletricidade através de painéis fotovoltaicos. O Brasil possui grande potencial devido à sua localização geográfica. A tecnologia reduz custos e contribui para sustentabilidade.",
            "method": "seed"
        },
        {
            "url": "https://www.absolar.org.br/",
            "title": "Associação Brasileira de Energia Solar Fotovoltaica",
            "content": """A ABSOLAR é uma associação sem fins lucrativos que representa o setor de energia solar fotovoltaica no Brasil. 
            O país superou a marca de 35 GW de potência instalada em energia solar, consolidando-se como líder em geração distribuída 
            na América Latina. A energia solar fotovoltaica já beneficia mais de 2,5 milhões de unidades consumidoras no Brasil. 
            O setor tem crescido exponencialmente, gerando milhares de empregos e contribuindo para a diversificação da matriz energética 
            brasileira. As políticas de incentivo e a queda nos custos dos equipamentos têm impulsionado esse crescimento.""",
            "summary": "O Brasil ultrapassou 35 GW de energia solar instalada, beneficiando milhões de consumidores. O setor cresce rapidamente, gerando empregos e diversificando a matriz energética nacional.",
            "method": "seed"
        },
        {
            "url": "https://www.gov.br/mme/pt-br/assuntos/secretarias/energia-eletrica/energia-solar",
            "title": "Ministério de Minas e Energia - Energia Solar",
            "content": """O Ministério de Minas e Energia (MME) apoia o desenvolvimento da energia solar no Brasil através de programas 
            e políticas públicas. A energia solar é estratégica para a transição energética e descarbonização da economia. 
            O governo tem implementado leilões de energia solar e incentivos fiscais para promover investimentos no setor. 
            A meta é aumentar significativamente a participação das fontes renováveis na matriz energética brasileira. 
            A energia solar, junto com eólica e hidrelétrica, forma o tripé das energias limpas no país.""",
            "summary": "O governo brasileiro promove energia solar através de leilões e incentivos fiscais. A estratégia visa aumentar energias renováveis na matriz energética como parte da transição energética.",
            "method": "seed"
        },
        {
            "url": "https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/atlas-brasileiro-de-energia-solar",
            "title": "Atlas Brasileiro de Energia Solar",
            "content": """O Atlas Brasileiro de Energia Solar é uma publicação da Empresa de Pesquisa Energética (EPE) que mapeia 
            o potencial de irradiação solar em todo território nacional. O estudo demonstra que o Brasil possui excelentes condições 
            para aproveitamento da energia solar, com níveis de irradiação superiores aos de países europeus que são referência 
            no uso desta tecnologia. Mesmo as regiões menos favoráveis do Brasil apresentam potencial superior à Alemanha, 
            líder mundial em capacidade instalada fotovoltaica. O Nordeste brasileiro possui os maiores índices de irradiação.""",
            "summary": "O Atlas da EPE mostra que todo o Brasil tem excelente potencial solar, superior a países líderes europeus. O Nordeste apresenta os maiores índices de irradiação do país.",
            "method": "seed"
        },
        {
            "url": "https://www.aneel.gov.br/geracao-distribuida",
            "title": "ANEEL - Geração Distribuída de Energia Solar",
            "content": """A Agência Nacional de Energia Elétrica (ANEEL) regula a geração distribuída no Brasil, permitindo que 
            consumidores residenciais, comerciais e industriais instalem sistemas de micro e minigeração de energia solar. 
            O sistema de compensação de energia permite que a energia excedente seja injetada na rede e compensada na conta de luz. 
            A Resolução Normativa 482/2012 e suas atualizações estabeleceram as regras para conexão e compensação. 
            Milhões de brasileiros já aderiram ao sistema, economizando nas contas de luz e contribuindo para a sustentabilidade.""",
            "summary": "A ANEEL regulamenta a geração distribuída solar permitindo que consumidores produzam energia. O sistema de compensação possibilita redução na conta de luz através da energia excedente.",
            "method": "seed"
        }
    ]
    
    # Criar artigos e resumos
    for idx, data in enumerate(articles_data, 1):
        article = Article.objects.create(
            query=query,
            url=data["url"],
            title=data["title"],
            content=data["content"]
        )
        print(f"  ✓ Artigo {idx}: {article.title[:50]}...")
        
        Summary.objects.create(
            article=article,
            summary_text=data["summary"],
            method=data["method"]
        )
        print(f"    ✓ Resumo criado")
    
    print(f"\n✓ Seed completo! {len(articles_data)} artigos com resumos criados.")
    print(f"  Acesse: http://127.0.0.1:8000/results/{query.id}/")
    
    return query

if __name__ == "__main__":
    # Verificar se já existe query de exemplo
    if SearchQuery.objects.filter(termo="energia solar").exists():
        print("⚠ Já existe uma query 'energia solar'. Pulando seed...")
        print("  Para recriar, delete a query existente primeiro:")
        print("  python manage.py shell -c \"from pesquisador_app.models import SearchQuery; SearchQuery.objects.filter(termo='energia solar').delete()\"")
    else:
        create_seed_data()
