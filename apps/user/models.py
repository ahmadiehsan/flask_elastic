from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices


class User(AbstractUser):
    class Gender(DjangoChoices):
        male = ChoiceItem('1', _('Male'))
        female = ChoiceItem('2', _('Female'))
        non_binary = ChoiceItem('3', _('Non-Binary'))

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
