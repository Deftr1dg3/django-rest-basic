# Generated by Django 5.1.2 on 2024-11-12 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]
