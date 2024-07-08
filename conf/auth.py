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


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        jwt_token = get_tokens_for_user(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'jwt_token':jwt_token
        })
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        # fields = ['id', 'username', 'email']

class AuthTokenVerify(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return JsonResponse({"detail": "Token not provided."}, status=400)

        try:
            verify = Token.objects.get(key=token)
            user_data = UserSerializer(verify.user).data
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")
        
        return JsonResponse({"message": "Token verification successful", "user": user_data}, status=200)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        user = request.user
        user.username = request.data.get("new_username")
        user.save()
        return Response({"detail": "Username updated successfully"})

class GetUserProfileUsername(APIView):
    authentication_classes = [TokenAuthentication]
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
    
    