from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices


class User(AbstractUser):
    class Gender(DjangoChoices):
        male = ChoiceItem('m', _('Male'))
        female = ChoiceItem('f', _('Female'))
        non_binary = ChoiceItem('n', _('Non-Binary'))

    email = models.EmailField(
        _('Email Address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists"),
        },
    )
    birthdate = models.DateField(
        _('Birthdate'),
        null=True
    )
    gender = models.CharField(
        _('Gender'),
        max_length=1,
        choices=Gender.choices,
        null=True
    )
