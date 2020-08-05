from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from .models import Client, Project, MyUser
from .serializers import ClientSerializer, ProjectSerializer, MyUserSerializer


import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    serializer_class = MyUserSerializer

    def get_queryset(self):
        return MyUser.objects.all()

    @action(detail=False, methods=["POST"], permission_classes=[~IsAuthenticated])
    def login_with_password(self,request):
        try:
            username = request.data.get('username')
            if not username:
                return Response({'detail': 'Please provide username.'}, status=status.HTTP_400_BAD_REQUEST)
            password = request.data.get('password')
            if not password:
                return Response({'detail': 'Please provide password.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    user = MyUser.objects.get(username=username, is_active=True)
                except MyUser.DoesNotExist:
                    return Response({'detail':'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                if not user or not user.password:
                    return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
                logger.info(password + ' - ' + user.password)
                if not check_password(password, user.password):
                    return Response({'detail': 'Unauthorised'}, status=401)

                serializer = MyUserSerializer(user)
                # token = Token.objects.filter(user=user).first()
                # if not token:
                #     Token.objects.create(user=user)
                #     print(token.key)
                #     token=Token.objects.filter(user=user).first()

                response_data = serializer.data
                # response_data['token']= token.key
                login(request, user)
            return Response(response_data)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            if request.user:
                print('Logging out ' + request.user.username)
                logout(request)
                return Response({'detail': 'Logged out.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'Error': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
