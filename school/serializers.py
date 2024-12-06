from rest_framework import serializers
from student.models import SchoolStudent,Students

from .models import ChatMessage
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone

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
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp', 
                 'is_edited', 'is_read', 'deleted_by_sender', 
                 'deleted_by_receiver', 'formatted_date']

    def get_formatted_date(self, obj):
        """
        Returns a formatted date string based on the message timestamp:
        - "Today" for today's messages
        - "Yesterday" for yesterday's messages
        - "dd-mm-yyyy" for older messages
        """
        now = timezone.now()
        message_date = obj.timestamp.astimezone(now.tzinfo)
        
        # Strip time to compare just the dates
        today = now.date()
        msg_date = message_date.date()
        yesterday = today - timedelta(days=1)
        
        if msg_date == today:
            return 'Today'
        elif msg_date == yesterday:
            return 'Yesterday'
        else:
            return message_date.strftime('%d-%m-%Y')