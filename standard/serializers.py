from .models import standard_master,AcademicYear
from rest_framework import serializers


class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = standard_master
        fields = '__all__'
        
class StandardMasterSerializer(serializers.ModelSerializer):
    SCHOOL_TYPE_CHOICES = (
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
    )
    
    school_type = serializers.ChoiceField(choices=SCHOOL_TYPE_CHOICES, default='Primary')
    
    class Meta:
        model = standard_master
        fields = ['id', 'name', 'school_type','is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']        
        
        

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'year', 'is_current']
        read_only_fields = ['id']                