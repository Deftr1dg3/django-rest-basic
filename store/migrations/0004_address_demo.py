# Generated by Django 5.1 on 2024-10-08 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='demo',
            field=models.CharField(default='00000', max_length=16),
        ),
    ]