from django.db import models
from authentication.models import User
from wagtail.fields import RichTextField
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

class CompanyCategory(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True, unique=True)
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(CompanyCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class CompanySize(models.Model):
    size = models.CharField(max_length=500, null=True, blank=True, unique=True)
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.size, allow_unicode=True)
        super(CompanySize, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.size}"

class Company(models.Model):
    profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="companies")
    company_name = models.CharField(max_length=500, null=True, blank=True, unique=True)
    organization_type = models.ForeignKey(CompanyCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="companies")
    about = RichTextField(null=True, blank=True)
    tag_line = models.CharField(max_length=500, null=True, blank=True)
    company_size = models.ForeignKey(CompanySize, on_delete=models.DO_NOTHING, null=True, related_name="companies")
    logo = models.ImageField(null=True, blank=True)
    banner = models.ImageField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    office_address = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    verify = models.BooleanField(default=False)
    slug = models.SlugField(null=True,  max_length=500)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.company_name, allow_unicode=True)
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_name}"
