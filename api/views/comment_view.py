from rest_framework import viewsets, status
from api.serializers.all_serializer import CommentSerializer
from api.models.comment_model import Comment
from api.models.post_model import Post
from api.models.company_model import Company
from rest_framework.generics import (
    get_object_or_404, 
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        user = self.request.user if 'user' in self.request.data else None
        company = Company.objects.get(pk=self.request.data['company']) if 'company' in self.request.data else None
        serializer.save(user=user, company=company)