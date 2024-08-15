from django.db import models
from api.models.company_model import Company
from django.utils.text import slugify
from django.utils import timezone

class DocumentType(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True, unique=True)
    type = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(DocumentType, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    

class Document(models.Model):
    type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True, blank=True)
    document = models.FileField()
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, related_name='documents')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.type.name} {self.company.company_name}"