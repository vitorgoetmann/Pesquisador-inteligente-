from django.core.management.base import BaseCommand
from pesquisador_app.models import SearchQuery
from pesquisador_app.search_utils import search_and_fetch

class Command(BaseCommand):
    help = "Run a search: --term '...'"

    def add_arguments(self, parser):
        parser.add_argument("--term", type=str, required=True)

    def handle(self, *args, **options):
        term = options["term"]
        q = SearchQuery.objects.create(termo=term)
        self.stdout.write(f"Criada query {q.id} {term}")
        search_and_fetch(q)
        self.stdout.write("Busca finalizada.")
