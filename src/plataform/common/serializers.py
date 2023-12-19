from django.db.models import fields
from rest_framework import serializers
from .models import Log, AutorizedNumber


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class AutorizedNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutorizedNumber
        fields = '__all__'
