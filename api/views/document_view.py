from api.serializers.all_serializer  import DocumentSerializer, DocumentTypeSerializer
from api.models.document_model import Document, DocumentType
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company',]
    ordering_fields = (
        'date_created'
    )


class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name',]

    