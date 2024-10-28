from .models import standard_master,AcademicYear
from rest_framework import serializers


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = standard_master
        fields = '__all__'
        
class StandardMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = standard_master
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']        
        
        

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'year', 'is_current']
        read_only_fields = ['id']                