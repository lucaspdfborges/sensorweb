from rest_framework import serializers
from .models import DashData
from django.contrib.auth.models import User

class DashDataSerializer(serializers.ModelSerializer):

    pesquisador = serializers.PrimaryKeyRelatedField(queryset=DashData.objects.all())

    class Meta:
        model = DashData
        fields = ('pesquisador','data','experimento','dado')

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
