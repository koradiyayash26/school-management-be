from .models import standard_master
from rest_framework import serializers


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = standard_master
        fields = '__all__'