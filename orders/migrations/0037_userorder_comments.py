# Generated by Django 4.1.2 on 2022-11-18 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0036_remove_category_category_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='comments',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
