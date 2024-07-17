from .models import Students,ExamMarks,StudentsUpdatesHistory,UpdateStudent,StudentsStdMultiList,ExamMarksTemplateAdd,ExamMarkAssingData
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



class ExamMarksTemplateAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamMarksTemplateAdd
        fields = '__all__'
        
class ExamMarksAssignSerializer(serializers.Serializer):
    marks = serializers.DictField(child=serializers.IntegerField())        
    
class ExamMarkAssingDataSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    middle_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = ExamMarkAssingData
        fields = '__all__'

    def get_first_name(self, obj):
        return obj.student.first_name if obj.student else None

    def get_middle_name(self, obj):
        return obj.student.middle_name if obj.student else None

    def get_last_name(self, obj):
        return obj.student.last_name if obj.student else None