from django.urls import include, path
from django.contrib.auth.decorators import login_required
from payment import views

feetypes_urlpatterns = [
    path('add/', views.FeeTypesPost.as_view(), name='fee_types_add'),
    path('search/', views.FeeTypeGet.as_view(), name='fee_types_get'),
    path('<int:pk>/search/', views.FeeTypeIdGetData.as_view(), name='fee_types_id_get'),
    path('<int:pk>/edit/', views.FeeTypePatch.as_view(), name='fee_types_edit'),
    path('<int:pk>/delete/', views.FeeTypeDelete.as_view(), name='fee_types_delete'),
    path('add-search/', views.FeeTypeGetAddDetails.as_view(), name='fee_types_get_add_details'),
    path('<int:pk>/<int:standard>/<int:year>/student-assign/', views.StudentAssignFeeApiGet.as_view(), name='fee_types_get_student_assing'),
]

apioldfees_urlpatterns = [
    path('search/', views.HistoricalDataGetApi.as_view(), name='historical_fees_get'),
    path('add/', views.HistoricalDataPostApi.as_view(), name='historical_fees_add'),
    path('<int:pk>/delete/', views.HistoricalDataDeleteApi.as_view(), name='historical_fees_delete'),
]

payments_urlpatterns = [
    path('search/', views.PaymentFeeListGet.as_view(), name='payment_list'),
    path('<int:pk>/receipt/details/', views.PaymentReceiptDetails.as_view(), name='payment_id_get_details_list'),
    path('<int:pk>/search/', views.PaymentFeeListIdToGet.as_view(), name='payment_id_get_list'),
    path('<int:pk>/delete/', views.PaymentFeeDelete.as_view(), name='payment_fee_delete'),
    path('<int:pk>/<int:year>/', views.PaymentStudentFeeGet.as_view(), name='payment_student_fee_get'),
    path('payment-collect/', views.PaymentStudentFeePatch.as_view(), name='payment_student_fee_patch'),
]

urlpatterns = [
    path('fee-types/', include(feetypes_urlpatterns)),
    path('fee-type-master/<int:pk>/', views.FeeTypeMasterRetrieveUpdateView.as_view(), name='fee-type-master-detail'),
    path('fee-type-master/', views.FeeTypeMasterViewSet.as_view(), name='fee-type-master'),
    path('update-student-fee-types/', views.StudentAssignUnAssign.as_view(), name='student_assign_unassign'),
    # for api 
    path('fee-report/', views.FeeTotalCount.as_view(), name='fee_report'),
    path('historical-fees/', include(apioldfees_urlpatterns)),
    path('payments/', include(payments_urlpatterns)),
]
