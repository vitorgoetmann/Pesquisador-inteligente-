import os, sys, django
from openpyxl import Workbook

# Adicionar o diretório pai ao path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE","pesquisador_project.settings")
django.setup()
from pesquisador_app.models import SearchQuery

def export_query(qid):
    q = SearchQuery.objects.get(id=qid)
    wb = Workbook()
    ws = wb.active
    ws.title = q.termo[:31]
    ws.append(["title","url","summary","method"])
    for a in q.articles.all():
        s = getattr(a, "summary", None)
        ws.append([a.title or "", a.url, s.summary_text if s else "", s.method if s else ""])
    fn = f"pesquisa_{q.id}.xlsx"
    wb.save(fn)
    print("Salvo", fn)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        qid = int(sys.argv[1])
        export_query(qid)
    else:
        print("Uso: python scripts\\export_search.py <query_id>")
        print("\nQueries disponíveis:")
        for q in SearchQuery.objects.all():
            print(f"  ID {q.id}: {q.termo} ({q.articles.count()} artigos)")
        print("\nExemplo: python scripts\\export_search.py 2")
