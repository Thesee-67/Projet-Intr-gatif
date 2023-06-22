from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Capteur/liste_capteur/', views.liste_capteurs),
    path('Capteur/ajouter_capteur', views.ajouter_capteur),
    path('Capteur/modifier_capteur/<str:di>/', views.modifier_capteur),
    path('Capteur/supprimer_capteur/<str:di>/', views.supprimer_capteur),
    path('Capteur/supprimer_confirm_capteur/<str:di>/', views.supprimer_confirm_capteur),

    path('Donnees/liste_donnees/', views.liste_Donnes),
    path('Donnees/ajouter_donnees/', views.ajouter_donnees),
    path('Donnees/supprimer_donnees/<int:id>/', views.supprimer_donnes),
    path('Donnees/supprimer_confirm_donnees/<int:id>/', views.supprimer_confirm_donnees),
    path('Donnees/modifier_donnees/<int:id>/', views.modifier_donnees),
]