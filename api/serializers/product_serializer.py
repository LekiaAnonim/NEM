from rest_framework import serializers
from api.models.product_model import Product, ProductCategory, ProductImage
# from api.serializers.company_serializer import CompanySerializer
from api.models.company_model import Company
from api.serializers.comment_serializer import LikeSerializer
class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:product-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:productcategory-detail')
    class Meta:
        model = ProductCategory
        fields = ['url', 'pk', 'name', 'products']

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:productimage-detail')
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='title')
    class Meta:
        model = ProductImage
        fields = ['url', 'caption', 'image', 'product']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(queryset=ProductCategory.objects.all(), slug_field='name')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='company_name')
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['title', 'sub_title', 'category', 'description', 'date_created', 
                  'date_updated', 'featured', 'company', 'images']
        
    def get_likes(self, obj):
        likes = obj.likes.all()
        return LikeSerializer(likes, many=True).data