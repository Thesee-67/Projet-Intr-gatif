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


    path('Donnees/liste_dates/', views.liste_dates, name='liste_dates'),
    path('Donnees/filtre_capteur/', views.filtrer_par_capteur, name='filtrer_par_capteur'),
    path('Donnees/filtre_donnees/', views.filtrer_donnees, name='filtrer_donnees'),
    path('Donnees/csv/', views.generate_csv, name='generate_csv'),
    path('Donnees/supprimer_toutes_donnees/', views.supprimer_toutes_donnees),
    path('Donnees/supprimer_confirm_toutes_donnees/', views.supprimer_confirm_toutes_donnees),
    path('capteurs/', views.selection_capteurs, name='selection_capteurs'),
    path('graphique/', views.graphique, name='graphique'),
    path('contact/', views.contact, name='contact'),
    path('api/models/', views.ModelList.as_view(), name='model-list'),
    path('api/models/<int:pk>/', views.ModelDetail.as_view(), name='model-detail'),

]