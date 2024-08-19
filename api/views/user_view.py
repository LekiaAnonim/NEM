from api.serializers.user_serializer import UserSerializer, GenderSerializer
from authentication.models import User, Gender
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)
from api.serializers.all_serializer import FollowerRelationshipSerializer, FollowingRelationshipSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, OuterRef, Exists, Subquery
from api.models.comment_model import FollowingRelationships

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['post'], url_path='follow')
    def follow_user(self, request, pk=None):
        target_user = self.get_object()  # The user being followed
        user = request.user  # The user making the request
        follower_company = request.data.get('company_id')  # The company making the request, if any

        if user == target_user and follower_company is None:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = FollowingRelationships.objects.get_or_create(
            user_following=target_user,
            user_follower=user if user.is_authenticated else None,
            company_follower_id=follower_company if follower_company else None
        )
        
        if not created:
            return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "User followed."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='unfollow')
    def unfollow_user(self, request, pk=None):
        target_user = self.get_object()  # The user being unfollowed
        user = request.user  # The user making the request
        follower_company = request.data.get('company_id')  # The company making the request, if any

        follow = FollowingRelationships.objects.filter(
            user_following=target_user,
            user_follower=user if user.is_authenticated else None,
            company_follower_id=follower_company if follower_company else None
        ).first()

        if not follow:
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        follow.delete()
        return Response({"detail": "User unfollowed."}, status=status.HTTP_204_NO_CONTENT)

class UserFollowersView(ListAPIView):
    serializer_class = FollowerRelationshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.followers.all()


class UserFollowingView(ListAPIView):
    serializer_class = FollowingRelationshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.following.all()
    
class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class CurrentUserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            User.objects.filter(email=self.request.user.email)
            .select_related("email")
            .prefetch_related("user_following", "user_followers")
            .annotate(
                followers_count=Count("user_followers"), following_count=Count("user_following")
            )
        )

    def get_object(self):
        return get_object_or_404(self.get_queryset())

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        user.delete()
        return response