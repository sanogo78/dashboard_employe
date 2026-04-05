from django.urls import path
from . import views

urlpatterns = [
    path('accueil/', views.accueil, name='accueil'),
    path('', views.liste_employes, name='liste_employes'),
    path('employe/<int:pk>/', views.detail_employe, name='detail_employe'),
    path('employe/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employe/<int:pk>/modifier/', views.modifier_employe, name='modifier_employe'),
    path('employe/<int:pk>/supprimer/', views.supprimer_employe, name='supprimer_employe'),
    path('employe/<int:pk>/bulletin/', views.bulletin_employe, name='bulletin_employe'),
]
