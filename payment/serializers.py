from rest_framework import serializers
from .models import fee_type, fee_type_master, standard_master,ReceiptDetail,Receipt,Students

class FeeTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = fee_type_master
        fields = '__all__'

class StandardMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = standard_master
        fields = '__all__'

class FeeTypePostSerializer(serializers.ModelSerializer):
    # fee_master = FeeTypeMasterSerializer()
    fee_master = serializers.PrimaryKeyRelatedField(queryset=fee_type_master.objects.all())
    standard = serializers.PrimaryKeyRelatedField(queryset=standard_master.objects.all())

    class Meta:
        model = fee_type
        fields = ['id', 'fee_master', 'amount', 'standard', 'year', 'is_active']


class StandardMasterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = standard_master
        fields = ['id', 'name']

class FeeTypeGetSerializer(serializers.ModelSerializer):
    fee_master = FeeTypeMasterSerializer()
    standard = StandardMasterDetailSerializer()  # Use the new serializer instead of PrimaryKeyRelatedField
    standard_name = serializers.SerializerMethodField()  # Add this field

    class Meta:
        model = fee_type
        fields = ['id', 'fee_master', 'amount', 'standard', 'standard_name', 'year', 'is_active']

    def get_standard_name(self, obj):
        # Return 'Balvatika' for standard_id 7, otherwise return the standard name
        if obj.standard.id == 7:
            return 'Balvatika'
        return obj.standard.name
#  all in above of receips or receipt details for api

class ReceiptFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = fee_type
        fields = '__all__'

class ReceiptStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['grno','first_name', 'last_name', 'middle_name']


class ReceiptReceiptSerializer(serializers.ModelSerializer):
    student = ReceiptStudentsSerializer(read_only=True)    
    
    class Meta:
        model = Receipt
        fields = '__all__'



class ReceiptDetailsFeesSerializer(serializers.ModelSerializer):
    receipt = ReceiptReceiptSerializer(read_only=True)
    fee_type = FeeTypeGetSerializer(read_only=True)
    class Meta:
        model = ReceiptDetail
        fields = '__all__'



class StudentFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'

class FeeTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = fee_type_master
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']