# Generated by Django 4.1.2 on 2022-11-29 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0037_userorder_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='salad',
            name='dish_image2',
            field=models.ImageField(default='media/no-img-available.png', upload_to='salads'),
        ),
    ]
