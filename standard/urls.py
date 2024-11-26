from django.urls import path, include

from standard import views

standards_urlpatterns = [
    path('<str:pk>/search/', views.StandardsGetData.as_view(), name='standards-data'),
    path('standard-counter/', views.StandardsNo.as_view(), name='standard-no'),
    path('standard-master/', views.StandardMasterListCreateView.as_view(), name='standard-master-list'),
    path('standard-master/<int:pk>/', views.StandardMasterRetrieveUpdateView.as_view(), name='standard-master-detail'),
]


academic_year_urlpatterns = [
    path('create-list/', views.AcademicYearListCreateView.as_view(), name='academic-year-list'),
    path('update-delete/<int:pk>/', views.AcademicYearRetrieveUpdateView.as_view(), name='academic-year-detail'),
]

urlpatterns = [
    path('standard-count/', views.CountStudents.as_view(), name="CountStudents"),
    path('caste-report/', views.CasteReportAPI.as_view(), name="caste-report"),
    path('standards/', include(standards_urlpatterns)),
    path('academic-year/', include(academic_year_urlpatterns)),
]
