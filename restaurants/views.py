from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.db.models import Avg, Q, F
from django.db.models.functions import Coalesce

from restaurants.forms import CommentaireForm, FormulaireModificationRestaurant, RestaurantForm
from restaurants.models import Commentaire, Restaurant, TypeResto

# Create your views here.
class AccueilRestaurant(ListView):
    model = Restaurant
    template_name = 'accueilRestaurant.html'
    context_object_name = 'lstRestaurants'

    def get_queryset(self):
        queryset = super().get_queryset()
        type_restaurant = self.request.GET.get('typeRestaurant')
        ville = self.request.GET.get('villeRestaurant')
        avec_note = self.request.GET.get('avecNote') == 'true'
        tri_note = self.request.GET.get('triNote') 

        if type_restaurant:
            queryset = queryset.filter(typeRestaurant__nomType=type_restaurant)
        
        if ville:
            queryset = queryset.filter(villeRestaurant__icontains=ville)
        
        if avec_note:
            queryset = queryset.exclude(noteRestaurant__isnull=True)

            
        if tri_note == 'asc':
            queryset = queryset.order_by('-noteRestaurant')
        elif tri_note == 'desc':
            queryset = queryset.order_by('noteRestaurant')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['villeSaisie'] = self.request.GET.get('villeRestaurant', '')
        context['typeRestaurants'] = TypeResto.objects.all()
        context['typeSaisi'] = self.request.GET.get('typeRestaurant', '')
        context['avecNote'] = self.request.GET.get('avecNote') == 'true'
        context['triNote'] = self.request.GET.get('triNote', '')  
        return context
    def post(self, request, *args, **kwargs):
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return redirect('accueilRestaurant')
        else:

            return self.render_to_response(self.get_context_data(form=form))
    
class DetailRestaurant(DetailView):
    model = Restaurant
    template_name = 'detailRestaurant.html'
    context_object_name = 'leRestaurant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Vérifier si l'utilisateur a déjà commenté ce restaurant
        user = self.request.user
        if user.is_authenticated:
            context['commentaire_exist'] = Commentaire.objects.filter(userName=user, noRestaurant=self.object).exists()
        context['commentaire_form'] = CommentaireForm() 
        return context

    def post(self, request, *args, **kwargs):
        restaurant = self.get_object()
        commentaire_form = CommentaireForm(request.POST)
        if commentaire_form.is_valid():
            nouveau_commentaire = commentaire_form.save(commit=False)
            nouveau_commentaire.userName = request.user
            nouveau_commentaire.noRestaurant = restaurant
            nouveau_commentaire.save()
            return redirect('detailRestaurant', pk=restaurant.pk)
        else:
            return self.render_to_response(self.get_context_data(commentaire_form=commentaire_form))

class ModifierRestaurantView(View):
    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        form = FormulaireModificationRestaurant(instance=restaurant)
        context = {'form': form}
        return render(request, 'modifierRestaurant.html', context)

    def post(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        form = FormulaireModificationRestaurant(request.POST, instance=restaurant)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return redirect('accueilRestaurant')
        context = {'form': form}
        return render(request, 'modifierRestaurant.html', context)

class SupprimerRestaurantView(View):
    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        context = {'leRestaurant': restaurant}
        return render(request, 'supprimerRestaurant.html', context)

    def post(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        restaurant.delete()
        return redirect('accueilRestaurant')

class MesCommentairesView(View):
    def get(self, request):
        user = request.user
        
        commentaires = Commentaire.objects.filter(userName=user)
        print(commentaires)
        
        context = {'commentaires': commentaires}
        
        return render(request, 'mesCommentaires.html', context)
    
class ModifierCommentaire(UpdateView):
    model = Commentaire
    form_class = CommentaireForm
    template_name = 'modifierCommentaire.html'
    success_url = reverse_lazy('accueilRestaurant')

    def get(self, request, *args, **kwargs):
        commentaire = self.get_object()
        form = self.form_class(instance=commentaire)
        return render(request, self.template_name, {'form': form, 'commentaire': commentaire})

    def post(self, request, *args, **kwargs):
        commentaire = self.get_object()
        form = self.form_class(request.POST, instance=commentaire)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return redirect(self.success_url, pk=commentaire.noRestaurant.pk)  # 
        return render(request, self.template_name, {'form': form, 'commentaire': commentaire})
    
class SupprimerCommentaireView(View):
    def get(self, request, pk):
        leCommentaire = get_object_or_404(Commentaire, pk=pk)
        context = {'leCommentaire': leCommentaire}
        return render(request, 'supprimerCommentaire.html', context)

    def post(self, request, pk):
        leCommentaire = get_object_or_404(Commentaire, pk=pk)
        leCommentaire.delete()
        return redirect('accueilRestaurant')
