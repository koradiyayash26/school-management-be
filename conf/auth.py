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

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        jwt_token = get_tokens_for_user(user)
        return Response({
            'user_id': user.pk,
            'email': user.email,
            'jwt_token': jwt_token,
        })

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class AuthTokenVerify(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            user_data = UserSerializer(request.user).data
            # that group of  user aasing that list return
            groups = list(request.user.groups.values_list('name', flat=True))
        except Exception as e:
            raise AuthenticationFailed("Invalid token or user not found")
        return JsonResponse({"message": "Token verification successful", "user": user_data,"groups":groups}, status=200)
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
    
class ChangeUsernameView(generics.UpdateAPIView):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        user = request.user
        user.username = request.data.get("new_username")
        user.save()
        return Response({"detail": "Username updated successfully"})

class GetUserProfileUsername(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        token_key = request.query_params.get('token')
        if not token_key:
            return JsonResponse({"detail": "Token not provided."}, status=400)

        try:
            token = Token.objects.get(key=token_key)
            username = token.user.username
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        return JsonResponse({"message": "Token verification successful", "username": username}, status=200)
    
    