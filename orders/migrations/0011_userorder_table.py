# Generated by Django 4.1.2 on 2022-10-15 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20221011_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='table',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=3),
            preserve_default=False,
        ),
    ]