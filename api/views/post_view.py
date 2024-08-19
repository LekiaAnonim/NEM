from api.serializers.all_serializer import PostSerializer, CommentSerializer
from api.models.comment_model import Like, Comment
from rest_framework import generics
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404, 
    ListAPIView,
)
from api.models.company_model import Company
from api.models.post_model import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company', 'date_created']
    search_fields = (
        '^body',
    )
    ordering_fields = (
        'date_created',
    )

    def perform_create(self, serializer):
        company = Company.objects.get(pk=self.request.data['company']) if 'company' in self.request.data else None
        serializer.save(user=self.request.user, company=company)

    
    @action(detail=True, methods=['post'], url_path='like')
    def like_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        company = request.data.get('company_id')
        like, created = Like.objects.get_or_create(post=post, user=user if user.is_authenticated else None, company_id=company if company else None)
        if not created:
            return Response({"detail": "Already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        company = request.data.get('company_id')
        like = Like.objects.filter(post=post, user=user if user.is_authenticated else None, company_id=company if company else None).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='comment')
    def comment_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        company_id = request.data.get('company_id')
        body = request.data.get('body')

        if not body:
            return Response({"detail": "Content is required to comment."}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(post=post, user=user if user.is_authenticated else None, company_id=company_id if company_id else None, body=body)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
