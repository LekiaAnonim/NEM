# Generated by Django 4.1.8 on 2024-07-15 00:02

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0092_remove_formsubmission_page_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500, null=True)),
                ('answer', wagtail.fields.RichTextField(blank=True)),
                ('accordion_heading_id', models.CharField(max_length=500, null=True)),
                ('flush_collapse_id', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('hero_section_message', wagtail.fields.RichTextField(blank=True)),
                ('our_mission', wagtail.fields.RichTextField(blank=True)),
                ('our_vision', wagtail.fields.RichTextField(blank=True)),
                ('our_promise', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=500, null=True)),
                ('message', wagtail.fields.RichTextField(blank=True)),
                ('avatar', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image')),
            ],
        ),
    ]
