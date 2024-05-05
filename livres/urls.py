from django.urls import path

from livres import views

urlpatterns = [
    path('livres', views.livres, name="livres"),
]