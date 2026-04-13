from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import SearchQuery
from .search_utils import search_and_fetch


def _query_dashboard_queryset():
    return SearchQuery.objects.annotate(
        total_articles=Count("articles", distinct=True),
        valid_summaries=Count(
            "articles__summary",
            filter=~Q(articles__summary__method="none")
            & ~Q(articles__summary__summary_text__isnull=True)
            & ~Q(articles__summary__summary_text__exact=""),
            distinct=True,
        ),
    )


def home(request):
    queries = _query_dashboard_queryset().order_by("-created_at")[:8]
    return render(request, "pesquisador_app/home.html", {"queries": queries})


def queries(request):
    query_list = _query_dashboard_queryset().order_by("-created_at")
    return render(request, "pesquisador_app/queries.html", {"queries": query_list})

def submit_search(request):
    if request.method == "POST":
        termo = request.POST.get("termo")
        if termo:
            q = SearchQuery.objects.create(termo=termo)
            # para MVP rodamos síncrono (Copilot poderá paralelizar)
            search_and_fetch(q)
            return redirect("results", query_id=q.id)
    return redirect("home")

def results(request, query_id):
    q = get_object_or_404(SearchQuery, id=query_id)
    articles = (
        q.articles
        .select_related("summary")
        .exclude(summary__method="none")
        .exclude(summary__summary_text__isnull=True)
        .exclude(summary__summary_text__exact="")
        .exclude(summary__summary_text__iexact="Não foi possível extrair conteúdo desta página")
        .order_by("-fetched_at")
    )
    return render(request, "pesquisador_app/results.html", {"query": q, "articles": articles})


def delete_query(request, query_id):
    if request.method == "POST":
        q = get_object_or_404(SearchQuery, id=query_id)
        q.delete()
    return redirect("home")
