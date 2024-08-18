from api.models.post_model import Post
from rest_framework import serializers
# from api.serializers.company_serializer import CompanySerializer
# from api.serializers.comment_serializer import CommentSerializer
# from api.serializers.user_serializer import UserSerializer
# from api.serializers.product_serializer import ProductSerializer
# from api.serializers.service_serializer import ServiceSerializer
class PostSerializer(serializers.HyperlinkedModelSerializer):
    # company = CompanySerializer()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['body', 'company']
    
    def get_likes(self, obj):
        likes = obj.likes.all()
        return LikeSerializer(likes, many=True).data

    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data


class PostListSerializer(PostSerializer):
    liked_by_user = serializers.BooleanField(read_only=True)
    liked_by_company = serializers.BooleanField(read_only=True)
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ["liked_by_user","liked_by_company"]

class LikeSerializer(serializers.ModelSerializer):
    liked_by_user = serializers.CharField(source="user.first_name", read_only=True)
    liked_by_company = serializers.CharField(source="company.company_name", read_only=True)
    # user = UserSerializer(read_only=True)
    # company = CompanySerializer(read_only=True)
    post = PostSerializer(read_only=True)
    # product = ProductSerializer(read_only=True)
    # service = ServiceSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ("id", "liked_by_user", "liked_by_company", 'post')