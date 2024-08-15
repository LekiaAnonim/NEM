from api.serializers.company_serializer import CompanySerializer, CompanyCategorySerializer, CompanySizeSerializer
from api.models.company_model import Company, CompanyCategory, CompanySize
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['organization_type', 'company_size', 'country', 'date_created']
    search_fields = (
        '^company_name',
    )
    ordering_fields = (
        'company_name',
        'date_created'
    )

    def perform_create(self, serializer):
        serializer.save(profile = self.request.user)


class CompanyCategoryViewSet(viewsets.ModelViewSet):
    queryset = CompanyCategory.objects.all()
    serializer_class = CompanyCategorySerializer


class CompanySizeViewSet(viewsets.ModelViewSet):
    queryset = CompanySize.objects.all()
    serializer_class = CompanySizeSerializer
