# Generated by Django 5.1.2 on 2024-11-10 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_cartitem_cart_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
    ]
