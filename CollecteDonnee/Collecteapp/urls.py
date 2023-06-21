from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),

    path('Capteur/liste_capteur/', views.liste_capteurs),
    path('Capteur/modifier_capteur', views.modifier_capteur),
]