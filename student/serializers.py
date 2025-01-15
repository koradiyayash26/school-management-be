from .models import Students,StudentsUpdatesHistory,UpdateStudent,StudentsStdMultiList,ExamMarksTemplateAdd,ExamMarkAssingData,StudentUpdateStdAcademicHistory
from rest_framework import serializers


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        # fields = ['id', 'grno', 'last_name', 'first_name', 'middle_name', 'address', 'standard', 'section']
        fields = '__all__'

class ExamSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
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
    roll_no = serializers.SerializerMethodField()

    class Meta:
        model = ExamMarkAssingData
        fields = '__all__'

    def get_first_name(self, obj):
        return obj.student.first_name if obj.student else None

    def get_middle_name(self, obj):
        return obj.student.middle_name if obj.student else None

    def get_last_name(self, obj):
        return obj.student.last_name if obj.student else None
    
    def get_roll_no(self, obj):
        return obj.student.roll_no if obj.student else None
    

class StudentUpdateHistorySerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    academic_year = serializers.CharField(source='academic_year.year')
    standard = serializers.CharField(source='standard.name')

    class Meta:
        model = StudentUpdateStdAcademicHistory
        fields = ['id', 'student_name', 'academic_year','section', 'standard', 'note', 'update_date']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"    