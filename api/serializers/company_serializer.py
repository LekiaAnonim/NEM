from rest_framework import serializers
from api.models.company_model import Company, CompanyCategory, CompanySize


class CompanyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCategory
        fields = ['name',]


class CompanySizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySize
        fields = ['size',]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['profile', 'company_name', 'organization_type', 'about', 'tag_line', 
                  'company_size', 'logo', 'banner', 'email', 'office_address', 'country', 
                  'state', 'city', 'website', 'verify']