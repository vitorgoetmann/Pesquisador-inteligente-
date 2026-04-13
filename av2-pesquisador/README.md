# Pesquisador Inteligente

Aplicacao Django para buscar conteudo na web, extrair texto, gerar resumos automaticamente e visualizar resultados de forma organizada.

## Visao Geral

- Busca por tema com coleta de URLs em multiplas fontes.
- Extracao de conteudo e geracao de resumo por artigo.
- Pipeline de resumo com OpenAI (quando configurado) e fallback local com Sumy.
- Interface web com paginas separadas para inicio, historico e resultados.
- Painel administrativo Django para gerenciamento dos dados.

## Stack

- Python 3.10+
- Django 4.2+
- requests + BeautifulSoup4
- sumy
- openpyxl
- python-dotenv

## Estrutura do Projeto

```text
av2-pesquisador/
|-- manage.py
|-- requirements.txt
|-- pesquisador_project/
|-- pesquisador_app/
|   |-- management/commands/run_search.py
|   |-- search_utils.py
|   |-- summarize_utils.py
|   |-- views.py
|   `-- models.py
|-- templates/pesquisador_app/
|   |-- base.html
|   |-- home.html
|   |-- queries.html
|   `-- results.html
|-- static/pesquisador_app/
|   |-- css/style.css
|   `-- js/app.js
`-- scripts/
```

## Como Rodar

1. Criar e ativar ambiente virtual.
2. Instalar dependencias.
3. Configurar variaveis de ambiente.
4. Aplicar migrations.
5. Subir servidor.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Aplicacao local: http://127.0.0.1:8000/

## Variaveis de Ambiente

Crie o arquivo `.env` na raiz:

```ini
DJANGO_SECRET_KEY=sua_chave
DJANGO_DEBUG=True
OPENAI_API_KEY=
```

- Se `OPENAI_API_KEY` estiver vazia, o projeto usa fallback local para resumo.

## Comandos Uteis

### Executar busca pelo terminal

```powershell
python manage.py run_search --term "inteligencia artificial"
```

### Criar superusuario

```powershell
python manage.py createsuperuser
```

### Popular base com dados de exemplo

```powershell
python scripts\seed_data.py
```

### Exportar uma busca para Excel

```powershell
python scripts\export_search.py <query_id>
```

## Fluxo das Paginas

- `/`: cria nova busca e mostra ultimas pesquisas.
- `/queries/`: lista historico completo com metricas.
- `/results/<id>/`: exibe artigos e resumos validos da busca.
- `/admin/`: gerenciamento administrativo.

## Licenca

Uso academico/educacional.
