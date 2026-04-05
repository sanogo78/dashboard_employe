from django import forms
from .models import Employe
from django.core.exceptions import ValidationError
from django.utils import timezone

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = '__all__'
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Ex: 0123456789'}),
        }
        help_texts = {
            'nom': 'Entrez le nom de famille.',
            'prenom': 'Entrez le prénom.',
            'sexe': 'Sélectionnez le sexe.',
            'date_naissance': 'Format: JJ/MM/AAAA',
            'adresse': 'Adresse complète (optionnel).',
            'date_embauche': 'Date d\'embauche.',
            'etat_civil': 'Sélectionnez l\'état civil.',
            'telephone': '10 chiffres sans espaces (optionnel).',
            'fonction': 'Sélectionnez la fonction.',
            'photo': 'Image JPG/PNG (optionnel).',
        }

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if date_naissance and date_naissance >= timezone.now().date():
            raise ValidationError("La date de naissance doit être dans le passé.")
        return date_naissance

    def clean_date_embauche(self):
        date_embauche = self.cleaned_data.get('date_embauche')
        if date_embauche and date_embauche > timezone.now().date():
            raise ValidationError("La date d'embauche ne peut pas être dans le futur.")
        return date_embauche

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            if not telephone.isdigit() or len(telephone) != 10:
                raise ValidationError("Le numéro de téléphone doit contenir exactement 10 chiffres.")
        return telephone