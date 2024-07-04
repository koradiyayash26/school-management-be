from .models import Students,ExamMarks,StudentsUpdatesHistory,UpdateStudent,StudentsStdMultiList
from rest_framework import serializers


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        # fields = ['id', 'grno', 'last_name', 'first_name', 'middle_name', 'address', 'standard', 'section']
        fields = '__all__'



class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamMarks
        fields = ['id','student', 'std', 'sub', 'marks', 'total_marks', 'date']

class ExamSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'

class ExamGetSerializer(serializers.ModelSerializer):
    student = ExamSerializer2()
    class Meta:
        model = ExamMarks
        fields = ['id','student', 'std', 'sub', 'marks', 'total_marks', 'date']



class ExamPatchSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Students.objects.all())

    class Meta:
        model = ExamMarks
        fields = ['id','student', 'std', 'sub', 'marks', 'total_marks', 'date']


# student update historical 

class StudentUpdateHistoricalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsUpdatesHistory
        fields = '__all__'


# student update templet year and standard 

class StudentUpdateStdYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateStudent
        fields = '__all__'



#  for student-update year and std to get by year and std get api 

class StudentUpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsStdMultiList
        fields = '__all__'
        
        # fields = ['id','grno','first_name','last_name','standard','year']
