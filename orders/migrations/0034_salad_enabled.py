# Generated by Django 4.1.2 on 2022-11-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0033_burgers_dish_image_desserts_dish_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salad',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
