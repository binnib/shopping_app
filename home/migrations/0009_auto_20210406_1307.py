# Generated by Django 3.0.6 on 2021-04-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_order_cart_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]