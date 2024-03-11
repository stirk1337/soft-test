from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=500, unique=True)
    created_at = models.DateTimeField()
    hub = models.ForeignKey('Hub', on_delete=models.CASCADE)
    author_url = models.URLField(max_length=500)
    author_name = models.CharField(max_length=100)
    body = models.TextField()
