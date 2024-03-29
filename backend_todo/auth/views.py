from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer
from auth import models


@api_view(['POST',])
def logout_view(request):

  if request.method == 'POST':
    request.user.auth_token.delete()

    data = {
      "message": "Logout successfully!"
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET',])
def getToken_view(request, auth_token):

  if request.method == 'GET':
    user = Token.objects.get(key=auth_token).user
    token = Token.objects.get(user=user).key

    data = {
      "id": user.id,
      "username": user.username,
      "email": user.email,
      "auth_token":  token
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST',])
def registration_view(request):

  if request.method == 'POST':
    serializer = RegistrationSerializer(data=request.data)
    
    data = {}
    httpStatus = ''
    
    if serializer.is_valid():
      account = serializer.save()

      data['response'] = "Registration Successful!"
      data['username'] = account.username
      data['email'] = account.email

      token = Token.objects.get(user=account).key
      data['token'] = token

      httpStatus = status.HTTP_201_CREATED
      # refresh = RefreshToken.for_user(account)
      # data['token'] = {
      #  'refresh': str(refresh),
      #   'access': str(refresh.access_token),
      #}
        
    else:
      data = serializer.errors
      httpStatus = status.HTTP_400_BAD_REQUEST
    
    return Response(data, status=httpStatus)
    
class CustomAuthToken(ObtainAuthToken):

  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)

    response = Response({
        'token': token.key,
        'user_id': user.pk,
        'email': user.email
    })

    # This is how to set cookie, check the offical docs for more info
    # response.set_cookie(key='token', value=token, samesite='none', secure=True)
  
    return response
