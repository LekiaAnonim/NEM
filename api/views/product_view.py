from api.serializers.all_serializer import ProductSerializer, ProductCategorySerializer, ProductImageSerializer
from api.models.product_model import Product, ProductCategory, ProductImage
from api.models.company_model import Company
from rest_framework import generics
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models.comment_model import Like
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

    @action(detail=True, methods=['post'], url_path='like')
    def like_product(self, request, pk=None):
        product = self.get_object()
        user = request.user
        company = request.data.get('company_id')
        like, created = Like.objects.get_or_create(product=product, user=user if user.is_authenticated else None, company_id=company if company else None)
        if not created:
            return Response({"detail": "Already liked this product."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Product liked."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike_product(self, request, pk=None):
        product = self.get_object()
        user = request.user
        company = request.data.get('company_id')
        like = Like.objects.filter(product=product, user=user if user.is_authenticated else None, company_id=company if company else None).first()
        if not like:
            return Response({"detail": "You have not liked this product."}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({"detail": "Product unliked."}, status=status.HTTP_204_NO_CONTENT)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product',]