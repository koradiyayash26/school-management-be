from django.urls import path, include
from . import views

from school import views

schoolStudent_urlpatterns = [
    path('search/', views.SchoolStudentGet.as_view(), name='school_student_list'),
    path('<int:pk>/search/', views.SchoolStudentByIdGet.as_view(), name='school_student_list'),
    path('name/', views.SchoolStudentNamesGet.as_view(), name='school_student_name_list'),
    path('add/', views.SchoolStudentPost.as_view(), name='school_student_post'),
    path('<int:pk>/edit/', views.SchoolStudentPatch.as_view(), name='school_student_patch'),
    # path('<int:pk>/delete/', views.PaymentFeeDelete.as_view(), name='payment_fee_delete'),
]

urlpatterns = [    
    path('report/standard/<str:standard>/', views.FeeReportDetailAPIViewDemo.as_view(), name="report"),
    path('report/fee-report-excel/<int:standard>/', views.FeeReportExcelView.as_view(), name='fee-report-excel'),
    path('report/fee-type-report-excel/<str:standard>/<int:fee_master_id>/', views.FeeTypeReportExcelViewSingle.as_view(), name='fee-type-report-excel'),
    path('school-student/', include(schoolStudent_urlpatterns)),
]
