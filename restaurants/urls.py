from django.contrib import admin
from django.urls import include, path

from restaurants.views import AccueilRestaurant, DetailRestaurant, MesCommentairesView, ModifierRestaurantView, SupprimerRestaurantView, ModifierCommentaire, SupprimerCommentaireView

urlpatterns = [
    path('',AccueilRestaurant.as_view(), name="accueilRestaurant"),
    path('detailRestaurant/<str:pk>/', DetailRestaurant.as_view(), name='detailRestaurant'),
    path('ajouterCommentaire/<str:pk>/', DetailRestaurant.as_view(), name='ajouterCommentaire'),
    path('modifierCommentaire/<int:pk>/', ModifierCommentaire.as_view(), name='modifierCommentaire'),
    path('supprimerCommentaire/<int:pk>/', SupprimerCommentaireView.as_view(), name='supprimerCommentaire'),
    path('ajouterRestaurant/', AccueilRestaurant.as_view(), name='ajouterRestaurant'),
    path('modifierRestaurant/<str:pk>/', ModifierRestaurantView.as_view(), name='modifierRestaurant'),
    path('supprimerRestaurant/<str:pk>/', SupprimerRestaurantView.as_view(), name='supprimerRestaurant'), 
    path('mesCommentaires/', MesCommentairesView.as_view(), name='mesCommentaires'),

]
