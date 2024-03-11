from django.urls import path

from app.internal.transport.rest.handlers import hello

urlpatterns = [
    path('hello/', hello)
]
