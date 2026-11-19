import os
import re
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or None


def _split_sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _paragraphize_from_sentences(text, sentences_per_paragraph=3):
    sentences = _split_sentences(text)
    if not sentences:
        return text.strip()

    paragraphs = []
    for i in range(0, len(sentences), sentences_per_paragraph):
        chunk = " ".join(sentences[i:i + sentences_per_paragraph]).strip()
        if chunk:
            paragraphs.append(chunk)
    return "\n\n".join(paragraphs)


def organize_text(text, paragraphize=False, sentences_per_paragraph=3):
    """Limpa ruídos e opcionalmente estrutura texto em parágrafos."""
    if not text:
        return ""

    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    raw_paragraphs = re.split(r"\n\s*\n", cleaned)
    paragraphs = []
    for p in raw_paragraphs:
        p = re.sub(r"\s+", " ", p).strip()
        p = re.sub(r"([.!?]){2,}", r"\1", p)
        p = re.sub(r"([.!?])(\S)", r"\1 \2", p)
        if p:
            paragraphs.append(p)

    cleaned = "\n\n".join(paragraphs)

    if paragraphize:
        cleaned = _paragraphize_from_sentences(cleaned, sentences_per_paragraph=sentences_per_paragraph)

    return cleaned


def format_summary_text(text):
    """Formata resumo em 1-3 parágrafos curtos e legíveis."""
    base = organize_text(text, paragraphize=True, sentences_per_paragraph=2)
    paragraphs = [p.strip() for p in base.split("\n\n") if p.strip()]
    return "\n\n".join(paragraphs[:3])

def summarize_text(text):
    if not text:
        return ("", "none")
    text = organize_text(text, paragraphize=True, sentences_per_paragraph=3)
    if OPENAI_KEY:
        try:
            return format_summary_text(summarize_with_openai(text)), "openai"
        except Exception as e:
            print("OpenAI failed:", e)
    try:
        return format_summary_text(summarize_with_sumy(text)), "sumy"
    except Exception as e:
        print("Sumy failed:", e)
    fallback = text[:800] + "..." if len(text) > 800 else text
    return (format_summary_text(fallback), "trim")

def summarize_with_openai(text):
    import requests, os
    # Truncar texto para evitar limites de tokens (mantém primeiros 3000 caracteres)
    text_truncated = text[:3000]
    if len(text) > 3000:
        text_truncated += "\n[...texto truncado para caber no limite de tokens...]"
    
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role":"user","content": f"Resuma o texto a seguir em 3 frases curtas:\n\n{text_truncated}"}],
        "max_tokens": 200
    }
    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()

def summarize_with_sumy(text, sentences_count=3):
    try:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lex_rank import LexRankSummarizer
        
        # Truncar se muito longo
        text_truncated = text[:5000] if len(text) > 5000 else text
        
        parser = PlaintextParser.from_string(text_truncated, Tokenizer("portuguese"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return " ".join(str(s) for s in summary)
    except Exception as e:
        print(f"Erro ao sumarizar com sumy: {e}")
        # Fallback: retornar primeiras frases
        return text[:500] + "..." if len(text) > 500 else text
