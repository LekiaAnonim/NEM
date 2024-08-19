from rest_framework import serializers

from api.models.comment_model import FollowingRelationships, Comment, Like
from api.serializers.user_serializer import UserSerializer
from api.models.company_model import Company, CompanyCategory, CompanySize
from api.models.document_model import Document, DocumentType
from api.models.post_model import Post
from api.models.product_model import Product, ProductCategory, ProductImage
from api.models.service_model import Service, ServiceCategory, ServiceImage
from authentication.models import User

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.SlugRelatedField(queryset=DocumentType.objects.all(), slug_field='name')
    
    class Meta:
        model = Document
        fields = ['id', 'type', 'document', 'company']

class DocumentTypeSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:documenttype-detail')
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'type']



class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:product-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:productcategory-detail')
    class Meta:
        model = ProductCategory
        fields = ['id', 'url', 'name', 'products']

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:productimage-detail')
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='title')
    class Meta:
        model = ProductImage
        fields = ['id', 'url', 'caption', 'image', 'product']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(queryset=ProductCategory.objects.all(), slug_field='name')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='company_name')
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'sub_title', 'category', 'description', 'date_created', 
                  'date_updated', 'featured', 'company','likes', 'images']
        
    def get_likes(self, obj):
        likes = obj.likes.all()
        return LikeSerializer(likes, many=True).data
    
class ServiceCategorySerializer(serializers.HyperlinkedModelSerializer):
    services = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:service-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:servicecategory-detail')
    class Meta:
        model = ServiceCategory
        fields = ['id', 'url',  'name', 'services']

class ServiceImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:serviceimage-detail')
    service = serializers.SlugRelatedField(queryset=Service.objects.all(), slug_field='title')
    class Meta:
        model = ServiceImage
        fields = ['id', 'url', 'caption', 'image', 'service']

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(queryset=ServiceCategory.objects.all(), slug_field='name')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='company_name')
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = ['id', 'title', 'sub_title', 'category', 'description', 'date_created', 
                  'date_updated', 'featured', 'company', 'likes']
        
    def get_likes(self, obj):
        likes = obj.likes.all()
        return LikeSerializer(likes, many=True).data


class CompanySizeSerializer(serializers.HyperlinkedModelSerializer):
    companies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:company-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:companysize-detail')
    class Meta:
        model = CompanySize
        fields = ['id', 'url', 'size', 'companies']

class CompanyCategorySerializer(serializers.HyperlinkedModelSerializer):
    companies = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:company-detail')
    url = serializers.HyperlinkedRelatedField(
                    many=True,
                    read_only=True,
                    view_name='api:companycategory-detail')
    class Meta:
        model = CompanyCategory
        fields = ['id', 'url', 'name', 'companies']


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    organization_type = serializers.SlugRelatedField(queryset=CompanyCategory.objects.all(), slug_field='name')
    company_size = serializers.SlugRelatedField(queryset=CompanySize.objects.all(), slug_field='size')
    profile = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')
    documents = DocumentSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    profile = serializers.ReadOnlyField(source='profile.email')
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    url = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api:company-detail')
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ['id', 'url', 'profile', 'company_name', 'organization_type', 'about', 'tag_line', 
                  'company_size', 'logo', 'banner', 'email', 'office_address', 'country', 
                  'state', 'city', 'website', 'verify',"followers_count",
            "following_count", 'documents', 'products', 'services', 'followers', 'following']
        
    def get_followers(self, obj):
        followers = obj.followers.all()
        return FollowSerializer(followers, many=True).data
    
    def get_following(self, obj):
        following = obj.following.all()
        return FollowSerializer(following, many=True).data
    
class PostSerializer(serializers.HyperlinkedModelSerializer):
    company = CompanySerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'body', 'company', 'likes', 'comments']
    
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

class FollowSerializer(serializers.ModelSerializer):
    user_follower = UserSerializer(read_only=True)
    company_follower = CompanySerializer(read_only=True)
    user_following = UserSerializer(read_only=True)
    company_following = CompanySerializer(read_only=True)

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
        fields = ('id', "user_id", "first_name", "company_id", "company_name")


class FollowerRelationshipSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user_follower.id", read_only=True)
    first_name = serializers.CharField(source="user_follower.first_name")
    company_id = serializers.IntegerField(source="company_follower.id", read_only=True)
    company_name = serializers.CharField(source="company_follower.company_name")

    class Meta:
        model = FollowingRelationships
        fields = ('id', "user_id", "first_name", "company_id", "company_name")


class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source="post.id", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    company_name = serializers.CharField(source="company.company_name", read_only=True)
    commented_at = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "user_first_name", "company_name", "post_id", "content", "commented_at", 'user', 'company', 'post')



class LikeSerializer(serializers.ModelSerializer):
    liked_by_user = serializers.CharField(source="user.first_name", read_only=True)
    liked_by_company = serializers.CharField(source="company.company_name", read_only=True)
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    post = PostSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ("id", "liked_by_user", "liked_by_company", 'post', 'user', 'company', 'product', 'service')