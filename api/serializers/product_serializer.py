from rest_framework import serializers
from api.models.product_model import Product, ProductCategory, ProductImage

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name',]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['caption', 'image', 'product']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'sub_title', 'category', 'description', 'date_created', 
                  'date_updated', 'featured', 'company']