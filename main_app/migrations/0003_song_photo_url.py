# Generated by Django 2.1.2 on 2018-10-17 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20181016_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='photo_url',
            field=models.CharField(default='https://cdn.shopify.com/s/files/1/0638/5445/products/Chicago.jpg?v=1487360969', max_length=200),
        ),
    ]
