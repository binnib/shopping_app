# Generated by Django 3.0.6 on 2021-04-06 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210406_0703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_item',
        ),
    ]
