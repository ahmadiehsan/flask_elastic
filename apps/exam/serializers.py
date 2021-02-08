import json

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from helpers.utils import Encryption
from .models import Exam

User = get_user_model()


class ExamResultField(serializers.Field):
    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, value):
        if self._is_json(value):
            return value
        else:
            return json.dumps(value)

    @staticmethod
    def _is_json(value):
        try:
            json.loads(value)
            return True
        except TypeError as e:
            return False


class ExamSerializer(serializers.ModelSerializer):
    result = ExamResultField()
    translated_type = serializers.CharField(source='get_type_display', read_only=True)
    user_id = serializers.CharField(source='user', write_only=True)

    @staticmethod
    def validate_user_id(value):
        try:
            user_id = int(Encryption.decrypt(value))
        except:
            raise ValidationError(_('Invalid user id'))

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError(_('User does not exist'))

    class Meta:
        model = Exam
        fields = ('id', 'type', 'translated_type', 'user_id', 'user', 'result')
        read_only_fields = ('user',)
