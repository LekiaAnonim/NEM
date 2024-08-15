from api.models.document_model import Document, DocumentType
from rest_framework import serializers
# from api.serializers.company_serializer import CompanySerializer

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.SlugRelatedField(queryset=DocumentType.objects.all(), slug_field='name')
    
    class Meta:
        model = Document
        fields = ['id', 'type', 'document', 'company']

class DocumentTypeSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:documenttype-detail')
    class Meta:
        model = DocumentType
        fields = ['name', 'type']