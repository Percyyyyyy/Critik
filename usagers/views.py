from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout, login
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, FormView
from usagers.forms import EnregistrementForm
# Create your views here.

class EnregistrementView(FormView):
    template_name = 'usagers/enregistrement.html'
    form_class = EnregistrementForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Bonjour {username}, vous êtes enregistré !')
        return redirect('login')

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        form = EnregistrementForm() 
        return redirect('accueil')