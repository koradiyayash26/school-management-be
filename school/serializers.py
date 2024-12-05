from rest_framework import serializers
from student.models import SchoolStudent,Students

from .models import ChatMessage
from django.contrib.auth import get_user_model

class ReportsSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    student__first_name = serializers.CharField()
    student__last_name = serializers.CharField()
    student__middle_name = serializers.CharField()
    student__standard = serializers.CharField()
    student__grno = serializers.CharField()
    student__city = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    waived = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)


class SchoolStudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ["id",'grno','first_name', 'last_name', 'middle_name']


class SchoolStudentSerializer(serializers.ModelSerializer):
    student = SchoolStudentDetailSerializer(read_only=True)
    class Meta:
        model = SchoolStudent
        fields = '__all__'

# for post api of school student

class SchoolStudentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolStudent
        fields = '__all__'


# for chats webscokte

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_login', 'is_active']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp','is_edited', 'is_read','deleted_by_sender','deleted_by_receiver']