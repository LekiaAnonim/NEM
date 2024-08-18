from rest_framework import serializers

from api.models.comment_model import FollowingRelationships, Comment, Like
# from api.serializers.user_serializer import UserSerializer
# from api.serializers.company_serializer import CompanySerializer
# from api.serializers.post_serializer import PostSerializer


class FollowSerializer(serializers.ModelSerializer):
    user_follower = serializers.ReadOnlyField(source='user_follower.first_name')
    company_follower = serializers.ReadOnlyField(source='company_follower.company_name')
    user_following = serializers.ReadOnlyField(source='user_following.first_name')
    company_following = serializers.ReadOnlyField(source='company_following.company_name')

    class Meta:
        model = FollowingRelationships
        fields = ['id', 'user_follower', 'company_follower', 'user_following', 'company_following']

class FollowingRelationshipSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user_following.id", read_only=True)
    first_name = serializers.CharField(source="user_following.first_name")
    company_id = serializers.IntegerField(source="company_following.id", read_only=True)
    company_name = serializers.CharField(source="company_following.company_name")

    class Meta:
        model = FollowingRelationships
        fields = ("user_id", "first_name", "company_id", "company_name")


class FollowerRelationshipSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user_follower.id", read_only=True)
    first_name = serializers.CharField(source="user_follower.first_name")
    company_id = serializers.IntegerField(source="company_follower.id", read_only=True)
    company_name = serializers.CharField(source="company_follower.company_name")

    class Meta:
        model = FollowingRelationships
        fields = ("user_id", "first_name", "company_id", "company_name")


class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source="post.id", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    company_name = serializers.CharField(source="company.company_name", read_only=True)
    commented_at = serializers.DateTimeField(read_only=True)
    # user = UserSerializer(read_only=True)
    # company = CompanySerializer(read_only=True)
    # post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "user_first_name", "company_name", "post_id", "content", "commented_at")

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name')
    company = serializers.ReadOnlyField(source='company.company_name')

    class Meta:
        model = Like
        fields = ['id', 'user', 'company', 'post', 'product', 'service']