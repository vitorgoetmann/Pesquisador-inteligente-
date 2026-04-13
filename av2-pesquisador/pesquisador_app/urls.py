from django.urls import path
from . import views

urlpatterns = [
  path("", views.home, name="home"),
  path("queries/", views.queries, name="queries"),
  path("search/", views.submit_search, name="submit_search"),
  path("results/<int:query_id>/", views.results, name="results"),
  path("queries/<int:query_id>/delete/", views.delete_query, name="delete_query"),
]
