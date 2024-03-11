import datetime

from app.internal.models.article import Article
from app.internal.models.hub import Hub

from django.db.utils import IntegrityError


def add_article(article_title: str,
                article_url: str,
                created_at: datetime.datetime,
                author_url: str,
                author_name: str,
                body: str,
                hub: Hub):
    article = Article.objects.filter(url=article_url).first()
    if article:  # already exists
        return

    try:
        article = Article(title=article_title,
                          url=article_url,
                          created_at=created_at,
                          author_url=author_url,
                          author_name=author_name,
                          body=body,
                          hub=hub)
        article.save()
    except IntegrityError:  # hub was deleted in admin
        return
