# Generated by Django 4.1.8 on 2024-08-08 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=500, null=True)),
                ('about', wagtail.fields.RichTextField(blank=True, null=True)),
                ('tag_line', models.CharField(blank=True, max_length=500, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('office_address', models.CharField(blank=True, max_length=500, null=True)),
                ('country', models.CharField(blank=True, max_length=500, null=True)),
                ('state', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.CharField(blank=True, max_length=500, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('verify', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=500, null=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanySize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', wagtail.fields.RichTextField()),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_updated', models.DateField(auto_now=True)),
                ('featured', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', wagtail.fields.RichTextField()),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_updated', models.DateField(auto_now=True)),
                ('featured', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(upload_to='service/')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.service')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.servicecategory'),
        ),
        migrations.AddField(
            model_name='service',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_company', to='api.company'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(upload_to='product/')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_company', to='api.company'),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', wagtail.fields.RichTextField()),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_updated', models.DateField(auto_now=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.company')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('type', models.CharField(blank=True, max_length=500, null=True)),
                ('document', models.FileField(upload_to='')),
                ('slug', models.SlugField(max_length=500, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.company')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='company_size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.companysize'),
        ),
        migrations.AddField(
            model_name='company',
            name='organization_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.companycategory'),
        ),
        migrations.AddField(
            model_name='company',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]