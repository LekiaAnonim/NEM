# Generated by Django 4.1.8 on 2024-02-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_faqs_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='accordion_heading_id',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='flush_collapse_id',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
