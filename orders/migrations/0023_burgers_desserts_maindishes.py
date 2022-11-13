# Generated by Django 4.1.2 on 2022-10-25 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_toppings_dish_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Burgers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=200)),
                ('dish_description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'verbose_name': 'List of Burgers',
                'verbose_name_plural': 'List of Burgers',
            },
        ),
        migrations.CreateModel(
            name='Desserts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=200)),
                ('dish_description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'verbose_name': 'List of Desserts',
                'verbose_name_plural': 'List of Desserts',
            },
        ),
        migrations.CreateModel(
            name='MainDishes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=200)),
                ('dish_description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'verbose_name': 'List of Main Dishes',
                'verbose_name_plural': 'List of Main Dishes',
            },
        ),
    ]