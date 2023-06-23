from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('Capteur/liste_capteur/', views.liste_capteurs),
    path('Capteur/ajouter_capteur/', views.ajouter_capteur),
    path('Capteur/modifier_capteur/<str:id_capteur>/', views.modifier_capteur),
    path('Capteur/supprimer_capteur/<str:id_capteur>/', views.supprimer_capteur),
    path('Capteur/supprimer_confirm_capteur/<str:id_capteur>/', views.supprimer_confirm_capteur),

    path('Donnees/liste_donnees/', views.liste_donnees),
    path('Donnees/ajouter_donnees/', views.ajouter_donnees),
    path('Donnees/modifier_donnees/<str:id>/', views.modifier_donnees),
    path('Donnees/supprimer_donnees/<str:id>/', views.supprimer_donnees),
    path('Donnees/supprimer_confirm_donnees/<str:id>/', views.supprimer_confirm_donnees),


    #path('receive_message/', views.receive_message, name='receive_message'),
]