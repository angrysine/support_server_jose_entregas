from django.db.models import fields
from rest_framework import serializers
from .models import Log, AuthorizedNumber


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class AuthorizedNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizedNumber
        fields = '__all__'
