from django.urls import path
from . import views

urlpatterns = [
    path('demande-pret', views.demandePret, name='demandepret'),
    path('retour-livre', views.retourLivre, name='retourlivre'),    
    path('attente-livre', views.attLivre, name='attentelivre'), 
   
]