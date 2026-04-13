import requests, time
from bs4 import BeautifulSoup
from .models import Article, Summary
from .summarize_utils import summarize_text, organize_text
import re
from urllib.parse import quote_plus

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
INVALID_SUMMARY_MARKERS = {
    "não foi possível extrair conteúdo desta página",
    "conteúdo insuficiente para gerar resumo",
    "erro ao gerar resumo",
}


def has_valid_summary(summary_text, method):
    if not summary_text or method == "none":
        return False
    normalized = summary_text.strip().lower()
    if normalized in INVALID_SUMMARY_MARKERS:
        return False
    if len(normalized) < 60:
        return False
    return True

def wikipedia_search_urls(term, max_urls=3):
    """Busca artigos da Wikipedia relacionados ao termo"""
    try:
        print(f"  [Wikipedia] Buscando...")
        query = quote_plus(term)
        
        # API de busca da Wikipedia
        api_url = f"https://pt.wikipedia.org/w/api.php?action=opensearch&search={query}&limit={max_urls}&format=json"
        resp = requests.get(api_url, timeout=10)
        resp.raise_for_status()
        
        data = resp.json()
        titles = data[1]  # Títulos dos artigos
        urls = data[3]    # URLs dos artigos
        
        print(f"  [Wikipedia] Encontrados {len(urls)} artigos")
        return urls
    except Exception as e:
        print(f"  [Wikipedia] Erro: {e}")
        return []

def brave_search_urls(term, max_urls=5):
    """Busca usando Brave Search (sem necessidade de API key para resultados básicos)"""
    try:
        print(f"  [Brave] Buscando...")
        query = quote_plus(term)
        url = f"https://search.brave.com/search?q={query}"
        
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9",
        }
        
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        links = []
        # Buscar resultados orgânicos
        for div in soup.find_all("div", class_=re.compile("snippet")):
            a = div.find("a", href=True)
            if a:
                href = a.get("href")
                if href and href.startswith("http") and "brave.com" not in href:
                    links.append(href)
                    if len(links) >= max_urls:
                        break
        
        print(f"  [Brave] Encontrados {len(links)} URLs")
        return links
    except Exception as e:
        print(f"  [Brave] Erro: {e}")
        return []

def news_api_search(term, max_urls=3):
    """Busca notícias usando RSS feeds públicos"""
    try:
        print(f"  [News] Buscando notícias...")
        query = quote_plus(term)
        
        # Google News RSS (público)
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(rss_url, headers=headers, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.content, "xml")
        items = soup.find_all("item", limit=max_urls)
        
        links = []
        for item in items:
            link_tag = item.find("link")
            if link_tag:
                link = link_tag.text
                # Google News redireciona, pegar URL real se possível
                if link:
                    links.append(link)
        
        print(f"  [News] Encontrados {len(links)} artigos")
        return links
    except Exception as e:
        print(f"  [News] Erro: {e}")
        return []

def fallback_topic_urls(term):
    """URLs manualmente curadas por tópico como último recurso"""
    topic_map = {
        "aquecimento global": [
            "https://pt.wikipedia.org/wiki/Aquecimento_global",
            "https://brasilescola.uol.com.br/geografia/aquecimento-global.htm",
            "https://www.nationalgeographicbrasil.com/meio-ambiente/aquecimento-global",
        ],
        "energia solar": [
            "https://pt.wikipedia.org/wiki/Energia_solar",
            "https://www.portalsolar.com.br/energia-solar",
            "https://brasilescola.uol.com.br/fisica/energia-solar.htm",
        ],
        "inteligência artificial": [
            "https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial",
            "https://brasilescola.uol.com.br/informatica/inteligencia-artificial.htm",
            "https://www.ibm.com/br-pt/topics/artificial-intelligence",
        ],
        "mudanças climáticas": [
            "https://pt.wikipedia.org/wiki/Mudança_do_clima",
            "https://brasilescola.uol.com.br/geografia/mudanca-climatica.htm",
        ],
        "python programação": [
            "https://pt.wikipedia.org/wiki/Python",
            "https://www.python.org/",
            "https://brasilescola.uol.com.br/informatica/python.htm",
        ],
    }
    
    term_lower = term.lower().strip()
    
    # Buscar match exato ou parcial
    for key, urls in topic_map.items():
        if term_lower in key or key in term_lower:
            print(f"  [Fallback] Usando URLs curadas para '{term}'")
            return urls
    
    # Se não encontrou match, tentar Wikipedia genérico
    print(f"  [Fallback] Tentando Wikipedia genérico para '{term}'...")
    wiki_url = f"https://pt.wikipedia.org/wiki/{quote_plus(term)}"
    brasil_escola_search = f"https://brasilescola.uol.com.br/busca/?q={quote_plus(term)}"
    return [wiki_url, brasil_escola_search]

