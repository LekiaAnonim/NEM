from api.serializers.company_serializer import CompanySerializer, CompanyCategorySerializer, CompanySizeSerializer
from api.models.company_model import Company, CompanyCategory, CompanySize
from rest_framework import generics
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, OuterRef, Exists, Subquery
from api.models.comment_model import FollowingRelationships
from api.serializers.comment_serializer import FollowerRelationshipSerializer, FollowingRelationshipSerializer
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
    
    @action(
        detail=True,
        methods=["POST"],
        url_path="follow",
        permission_classes=[IsAuthenticated],
        # authentication_classes=[JWTAuthentication],
    )
    def follow(self, request, pk=None):
        follower = get_object_or_404(Company, user=request.user)
        following = get_object_or_404(Company, pk=pk)

        if follower == following:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if FollowingRelationships.objects.filter(
            company_follower=follower, company_following=following
        ).exists():
            return Response(
                {"detail": "You are already following this company."},
                status=status.HTTP_409_CONFLICT,
            )

        FollowingRelationships.objects.create(company_follower=follower, company_following=following)
        return Response(
            {"detail": "You started following this company."},
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
        follower = get_object_or_404(Company, user=request.user)
        following = get_object_or_404(Company, pk=pk)

        try:
            relation = FollowingRelationships.objects.get(
                Q(company_follower=follower) & Q(company_following=following)
            )
            relation.delete()
            return Response(
                {"detail": "You have unfollowed this company."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except FollowingRelationships.DoesNotExist:
            return Response(
                {"detail": "You are not following this company."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
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
