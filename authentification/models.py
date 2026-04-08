from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ActiveUserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='active_session')
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"Session active de {self.user.username}"
