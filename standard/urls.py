from django.urls import path, include

from standard import views

standards_urlpatterns = [
    path('<str:pk>/search/', views.StandardsGetData.as_view(), name='standards-data'),
    path('standard-counter/', views.StandardsNo.as_view(), name='standard-no'),
    path('standard-master/', views.StandardMasterListCreateView.as_view(), name='standard-master-list'),
    path('standard-master/<int:pk>/', views.StandardMasterRetrieveUpdateView.as_view(), name='standard-master-detail'),
]


urlpatterns = [
    path('standard-count/', views.CountStudents.as_view(), name="CountStudents"),
    path('standards/', include(standards_urlpatterns)),
]
