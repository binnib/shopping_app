# Generated by Django 3.0.6 on 2021-04-07 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20210406_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_delivered_date',
            field=models.DateTimeField(),
        ),
    ]