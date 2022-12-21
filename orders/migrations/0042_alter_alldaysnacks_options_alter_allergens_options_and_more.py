# Generated by Django 4.1.2 on 2022-12-21 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0041_alter_alldaysnacks_dish_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alldaysnacks',
            options={'verbose_name': 'All Day Snack', 'verbose_name_plural': 'All Day Snacks'},
        ),
        migrations.AlterModelOptions(
            name='allergens',
            options={'verbose_name': 'Allergen', 'verbose_name_plural': 'Allergens'},
        ),
        migrations.AlterModelOptions(
            name='burgers',
            options={'verbose_name': 'Burger', 'verbose_name_plural': 'Burgers'},
        ),
        migrations.AlterModelOptions(
            name='desserts',
            options={'verbose_name': 'Dessert', 'verbose_name_plural': 'Desserts'},
        ),
        migrations.AlterModelOptions(
            name='maindishes',
            options={'verbose_name': 'Main Dish', 'verbose_name_plural': 'Main Dishes'},
        ),
        migrations.AlterModelOptions(
            name='salad',
            options={'verbose_name': 'Salad', 'verbose_name_plural': 'Salads'},
        ),
        migrations.AlterField(
            model_name='category',
            name='category_title_el',
            field=models.CharField(max_length=200, null=True, verbose_name='category_title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='category_title'),
        ),
        migrations.AlterField(
            model_name='salad',
            name='enabled',
            field=models.BooleanField(default=1),
        ),
    ]
