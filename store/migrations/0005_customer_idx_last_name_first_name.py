# Generated by Django 5.1 on 2024-10-08 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_address_demo'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name', 'first_name'], name='idx_last_name_first_name'),
        ),
    ]