def simple_search_urls(term, max_urls=5):
    """Busca URLs usando múltiplas fontes (Wikipedia, News, Brave, fallback)"""
    print(f"[BUSCA] Procurando por: {term}")
    
    all_links = []
    
    # 1. Tentar Wikipedia primeiro (mais confiável)
    wiki_links = wikipedia_search_urls(term, max_urls=2)
    all_links.extend(wiki_links)
    
    # 2. Tentar Google News RSS
    if len(all_links) < max_urls:
        news_links = news_api_search(term, max_urls=2)
        all_links.extend(news_links)
    
    # 3. Tentar Brave Search
    if len(all_links) < max_urls:
        brave_links = brave_search_urls(term, max_urls - len(all_links))
        all_links.extend(brave_links)
    
    # 4. Se ainda não tem resultados, usar fallback
    if len(all_links) == 0:
        print("  [!] Nenhum resultado encontrado, usando fallback...")
        fallback_links = fallback_topic_urls(term)
        all_links.extend(fallback_links)
    
    # Remover duplicatas mantendo ordem
    seen = set()
    unique_links = []
    for link in all_links:
        # Normalizar URL
        link_clean = link.split("?")[0] if "?" in link else link
        if link_clean not in seen and link not in seen:
            seen.add(link)
            seen.add(link_clean)
            unique_links.append(link)
    
    return unique_links[:max_urls]

def fetch_article_text(url):
    """Extrai título e conteúdo de uma URL"""
    try:
        print(f"    [FETCH] Acessando: {url[:80]}...")
        
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Extrair título
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        elif soup.find("h1"):
            title = soup.find("h1").get_text().strip()
        
        # Remover scripts e styles
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extrair texto dos parágrafos preservando estrutura básica.
        paragraphs = soup.find_all("p")
        text_blocks = [p.get_text(" ", strip=True) for p in paragraphs if p.get_text(strip=True)]
        text = "\n\n".join(text_blocks)
        
        # Se não encontrou parágrafos, tentar outros elementos
        if not text or len(text) < 100:
            article = soup.find("article")
            if article:
                text = article.get_text().strip()
            else:
                main = soup.find("main")
                if main:
                    text = main.get_text().strip()
        
        text = organize_text(text, paragraphize=True, sentences_per_paragraph=3)
        
        print(f"    [FETCH] ✓ Título: {title[:60] if title else 'N/A'}")
        print(f"    [FETCH] ✓ Conteúdo: {len(text)} caracteres")
        
        return text, title
        
    except requests.exceptions.Timeout:
        print(f"    [FETCH] ✗ Timeout ao acessar {url[:60]}")
        return "", ""
    except requests.exceptions.RequestException as e:
        print(f"    [FETCH] ✗ Erro HTTP: {str(e)[:60]}")
        return "", ""
    except Exception as e:
        print(f"    [FETCH] ✗ Erro: {str(e)[:60]}")
        return "", ""

def search_and_fetch(search_query):
    """Busca URLs e extrai conteúdo para uma query"""
    term = search_query.termo
    print(f"\n{'='*60}")
    print(f"[SEARCH] Iniciando busca para: '{term}'")
    print(f"{'='*60}\n")
    
    # Buscar mais URLs e manter apenas os melhores resultados válidos.
    target_valid_articles = 5
    urls = simple_search_urls(term, max_urls=10)
    
    if not urls:
        print(f"\n[SEARCH] ✗ Nenhuma URL encontrada para '{term}'")
        print("[SEARCH] Verifique sua conexão com a internet\n")
        return
    
    print(f"\n[SEARCH] ✓ {len(urls)} URLs encontradas\n")
    
    articles_created = 0
    summaries_created = 0
    skipped_without_summary = 0
    
    # Processar cada URL até atingir quantidade de artigos válidos.
    for idx, url in enumerate(urls, 1):
        if articles_created >= target_valid_articles:
            break

        print(f"[{idx}/{len(urls)}] Processando URL...")
        print(f"  URL: {url}")
        
        # Extrair conteúdo
        content, title = fetch_article_text(url)
        
        # Não salva resultado sem conteúdo minimamente utilizável.
        if not content or len(content) < 180:
            skipped_without_summary += 1
            print(f"  [RESUMO] ⚠ Conteúdo insuficiente ({len(content)} chars). Pulando resultado.")
            print()
            if idx < len(urls):
                time.sleep(2)
            continue

        try:
            print("  [RESUMO] Gerando resumo...")
            summary_text, method = summarize_text(content)
        except Exception as e:
            print(f"  [RESUMO] ✗ Erro ao criar resumo: {e}")
            skipped_without_summary += 1
            print()
            if idx < len(urls):
                time.sleep(2)
            continue

        if not has_valid_summary(summary_text, method):
            skipped_without_summary += 1
            print("  [RESUMO] ⚠ Resumo inválido/insuficiente. Buscando próximo resultado.")
            print()
            if idx < len(urls):
                time.sleep(2)
            continue

        article = Article.objects.create(
            query=search_query,
            url=url,
            title=title if title else f"Artigo {idx}",
            content=content
        )
        articles_created += 1
        print(f"  [DB] ✓ Article #{article.id} criado")

        Summary.objects.create(
            article=article,
            summary_text=summary_text,
            method=method
        )
        summaries_created += 1
        print(f"  [RESUMO] ✓ Resumo criado (método: {method})")
        print(f"  [RESUMO] Preview: {summary_text[:100]}...")
        
        print()  # Linha em branco
        
        # Delay entre requisições para evitar bloqueio
        if idx < len(urls):
            time.sleep(2)
    
    # Resumo final
    print(f"{'='*60}")
    print(f"[SEARCH] ✓ Busca finalizada!")
    print(f"  Query ID: {search_query.id}")
    print(f"  Artigos criados: {articles_created}")
    print(f"  Resumos criados: {summaries_created}")
    print(f"  Resultados descartados (sem resumo válido): {skipped_without_summary}")
    print(f"  Acesse: http://127.0.0.1:8000/results/{search_query.id}/")
    print(f"{'='*60}\n")
