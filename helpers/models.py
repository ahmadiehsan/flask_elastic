from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('create time'))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_('modify time'))

    @property
    def update_time_formatted(self):
        return self.update_time.strftime("%b %d %Y, %H:%M")

    @property
    def create_time_formatted(self):
        return self.create_time.strftime("%b %d %Y, %H:%M")

    @property
    def update_date_formatted(self):
        return self.update_time.strftime("%b %d %Y")

    @property
    def create_date_formatted(self):
        return self.create_time.strftime("%b %d %Y")

    class Meta:
        ordering = ('-update_time',)
        abstract = True
