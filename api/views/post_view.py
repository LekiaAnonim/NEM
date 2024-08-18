from api.serializers.post_serializer import PostSerializer, PostListSerializer
from api.models.post_model import Post
from api.models.comment_model import Like
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

    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
    )
    def user_like(self, request, pk=None):
        """Endpoint to like a post"""
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if Like.objects.filter(user=user, post=post).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_409_CONFLICT,
            )
        Like.objects.create(user=user, post=post)
        if Like.objects.filter(company=user.companies, post=post).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_409_CONFLICT,
            )
        Like.objects.create(company=user.companies, post=post)
        return Response(
            {"detail": "You liked this post."}, status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="user_unlike",
    )
    def user_unlike(self, request, pk=None):
        """Endpoint to unlike a post"""
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        try:
            like = Like.objects.get(profile=user, post=post)
            like.delete()
            return Response(
                {"detail": "You unliked this post."},
                status=status.HTTP_204_NO_CONTENT,
            )
            
        except Like.DoesNotExist:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
    @action(
        methods=["POST"],
        detail=True,
        url_path="company_unlike",
    )
    def company_unlike(self, request, pk=None):
        """Endpoint to unlike a post"""
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        try:
            company_like = Like.objects.get(company=user.companies, post=post)
            company_like.delete()
            return Response(
                {"detail": "You unliked this post."},
                status=status.HTTP_204_NO_CONTENT,
            )
            
        except Like.DoesNotExist:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        methods=["GET"],
        detail=False,
        url_path="user_my-posts",
    )
    def user_my_posts(self, request):
        """Endpoint to get all posts from the user"""
        user = request.user
        queryset = self.get_queryset().filter(user=user)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(
        methods=["GET"],
        detail=False,
        url_path="company_my-posts",
    )
    def company_my_posts(self, request):
        """Endpoint to get all posts from a company"""
        user = request.user
        queryset = self.get_queryset().filter(company=user.companies)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="user_feed",
    )
    def user_feed(self, request):
        """Endpoint to get all posts from followed users"""
        user = request.user
        followed_users = user.following.values_list("following", flat=True)
        queryset = self.get_queryset().filter(user__in=followed_users)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(
        methods=["GET"],
        detail=False,
        url_path="company_feed",
    )
    def company_feed(self, request):
        """Endpoint to get all posts from followed users"""
        company = request.user.companies
        followed_company = company.following.values_list("following", flat=True)
        queryset = self.get_queryset().filter(user__in=followed_company)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="user_liked",
    )
    def user_liked(self, request):
        """Endpoint to get all posts liked by the user"""
        user = request.user
        queryset = self.get_queryset().filter(likes__user=user)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(
        methods=["GET"],
        detail=False,
        url_path="company_liked",
    )
    def company_liked(self, request):
        """Endpoint to get all posts liked by the user"""
        user = request.user
        queryset = self.get_queryset().filter(likes__company=user.companies)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)