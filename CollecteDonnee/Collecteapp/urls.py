from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),

    path('Capteur/liste_capteur/', views.liste_capteurs),
    path('Capteur/ajouter_capteur', views.ajouter_capteur),
    path('Capteur/modifier_capteur/<int:di>/', views.modifier_capteur),
    path('Capteur/supprimer_capteur/<int:di>/', views.supprimer_capteur),
    path('Capteur/supprimer_confirm_capteur/<int:di>/', views.supprimer_confirm_capteur),
]