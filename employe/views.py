from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Employe
from .form import EmployeForm
from django.template.loader import render_to_string
from django.templatetags.static import static
import weasyprint
from django.http import HttpResponse


# Create your views here.
# Cette partie nous permet de definir les parties qui seront afficher a l'écran de l'utilisateur

def accueil(request):
    return render(request, 'accueil.html')

def liste_employes(request):
    query = request.GET.get('q', '').strip()
    employes = Employe.objects.all() # on prend tous les employes
    if query:
        employes = employes.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(id__icontains=query)
        )
    return render(request, 'liste_employes.html', {'employes': employes, 'query': query})


# detail d'un employe
def detail_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    return render(request, 'detail_employes.html', {'employe': employe})


# ajouter un employe
def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm()
    return render(request, 'ajouter_employe.html', {'form': form})

# modifier un employe
def modifier_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        form = EmployeForm(request.POST, request.FILES, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'modifier_employe.html', {'form': form})

#Supprimer un employe
def supprimer_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.delete()
        return redirect('liste_employes')
    return render(request, 'supprimer_employe.html', {'employe': employe})

# Impression de la fiche employer
def bulletin_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    photo_url = None
    css_url = request.build_absolute_uri(static('css/bulletin.css'))

    if employe.photo:
        photo_url = request.build_absolute_uri(employe.photo.url)

    html = render_to_string('bulletin_employe.html', {
        'employe': employe,
        'photo_url': photo_url,
        'css_url': css_url,
    })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="bulletin_{employe.nom}_{employe.prenom}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf(response)
    return response
