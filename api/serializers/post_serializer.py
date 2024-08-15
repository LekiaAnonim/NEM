from api.models.post_model import Post
from rest_framework import serializers
from api.serializers.company_serializer import CompanySerializer

class PostSerializer(serializers.HyperlinkedModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Post
        fields = ['body', 'company']