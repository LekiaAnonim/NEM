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
from api.serializers.comment_serializer import FollowerRelationshipSerializer, FollowingRelationshipSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, OuterRef, Exists, Subquery
from api.models.comment_model import FollowingRelationships

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = (
            User.objects.prefetch_related(
                "following__user_following", "followers__user_follower"
            )
            .select_related("user")
            .annotate(
                followed_by_me=Exists(
                    FollowingRelationships.objects.filter(
                        user_follower__user=self.request.user, user_following=OuterRef("pk")
                    )
                ),
                followers_count=Count("followers"),
                following_count=Count("following"),
            )
        )

        username = self.request.query_params.get("username")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset
    
    @action(
        detail=True,
        methods=["POST"],
        url_path="follow",
        permission_classes=[IsAuthenticated],
        # authentication_classes=[JWTAuthentication],
    )
    def follow(self, request, pk=None):
        follower = get_object_or_404(User, email=request.user.email)
        following = get_object_or_404(User, pk=pk)

        if follower == following:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if FollowingRelationships.objects.filter(
            user_follower=follower, user_following=following
        ).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_409_CONFLICT,
            )

        FollowingRelationships.objects.create(user_follower=follower, user_following=following)
        return Response(
            {"detail": "You started following this user."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        methods=["POST"],
        url_path="unfollow",
        permission_classes=[IsAuthenticated],
        # authentication_classes=[JWTAuthentication],
    )
    def unfollow(self, request, pk=None):
        follower = get_object_or_404(User, email=request.user.email)
        following = get_object_or_404(User, pk=pk)

        try:
            relation = FollowingRelationships.objects.get(
                Q(user_follower=follower) & Q(user_following=following)
            )
            relation.delete()
            return Response(
                {"detail": "You have unfollowed this user."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except FollowingRelationships.DoesNotExist:
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

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