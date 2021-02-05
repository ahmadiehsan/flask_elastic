from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('create time'))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_('modify time'))

    class Meta:
        ordering = ('create_time',)
        abstract = True
