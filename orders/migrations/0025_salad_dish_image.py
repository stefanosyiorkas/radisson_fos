# Generated by Django 4.1.2 on 2022-10-26 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_extratoppings'),
    ]

    operations = [
        migrations.AddField(
            model_name='salad',
            name='dish_image',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]