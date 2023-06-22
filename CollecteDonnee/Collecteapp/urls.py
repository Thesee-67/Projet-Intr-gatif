from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Capteur/liste_capteur/', views.liste_capteurs),
    path('Capteur/ajouter_capteur', views.ajouter_capteur),
    path('Capteur/modifier_capteur/<str:di>/', views.modifier_capteur),
    path('Capteur/supprimer_capteur/<str:di>/', views.supprimer_capteur),

    path('Donnees/liste_donnees/', views.liste_donnees),
    path('Donnees/ajouter_donnees/', views.ajouter_donnees),
    path('Donnees/modifier_donnees/<int:di>/', views.modifier_donnees),
    path('Donnees/supprimer_donnees/<int:di>/', views.supprimer_donnees),



    path('receive_message/', views.receive_message, name='receive_message'),
]