# Generated by Django 4.1.2 on 2022-12-27 11:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergen_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Allergen',
                'verbose_name_plural': 'Allergens',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title_en', models.CharField(max_length=200, null=True, verbose_name='category_title')),
                ('category_title_el', models.CharField(max_length=200, null=True, verbose_name='category_title')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='SavedCarts',
            fields=[
                ('username', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('cart', models.TextField()),
            ],
            options={
                'verbose_name': 'Saved Users Cart',
                'verbose_name_plural': 'Saved Users Cart',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('order', models.TextField()),
                ('comments', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('table_number', models.IntegerField()),
                ('time_of_order', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('delivered', models.BooleanField()),
            ],
            options={
                'verbose_name': 'User Order List',
                'verbose_name_plural': 'User Order List',
            },
        ),
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=200)),
                ('dish_description', models.TextField(blank=True, null=True)),
                ('dish_image', models.ImageField(default='media/no-img-available.png', upload_to='food_imgs')),
                ('allergies', models.CharField(blank=True, default='', max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('enabled', models.BooleanField(default=1)),
                ('hidden', models.BooleanField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.category')),
            ],
            options={
                'verbose_name': 'Food',
                'verbose_name_plural': 'Foods',
            },
        ),
    ]
