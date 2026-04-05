from django import forms
from .models import Employe

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = '__all__' # ON prend tous les champs du formalaires