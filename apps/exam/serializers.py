import json

from django.contrib.auth import get_user_model
from rest_framework import serializers

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
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Exam
        fields = ('id', 'type', 'translated_type', 'user_id', 'user', 'result')
        read_only_fields = ('user',)
