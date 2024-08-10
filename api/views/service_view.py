from api.serializers.service_serializer import ServiceSerializer, ServiceCategorySerializer, ServiceImageSerializer
from api.models.service_model import Service, ServiceCategory, ServiceImage
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'company', 'featured', 'date_created']


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceImageViewSet(viewsets.ModelViewSet):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product',]