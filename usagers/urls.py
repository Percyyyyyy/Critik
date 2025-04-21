from django.urls import path
from usagers.views import EnregistrementView


urlpatterns = [
    path('',EnregistrementView.as_view(),name="enregistrement"),

]