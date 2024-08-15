from django.db import models
from wagtail.fields import RichTextField
from api.models.company_model import Company
from django.utils.text import slugify
from django.utils import timezone

class ProductCategory(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True, unique=True)
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    

class Product(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    sub_title = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, null=True, related_name='products')
    description = RichTextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='products')
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}, {self.category}"

class ProductImage(models.Model):
    caption = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='product/')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)