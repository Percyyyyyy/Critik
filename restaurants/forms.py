from django import forms
from .models import Commentaire, TypeResto, Restaurant
from captcha.fields import CaptchaField


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['commentaire', 'note']

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['nomRestaurant', 'villeRestaurant', 'adresseRestaurant', 'typeRestaurant']

class TypeRestoForm(forms.ModelForm):
    class Meta:
        model = TypeResto
        fields = ['nomType'] 
        widgets = {
            'nomType': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nomType'].label = 'Type de Restaurant'
        self.fields['nomType'].choices = [(type_resto.noType, type_resto.nomType) for type_resto in TypeResto.objects.all()]

class FormulaireAjoutRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['nomRestaurant', 'villeRestaurant', 'typeRestaurant']
        widgets = {
            'nomRestaurant': forms.TextInput(attrs={'class': 'form-control'}),
            'villeRestaurant': forms.TextInput(attrs={'class': 'form-control'}),
            'adresseRestaurant': forms.TextInput(attrs={'class': 'form-control'}),
            'typeRestaurant': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['typeRestaurant'].queryset = TypeResto.objects.all()

class FormulaireModificationRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['nomRestaurant', 'villeRestaurant', 'adresseRestaurant', 'typeRestaurant']
        widgets = {
            'nomRestaurant': forms.TextInput(attrs={'class': 'form-control'}),
            'villeRestaurant': forms.TextInput(attrs={'class': 'form-control'}),
            'adresseRestaurant': forms.TextInput(attrs={'class': 'form-control'}),
            'typeRestaurant': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['typeRestaurant'].queryset = TypeResto.objects.all()

class FormulaireSelectionRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['villeRestaurant']
        widgets = {
            'villeRestaurant': forms.Select(attrs={'class': 'form-control'}),
        }