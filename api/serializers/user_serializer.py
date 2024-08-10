from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'date_of_birth', 'bio', 'role', 'company', 'verified', 'country', 'city', 'phone_number', 'region', 'address', 'avatar']