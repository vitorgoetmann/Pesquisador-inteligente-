# Pesquisador Inteligente

Aplicação Django que pesquisa conteúdo na web, extrai artigos, produz resumos e organiza o histórico de consultas.

[**Ver demonstração**](https://pesquisador-inteligente.vercel.app)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2%2B-092E20?logo=django&logoColor=white)
![OpenAI](https://img.shields.io/badge/resumos-IA%20%2B%20fallback-412991?logo=openai&logoColor=white)

## Objetivo

Transformar uma pesquisa aberta em um conjunto organizado de fontes e resumos. O sistema registra cada consulta, coleta páginas relacionadas ao tema, extrai o conteúdo relevante e apresenta os resultados em uma interface navegável.

## Funcionalidades

- Pesquisa por tema em múltiplas fontes.
- Coleta de URLs e extração de conteúdo com Beautiful Soup.
- Resumo por artigo usando OpenAI quando configurada.
- Fallback local de sumarização com Sumy.
- Histórico de pesquisas e métricas.
- Painel administrativo Django.
- Comando de pesquisa pelo terminal.
- Exportação dos resultados para Excel.
- Scripts para dados de demonstração e criação de usuário administrativo.

## Fluxo da aplicação

```text
Consulta → busca de fontes → extração de texto → resumo → persistência → visualização/exportação
```

O código principal está em [`av2-pesquisador/`](av2-pesquisador/).

## Stack

Python · Django · Requests · Beautiful Soup · Sumy · OpenAI API · OpenPyXL

## Executando localmente

```bash
git clone https://github.com/vitorgoetmann/Pesquisador-inteligente-.git
cd Pesquisador-inteligente-/av2-pesquisador
python -m venv .venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Variáveis opcionais:

```env
DJANGO_SECRET_KEY=
DJANGO_DEBUG=True
OPENAI_API_KEY=
```

Sem `OPENAI_API_KEY`, o projeto utiliza o resumidor local.

## Comandos úteis

```bash
python manage.py run_search --term "inteligência artificial"
python scripts/seed_data.py
python scripts/export_search.py <query_id>
```

## Autor

Desenvolvido por [Vitor Goetmann](https://github.com/vitorgoetmann).
