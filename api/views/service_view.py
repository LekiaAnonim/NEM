from api.serializers.service_serializer import ServiceSerializer, ServiceCategorySerializer, ServiceImageSerializer
from api.models.service_model import Service, ServiceCategory, ServiceImage
from api.models.company_model import Company
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'company', 'featured', 'date_created']
    search_fields = (
        '^title',
        '^sub_title',
    )
    ordering_fields = (
        'title',
        'date_created'
    )

    def perform_create(self, serializer):
        company = Company.objects.get(pk=self.request.data['company'])
        serializer.save(company=company)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceImageViewSet(viewsets.ModelViewSet):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service',]