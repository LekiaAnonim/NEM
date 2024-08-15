from api.serializers.user_serializer import UserSerializer, GenderSerializer
from authentication.models import User, Gender
from rest_framework import generics
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer