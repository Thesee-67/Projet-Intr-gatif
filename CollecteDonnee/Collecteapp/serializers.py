from rest_framework import serializers
from .models import Donnees

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donnees
        fields = '__all__'
