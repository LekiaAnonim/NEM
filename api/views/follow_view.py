from rest_framework import viewsets, permissions
from api.models.comment_model import FollowingRelationships, Like
from api.models.company_model import Company
from authentication.models import User
from api.serializers.all_serializer import FollowSerializer, LikeSerializer

class FollowViewSet(viewsets.ModelViewSet):
    queryset = FollowingRelationships.objects.all()
    serializer_class = FollowSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_follower = self.request.user if 'user_follower' in self.request.data else None
        company_follower = Company.objects.get(pk=self.request.data['company_follower']) if 'company_follower' in self.request.data else None
        user_following = User.objects.get(pk=self.request.data['user_following']) if 'user_following' in self.request.data else None
        company_following = Company.objects.get(pk=self.request.data['company_following']) if 'company_following' in self.request.data else None
        serializer.save(user_follower=user_follower, company_follower=company_follower, user_following=user_following, company_following=company_following)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user if 'user' in self.request.data else None
        company = Company.objects.get(pk=self.request.data['company']) if 'company' in self.request.data else None
        serializer.save(user=user, company=company)