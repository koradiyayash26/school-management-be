from django.contrib import admin
from .models import Students,SchoolStudent,UpdateStudent,StudentsUpdatesHistory,StudentsStdMultiList,ExamMarksTemplateAdd,ExamMarkAssingData

# Register your models here.

admin.site.register(Students)
admin.site.register(SchoolStudent)
admin.site.register(UpdateStudent)
admin.site.register(StudentsStdMultiList)
admin.site.register(StudentsUpdatesHistory)
admin.site.register(ExamMarksTemplateAdd)
admin.site.register(ExamMarkAssingData)
