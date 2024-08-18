from api.serializers.product_serializer import ProductSerializer, ProductCategorySerializer, ProductImageSerializer
from api.models.product_model import Product, ProductCategory, ProductImage
from api.models.company_model import Company
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
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

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product',]