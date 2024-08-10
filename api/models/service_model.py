from django.db import models
from wagtail.fields import RichTextField
from api.models.company_model import Company
from django.utils.text import slugify
from django.utils import timezone

class ServiceCategory(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(ServiceCategory, self).save(*args, **kwargs)

class Service(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    sub_title = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.DO_NOTHING, null=True)
    description = RichTextField()
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)
    featured = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='service_company')
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Service, self).save(*args, **kwargs)

class ServiceImage(models.Model):
    caption = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='service/')
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, null=True)