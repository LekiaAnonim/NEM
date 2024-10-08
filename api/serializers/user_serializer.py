from rest_framework import serializers
from authentication.models import User, Gender

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # user_profile = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:company-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:user-detail')
    gender = serializers.SlugRelatedField(queryset=Gender.objects.all(), slug_field='type')
    companies = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:company-detail')
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ['url', 'id', 'first_name', 'last_name', 'email', 'gender', 'date_of_birth', 
                  'bio', 'role', 'company', 'verified', 'country', 'city', 'phone_number', 
                  'region', 'address', 'avatar',"followers_count",
            "following_count", 'companies']

class GenderSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:gender-detail')
    
    class Meta:
        model = Gender
        fields = ['url', 'pk', 'type',]