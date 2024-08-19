from api.serializers.all_serializer  import CompanySerializer, CompanyCategorySerializer, CompanySizeSerializer
from api.models.company_model import Company, CompanyCategory, CompanySize
from rest_framework import generics
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, OuterRef, Exists, Subquery
from api.models.comment_model import FollowingRelationships
from api.serializers.all_serializer import FollowerRelationshipSerializer, FollowingRelationshipSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    get_object_or_404,  
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['organization_type', 'company_size', 'country', 'date_created']
    search_fields = (
        '^company_name',
    )
    ordering_fields = (
        'company_name',
        'date_created'
    )

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    @action(detail=True, methods=['post'], url_path='follow')
    def follow_company(self, request, pk=None):
        company = self.get_object()
        user = request.user
        follower_company = request.data.get('company_id')
        follow, created = FollowingRelationships.objects.get_or_create(company_following=company, user_follower=user if user.is_authenticated else None, company_follower_id=follower_company if follower_company else None)
        if not created:
            return Response({"detail": "Already following this company."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Company followed."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='unfollow')
    def unfollow_company(self, request, pk=None):
        company = self.get_object()
        user = request.user
        follower_company = request.data.get('company_id')
        follow = FollowingRelationships.objects.filter(company_following=company, user_follower=user if user.is_authenticated else None, company_follower_id=follower_company if follower_company else None).first()
        if not follow:
            return Response({"detail": "You are not following this company."}, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response({"detail": "Company unfollowed."}, status=status.HTTP_204_NO_CONTENT)
        
# class CompanyFollowersView(ListAPIView):
#     serializer_class = FollowerRelationshipSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return user.companies.followers.all()


# class CompanyFollowingView(ListAPIView):
#     serializer_class = FollowingRelationshipSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return user.companies.following.all()



class CompanyCategoryViewSet(viewsets.ModelViewSet):
    queryset = CompanyCategory.objects.all()
    serializer_class = CompanyCategorySerializer


class CompanySizeViewSet(viewsets.ModelViewSet):
    queryset = CompanySize.objects.all()
    serializer_class = CompanySizeSerializer
