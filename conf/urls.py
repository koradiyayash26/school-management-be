"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .auth import AuthTokenVerify,ChangePasswordView,ChangeUsernameEmailView,GetUserProfileUsername,CustomAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from school.views import HomePageView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school.urls')),
    path('', include('standard.urls')),
    path('', include('student.urls')),
    path('', include('payment.urls')),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    
    path('', HomePageView.as_view(), name='home'),
    
    
   path('api-auth/', include('rest_framework.urls')),
   path('api-token-verify/', AuthTokenVerify.as_view(), name='api-token-verify'),
   path('api-auth/change-password/',ChangePasswordView.as_view(), name='change_password'),
   path('api-auth/change-username/',ChangeUsernameEmailView.as_view(), name='change_username'),
   path('api-auth/user-profile-username/',GetUserProfileUsername.as_view(), name='get_userprofile_username'),
   
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
]
