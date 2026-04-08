from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from .models import ActiveUserSession

# ajouter pour detecter l'inactivité de l'utilisateur sur la plateforme et le deconnecter automatiquement apres 15 minutes d'inactivité
# branché dans settings.py dans la section MIDDLEWARE
class SessionIdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now_ts = int(timezone.now().timestamp())
            last_activity = request.session.get("last_activity")
            timeout_seconds = int(getattr(settings, "SESSION_COOKIE_AGE", 15 * 60))

            if last_activity and now_ts - last_activity > timeout_seconds:
                ActiveUserSession.objects.filter(
                    user=request.user,
                    session_key=request.session.session_key,
                ).update(session_key=None)
                logout(request)
                messages.warning(
                    request,
                    "Votre session a expiré après 15 minutes d’inactivité",
                )
                return redirect("login")

            request.session["last_activity"] = now_ts

        return self.get_response(request)
