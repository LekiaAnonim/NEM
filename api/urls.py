from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import user_view, company_view, document_view, post_view, product_view, service_view
from rest_framework.routers import DefaultRouter

app_name = "api"

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'companies', company_view.CompanyViewSet, basename='company')
router.register(r'users', user_view.UserViewSet, basename='user')
router.register(r'genders', user_view.GenderViewSet, basename='gender')
router.register(r'company-categories', company_view.CompanyCategoryViewSet, basename='company-category')
router.register(r'company-sizes', company_view.CompanySizeViewSet, basename='company-size')
router.register(r'documents', document_view.DocumentViewSet, basename='document')
router.register(r'document-types', document_view.DocumentTypeViewSet, basename='document-type')
router.register(r'posts', post_view.PostViewSet, basename='post')
router.register(r'products', product_view.ProductViewSet, basename='product')
router.register(r'product-images', product_view.ProductImageViewSet, basename='product-image')
router.register(r'product-categories', product_view.ProductCategoryViewSet, basename='product-category')
router.register(r'services', service_view.ServiceViewSet, basename='service')
router.register(r'service-images', service_view.ServiceImageViewSet, basename='service-image')
router.register(r'service-categories', service_view.ServiceCategoryViewSet, basename='service-category')
urlpatterns = [
    path('', include(router.urls)),
    
]