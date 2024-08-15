from django.db import models
from wagtail.fields import RichTextField
from api.models.company_model import Company
from django.utils.text import slugify
from django.utils import timezone

class ServiceCategory(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True, unique=True)
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(ServiceCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Service(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    sub_title = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.DO_NOTHING, null=True, related_name='services')
    description = RichTextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='services')
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.category}"

class ServiceImage(models.Model):
    caption = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='service/')
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, null=True)