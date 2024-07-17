from django.contrib import admin
from .models import Students,ExamMarks,EducationalYear,SchoolStudent,UpdateStudent,StudentsUpdateList,StudentsUpdatesHistory,StudentsStdMultiList,ExamMarksTemplateAdd,ExamMarkAssingData

# Register your models here.

admin.site.register(Students)
admin.site.register(ExamMarks)
admin.site.register(EducationalYear)
admin.site.register(SchoolStudent)
admin.site.register(UpdateStudent)
admin.site.register(StudentsUpdateList)
admin.site.register(StudentsStdMultiList)
admin.site.register(StudentsUpdatesHistory)
admin.site.register(ExamMarksTemplateAdd)
admin.site.register(ExamMarkAssingData)
