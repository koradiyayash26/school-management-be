from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers,generics
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone  # Add this import
from django.contrib.auth import authenticate



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            return Response({
                'username': 'Please enter a valid username'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Try to authenticate with provided credentials
        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                'password': 'Wrong password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Authentication successful, proceed with token generation
        user.last_login = timezone.now()
        user.save()
        jwt_token = get_tokens_for_user(user)
        
        return Response({
            'user_id': user.pk,
            'email': user.email,
            'jwt_token': jwt_token,
        })

# api token verify api
class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'permissions', 'is_staff', 'is_superuser']

    def get_permissions(self, obj):
        return list(obj.get_all_permissions())

class AuthTokenVerify(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        try:
            user_data = UserSerializer(request.user).data
            groups = list(request.user.groups.values_list('name', flat=True))
            
            role = "user"
            if user_data['is_superuser']:
                role = "admin"
            elif user_data['is_staff']:
                role = "staff"
            
        except Exception as e:
            raise AuthenticationFailed("Invalid token or user not found")
        
        return JsonResponse({
            "message": "Token verification successful",
            "user": user_data,
            "groups": groups,
            "role": role
        }, status=200)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username']

# class AuthTokenVerify(APIView):
#     authentication_classes = [JWTAuthentication]
#     def get(self, request):
#         try:
#             user_data = UserSerializer(request.user).data
#             # that group of  user aasing that list return
#             groups = list(request.user.groups.values_list('name', flat=True))
#         except Exception as e:
#             raise AuthenticationFailed("Invalid token or user not found")
#         return JsonResponse({"message": "Token verification successful", "user": user_data,"groups":groups}, status=200)




class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.check_password(request.data.get("current_password")):
            return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(request.data.get("new_password"))
        user.save()
        return Response({"detail": "Password updated successfully"})
    
    
class ChangeUsernameEmailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        user = request.user
        new_username = request.data.get("new_username")
        new_email = request.data.get("new_email")

        # Check if at least one field is provided
        if not new_username and not new_email:
            return Response({
                "error": "Please provide either new username or new email or both."
            }, status=status.HTTP_400_BAD_REQUEST)

        updated_fields = []

        if new_username:
            # Check if username already exists
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                return Response({
                    "error": "Username already taken. Please choose a different username."
                }, status=status.HTTP_400_BAD_REQUEST)
            user.username = new_username
            updated_fields.append("username")

        if new_email:
            # Validate email
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                return Response({
                    "error": "Email already registered. Please use a different email."
                }, status=status.HTTP_400_BAD_REQUEST)
            user.email = new_email
            updated_fields.append("email")

        user.save()
        return Response({
            "detail": f"Successfully updated {' and '.join(updated_fields)}",
            "username": user.username,
            "email": user.email
        })
        
        
class GetUserProfileUsername(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get(self, request):
        # Since we're using JWT, we can directly get the username from the authenticated user
        if not request.user.is_authenticated:
            raise AuthenticationFailed("Invalid token")

        return JsonResponse({
            "message": "Token verification successful", 
            "username": request.user.username,
            "email": request.user.email
        }, status=200)
    
    