from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices

from helpers.models import BaseModel

User = get_user_model()


class Exam(BaseModel):
    class Type(DjangoChoices):
        visual_memory = ChoiceItem('vm', _('Visual memory'))
        working_memory = ChoiceItem('wm', _('Working memory'))
        orientation = ChoiceItem('o', _('Orientation'))
        perspective_taking = ChoiceItem('pt', _('Perspective taking'))

    type = models.CharField(max_length=50, choices=Type.choices, verbose_name=_('Type'))
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='exams')
    result = models.TextField(verbose_name=_('Result'))

    def __str__(self):
        return '{}, {}'.format(self.user, self.type)

    class Meta:
        verbose_name = _('Exam')
        verbose_name_plural = _('Exams')
