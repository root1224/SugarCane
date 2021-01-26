""" Users models. """
# Django
# https://github.com/django/django/blob/master/django/contrib/auth/models.py
from django.db import models # https://docs.djangoproject.com/en/3.1/ref/models/fields/
from django.contrib.auth.models import User  # https://docs.djangoproject.com/en/3.1/topics/auth/default/
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    """ Profile model.
    Proxy model that extends the base data with other
    information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(
        upload_to='users/picture',
        blank=True,
        null=True
    )

    is_expert = models.BooleanField(
        _('expert'),
        default=False,
        help_text=_(
            'Asigna si este usuario es tiene las herramientas de procesamiento de imagenes.'
        ),
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Return username. """
        return self.user.username
