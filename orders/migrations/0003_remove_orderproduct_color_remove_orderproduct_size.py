# Generated by Django 4.1 on 2023-01-29 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]
