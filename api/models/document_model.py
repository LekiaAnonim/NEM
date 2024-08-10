from django.db import models
from api.models.company_model import Company
from django.utils.text import slugify

class Document(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(max_length=500, null=True, blank=True)
    document = models.FileField()
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True)
    slug = models.SlugField(null=True,  max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Document, self).save(*args, **kwargs)