import json

from rest_framework import serializers

from .models import Exam


class CustomJsonField(serializers.Field):
    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, value):
        return value


class ExamSerializer(serializers.ModelSerializer):
    result = CustomJsonField()
    translated_type = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Exam
        fields = ('id', 'type', 'translated_type', 'user', 'result')
