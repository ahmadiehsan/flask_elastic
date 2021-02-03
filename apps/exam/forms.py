from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Exam


class CurrentStatusForm(forms.Form):
    one = forms.CharField(label='1- Select the correct color')
    two = forms.CharField(label='2- What is the next ...')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        if Exam.objects.filter(user=self.user, type=Exam.Type.current_status).exists():
            raise ValidationError(_('The user has already taken the test'))
