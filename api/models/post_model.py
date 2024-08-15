from django.db import models
# from wagtail.fields import RichTextField
from api.models.company_model import Company
from django.utils import timezone

class Post(models.Model):
    body = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True)
    