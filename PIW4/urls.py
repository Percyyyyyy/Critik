from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as authentification_views

from PIW4.views import AccueilView, AdministrationView
from restaurants.views import MesCommentairesView
from usagers.views import LogoutView

urlpatterns = [
    path('', AccueilView.as_view(), name='accueil'),
    path('admin/', admin.site.urls),
    path('restaurants/', include("restaurants.urls"), name='restaurants'),
    path('login/',authentification_views.LoginView.as_view(template_name="usagers/login.html"),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('enregistrement/',include("usagers.urls")),
    path('mesCommentaires/', MesCommentairesView.as_view(), name='mesCommentaires'),
    path('administration/',AdministrationView.as_view(),name='administration'),
    path('captcha/', include('captcha.urls')),

]
