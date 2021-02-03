from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices

User = get_user_model()


class Exam(models.Model):
    class Type(DjangoChoices):
        current_status = ChoiceItem('current_status', _('Current status'))

    type = models.CharField(max_length=50, choices=Type.choices, verbose_name=_('Type'))
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='exams')
    result = models.TextField(verbose_name=_('Result'))

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('Exam')
        verbose_name_plural = _('Exams')
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(type='current_status'),
                name='unique current_status result per user'
            ),
        ]
