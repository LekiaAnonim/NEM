from api.serializers.all_serializer import ServiceSerializer, ServiceCategorySerializer, ServiceImageSerializer
from api.models.service_model import Service, ServiceCategory, ServiceImage
from api.models.company_model import Company
from rest_framework import generics
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models.comment_model import Like

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

    @action(detail=True, methods=['post'], url_path='like')
    def like_service(self, request, pk=None):
        service = self.get_object()
        user = request.user
        company = request.data.get('company_id')
        like, created = Like.objects.get_or_create(service=service, user=user if user.is_authenticated else None, company_id=company if company else None)
        if not created:
            return Response({"detail": "Already liked this service."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Service liked."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike_service(self, request, pk=None):
        service = self.get_object()
        user = request.user
        company = request.data.get('company_id')
        like = Like.objects.filter(service=service, user=user if user.is_authenticated else None, company_id=company if company else None).first()
        if not like:
            return Response({"detail": "You have not liked this service."}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({"detail": "Service unliked."}, status=status.HTTP_204_NO_CONTENT)



class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceImageViewSet(viewsets.ModelViewSet):
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service',]