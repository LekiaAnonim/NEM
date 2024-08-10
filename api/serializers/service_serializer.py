from rest_framework import serializers
from api.models.service_model import Service, ServiceCategory, ServiceImage

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['name',]

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['caption', 'image', 'service']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['title', 'sub_title', 'category', 'description', 'date_created', 
                  'date_updated', 'featured', 'company']