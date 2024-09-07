from django.urls import path, include
from student import views

educational_urlpatterns = [
    path('search/', views.StudentUpdateHistoricalGet.as_view(), name='student_update_historical_get'),    
    path('<int:pk>/delete/', views.StudentUpdateHistoricalDelete.as_view(), name='student_update_historical_delete'),    
]

student_urlpatterns = [
    path('add/', views.StudentAdd.as_view(), name='student_add'),
    path('search/', views.StudentGet.as_view(), name='get_student'),
    path('<int:pk>/search/', views.StudentGetId.as_view(), name='search_student'),
    path('<int:pk>/edit/', views.StudentUpdate.as_view(), name='edit_student'),    
    path('<int:pk>/delete/', views.StudentDelete.as_view(), name='delete_student'),
]

exam_urlpatterns = [
    path('search/', views.ExamMarksGet.as_view(), name='get_exammarks'),
    path('add/', views.ExamMarksAdd.as_view(), name='add_exammarks'),   
    path('uploadfile/add/', views.ExamMarksUploadFileAdd.as_view(), name='get_id_exammarks'),   
    path('<int:pk>/search/', views.ExamMarksGetId.as_view(), name='search_exammarks'),   
    path('<int:pk>/edit/', views.ExamMarksUpdate.as_view(), name='update_exammarks'),   
    path('<int:pk>/delete/', views.ExamMarksDelete.as_view(), name='delete_exammarks'),   
]

# student update std and year api 
student_update_urlpatterns = [
    path('search/', views.StudentUpdateStdYearGet.as_view(), name='student_update_std_year_get'),    
    path('add/', views.StudentUpdateStdYearPost.as_view(), name='student_update_std_year_post'),    
    path('seleted/', views.StudentsSelectedPost.as_view(), name='student_update_seleted'),    
    path('unseleted/', views.StudentsUnselectedPost.as_view(), name='student_update_unseleted'),    
    path('students/<int:year>/<int:standard>/', views.StudentSletedOrNotSeletedGet.as_view(), name='student_seletedAndUnseleted_get'),    
    path('add-multilist/', views.StudentsAddYearAndstdFromurl.as_view(), name='student_update_add_updatemultilist_get'),    
]

exam_teamplate_urlpatterns = [
    path('search/', views.ExamMarksTemplateAddGet.as_view(), name='exam_template_list_get'),
    path('add/', views.ExamMarksTemplateAddAPI.as_view(), name='exam_template_post'),
    path('<int:pk>/search/', views.ExamMarksTemplateGetId.as_view(), name='exam_template_get_id'),    
    path('<int:pk>/edit/', views.ExamMarksTemplateAddUpdate.as_view(), name='exam_template_update'),    
    path('<int:pk>/delete/', views.ExamMarksTemplateDelete.as_view(), name='exam_template_delete'),    
    path('exam-marks-assign/<int:standard>/<int:pk>/', views.ExamMarksAssignAPIView.as_view(), name='exam_marks_assign'),
    path('exam-marks-view/<int:standard>/<int:pk>/', views.ExamMarksViewAPIView.as_view(), name='exam_marks_view'),
    path('update-mark/', views.ExamAssingUpdateMarkAPIView.as_view(), name='update-mark'),
]

urlpatterns = [
    path('exams/', include(exam_urlpatterns)),    
    path('exam-template/', include(exam_teamplate_urlpatterns)),    
    path('students/', include(student_urlpatterns)),   
    path('educationals/', include(educational_urlpatterns)),   
    path('student-update/', include(student_update_urlpatterns)),
    
    # admin api for user and group
    
    path('api/user/create/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('api/user/change-password/<int:user_id>/', views.ChangePasswordAPIView.as_view(), name='change-password'),
    path('api/user/detail/<int:user_id>/', views.UserDetailAPIView.as_view(), name='user-detail'),
    path('api/users/', views.UserListAPIView.as_view(), name='user-list'),
    path('api/user/delete/<int:user_id>/', views.UserDeleteAPIView.as_view(), name='user-delete'),
    
    path('api/user/<int:user_id>/groups/', views.GroupListAPIView.as_view(), name='user-groups'),
    path('api/user/<int:user_id>/assign-groups/', views.AssignGroupsToUserAPIView.as_view(), name='assign-groups'),
]
