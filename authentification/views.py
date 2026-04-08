from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sessions.models import Session
from django.utils import timezone
from .token import generatorToken
from .models import ActiveUserSession

# Create your views here.

def home(request):
    return render(request, 'accueil.html')

def register(request):
    if request.method == "POST":
        # on recupère les données entrer par l'utilisateurs.
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        # verification des données de l'tulisateur existantes
        if User.objects.filter(username=username):
            messages.error(request, "Ce nom d'utilisateur est déjà utilisé !")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, "Ce mail a déjà été utiliser !")
            return redirect('register')
        if not username.isalnum():
            messages.error(request, 'Saisissez un nom correct SVP !')
            return redirect('register')
        if password != password1:
            messages.error(request, 'Les mot de pass ne corresponde pas !')
            return redirect('register')
        
        mon_utilisteur = User.objects.create_user(username, email, password)
        mon_utilisteur.first_name = firstname
        mon_utilisteur.last_name = lastname
        mon_utilisteur.is_active = False
        mon_utilisteur.save() # pour enregistrer l'utilisateur
        messages.success(request, 'Votre compte a été créer avec succès !')
        # Envoi d'email de bienvenue
        subject = "Bienvenue chez TOP QUALITÉ !"
        message = "Bienvenue" + " \t" + str(mon_utilisteur) + "\n\n Nous sommes heureux de vous compter parmi nous \n\n\n Merci ! \n\n cordialement\n SANOGO PONNON MADOU"
        from_email = settings.EMAIL_HOST_USER
        to_list = [mon_utilisteur.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
    # Mail de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmation de l'adresse mail sur top qualité authen"
        messageConfirm = render_to_string('emailconfirm.html', {
            'name': mon_utilisteur.first_name,
            'domain': current_site.domain,
            'css_url': request.build_absolute_uri(static('css/emailconfirm.css')),
            'uidb64': urlsafe_base64_encode(force_bytes(mon_utilisteur.pk)),
            'token': generatorToken.make_token(mon_utilisteur),
        })
        
        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [mon_utilisteur.email]
        )
        
        email.fail_silently = False
        email.content_subtype = "html"
        email.send()
        
        return redirect('login')
        
    return render(request, 'register.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            active_session, _ = ActiveUserSession.objects.get_or_create(user=user)
            existing_session_key = active_session.session_key

            if existing_session_key:
                session_is_active = Session.objects.filter(
                    session_key=existing_session_key,
                    expire_date__gt=timezone.now(),
                ).exists()
                current_session_key = request.session.session_key

                if session_is_active and existing_session_key != current_session_key:
                    messages.error(
                        request,
                        "Une session est déjà active pour cet utilisateur sur un autre navigateur.",
                    )
                    return redirect('login')

                if not session_is_active:
                    active_session.session_key = None
                    active_session.save(update_fields=['session_key'])

            login(request, user)
            if request.session.session_key is None:
                request.session.save()
            active_session.session_key = request.session.session_key
            active_session.save(update_fields=['session_key'])
            return redirect('liste_employes')
        my_user = User.objects.filter(username=username).first()
        if my_user is not None and my_user.is_active is False:
            messages.error(request, "Vous n'avez pas confirmé votre adresse e-mail, faites-le avant de vous connecter.")
            return redirect('login')
        else:
            messages.error(request, 'Mauvaise authentification')
            return redirect('login')
        
    return render(request, 'login.html')

def logOut(request):
    if request.user.is_authenticated:
        ActiveUserSession.objects.filter(
            user=request.user,
            session_key=request.session.session_key,
        ).update(session_key=None)
    logout(request)
    messages.success(request, 'Vous avez été bien déconnecter !')
    return redirect('accueil')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Votre compte a été activé avec succès ! Vous pouvez maintenant vous connecter.')
        return redirect('login')
    else:
        messages.error(request, 'Le lien d\'activation est invalide ou a expiré.')
        return redirect('accueil')
