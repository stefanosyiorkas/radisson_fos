import logging

from .apps import MenuConfig as Configuration
from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _
from django.utils.html import mark_safe

class CategoryBaseModel(models.Model):
    title = models.CharField("title",max_length=200,blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title}"

class Category(models.Model):
    order = models.PositiveIntegerField(default=0)
    title = models.CharField("title",max_length=200,blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.title}"

class Subcategory(CategoryBaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

class ItemBaseModel(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='item_imgs', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    enabled = models.BooleanField(default=1)
    available = models.BooleanField(default=1)
    has_options = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

    def __str__(self):
        return f"{self.subcategory}:{self.name}"

    def save_image(self):
        try:
            self.image.field.upload_to = f'{Configuration.name}_images/{self.__class__.__name__}/{self.subcategory}'
        except AttributeError as e:
            logging.error(e)

    def save(self, *args, **kwargs):
        self.save_image()
        super().save(*args, **kwargs)

    def item_image(self):
        if not self.image or self.image == 'none':
            self.image = "media/no-img-available.png"
        return mark_safe('<img src="/media/%s" style="width: 20rem; object-fit: cover;" />' % (self.image))
    item_image.short_description = 'Image Preview'


class Foods(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    dish_name = models.CharField(max_length=200)
    dish_description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='food_imgs', blank=True, null=True)
    allergies = models.CharField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    enabled = models.BooleanField(default=1)
    available = models.BooleanField(default=1)
    has_options = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Food"
    def __str__(self):
        return f"{self.category}:{self.dish_name}"

    def save(self, *args, **kwargs):
        try:
            self.image.field.upload_to = f'{Configuration.name}_images/{self.category}'
            super().save(*args, **kwargs)
        except AttributeError as e:
            logging.error(e)
            super().save(*args, **kwargs)

    def food_image(self):
        if not self.image or self.image == 'none':
            self.image = "media/no-img-available.png"
        return mark_safe('<img src="/media/%s" style="width: 20rem; object-fit: cover;" />' % (self.image))
    food_image.short_description = 'Image Preview'


class FoodOption(models.Model):
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    allergies = models.CharField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.food.dish_name} - {self.name}"

class Drinks(ItemBaseModel):
    class Meta:
        verbose_name = "Drink"
        verbose_name_plural = "Drinks"


class DrinkOption(models.Model):
    drink = models.ForeignKey(Drinks, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.drink.name} - {self.name}"

class Table(models.Model):
    table_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.table_number}"

class UserOrder(models.Model):
    username = models.CharField(max_length=200)
    order = models.TextField()
    comments = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    table_number = models.IntegerField()
    time_of_order  = models.DateTimeField(default=datetime.now, blank=True)
    delivered = models.BooleanField()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order placed by  : {self.username} on {self.time_of_order.date()} at {self.time_of_order.time().strftime('%H:%M:%S')}"

class SavedCarts(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    cart = models.TextField()

    class Meta:
        verbose_name = "Saved Cart"
        verbose_name_plural = "Saved Carts"


    def __str__(self):
        return f"Saved cart for {self.username}"
