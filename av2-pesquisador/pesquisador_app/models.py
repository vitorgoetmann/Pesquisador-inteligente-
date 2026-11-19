from django.db import models

class SearchQuery(models.Model):
    termo = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.termo} @ {self.created_at:%Y-%m-%d %H:%M}"

class Article(models.Model):
    query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name="articles")
    url = models.TextField()
    title = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField(blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title or self.url[:60]

class Summary(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="summary")
    summary_text = models.TextField()
    method = models.CharField(max_length=50, default="auto")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.summary_text[:80]
