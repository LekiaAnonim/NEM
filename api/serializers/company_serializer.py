from rest_framework import serializers
from api.models.company_model import Company, CompanyCategory, CompanySize
from authentication.models import User
from api.serializers.document_serializer import DocumentSerializer
from api.serializers.product_serializer import ProductSerializer
from api.serializers.service_serializer import ServiceSerializer

class CompanySizeSerializer(serializers.HyperlinkedModelSerializer):
    companies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:company-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:companysize-detail')
    class Meta:
        model = CompanySize
        fields = ['url', 'pk', 'size', 'companies']
class CompanyCategorySerializer(serializers.HyperlinkedModelSerializer):
    companies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:company-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:companycategory-detail')
    class Meta:
        model = CompanyCategory
        fields = ['url', 'pk', 'name', 'companies']




class CompanySerializer(serializers.HyperlinkedModelSerializer):
    organization_type = serializers.SlugRelatedField(queryset=CompanyCategory.objects.all(), slug_field='name')
    company_size = serializers.SlugRelatedField(queryset=CompanySize.objects.all(), slug_field='size')
    profile = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')
    documents = DocumentSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    profile = serializers.ReadOnlyField(source='profile.email')
    url = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:company-detail')
    class Meta:
        model = Company
        fields = ['url', 'profile', 'company_name', 'organization_type', 'about', 'tag_line', 
                  'company_size', 'logo', 'banner', 'email', 'office_address', 'country', 
                  'state', 'city', 'website', 'verify', 'documents', 'products', 'services']