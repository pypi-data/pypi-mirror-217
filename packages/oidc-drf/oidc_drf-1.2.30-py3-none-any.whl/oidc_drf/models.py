from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AnonymousUser


class OIDCExtraData(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    data = models.JSONField()

    def __str__(self):
        return str(self.user)
    

class OIDCUser(AnonymousUser):
    @property
    def is_authenticated(self):
        # Always return True. This is a way to tell if
        # the user has been authenticated in permissions
        return True