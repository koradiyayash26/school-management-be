from django.urls import path, include

from . import views,consumers
from django.urls import re_path
from school import views

schoolStudent_urlpatterns = [
    path('search/', views.SchoolStudentGet.as_view(), name='school_student_list'),
    path('<int:pk>/search/', views.SchoolStudentByIdGet.as_view(), name='school_student_list'),
    path('name/', views.SchoolStudentNamesGet.as_view(), name='school_student_name_list'),
    path('add/', views.SchoolStudentPost.as_view(), name='school_student_post'),
    path('<int:pk>/edit/', views.SchoolStudentPatch.as_view(), name='school_student_patch'),
    # path('<int:pk>/delete/', views.PaymentFeeDelete.as_view(), name='payment_fee_delete'),
]

chats_urlpatterns = [
    path('api/chats/', views.ChatListView.as_view(), name='chat-list'),
    path('api/chats/<int:user_id>/', views.ChatMessageView.as_view(), name='chat-messages'),
    path('api/chats/<int:user_id>/read/', views.MarkChatAsReadView.as_view(), name='mark-chat-read'),
    path('api/messages/<int:message_id>/delivered/', views.MessageStatusView.as_view(), name='mark-message-delivered'),
    path('api/messages/<int:message_id>/read/', views.MessageStatusView.as_view(), name='mark-message-read'),
    path('api/messages/<int:message_id>/', views.MessageActionView.as_view(), name='message-actions'),
    path('api/messages/bulk-delete/', views.BulkMessageDeleteView.as_view(), name='bulk-message-delete'),
    path('api/chats/<int:user_id>/clear/', views.ClearChatView.as_view(), name='clear-chat'),
    # path('api/users/<int:user_id>/block/', views.BlockUserView.as_view(), name='block-user'),
    # path('api/chats/<int:user_id>/mute/', views.MuteNotificationsView.as_view(), name='mute-notifications'),
    # path('api/chats/<int:user_id>/disappearing-messages/', views.DisappearingMessagesView.as_view(), name='disappearing-messages'),

]

# for websockter for chats
websocket_urlpatterns = [
    path('chat/', consumers.ChatConsumer.as_asgi()),
]

urlpatterns = [    
    path('report/standard/<str:standard>/', views.FeeReportDetailAPIViewDemo.as_view(), name="report"),
    path('report/fee-report-excel/<int:standard>/', views.FeeReportExcelView.as_view(), name='fee-report-excel'),
    path('report/fee-type-report-excel/<str:standard>/<int:fee_master_id>/', views.FeeTypeReportExcelViewSingle.as_view(), name='fee-type-report-excel'),
    path('school-student/', include(schoolStudent_urlpatterns)),
    path('chats/', include(chats_urlpatterns)),
    path('ws/', include(websocket_urlpatterns)),  # Add this line
]
