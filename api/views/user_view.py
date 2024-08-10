from api.serializers.user_serializer import UserSerializer
from authentication.models import User
from rest_framework import generics
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer