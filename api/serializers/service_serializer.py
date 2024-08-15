from rest_framework import serializers
from api.models.service_model import Service, ServiceCategory, ServiceImage
from api.models.company_model import Company

class ServiceCategorySerializer(serializers.HyperlinkedModelSerializer):
    services = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:service-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:servicecategory-detail')
    class Meta:
        model = ServiceCategory
        fields = ['url',  'name', 'services']

class ServiceImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:serviceimage-detail')
    service = serializers.SlugRelatedField(queryset=Service.objects.all(), slug_field='title')
    class Meta:
        model = ServiceImage
        fields = ['url', 'caption', 'image', 'service']

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(queryset=ServiceCategory.objects.all(), slug_field='name')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='company_name')
    class Meta:
        model = Service
        fields = ['title', 'sub_title', 'category', 'description', 'date_created', 
                  'date_updated', 'featured', 'company']