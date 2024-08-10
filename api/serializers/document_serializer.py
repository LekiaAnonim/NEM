from api.models.document_model import Document
from rest_framework import serializers

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'type', 'document', 'company']