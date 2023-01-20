from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _
from translated_fields import TranslatedField
from django.utils.html import mark_safe
# Create your models here.

class Category(models.Model):
    order = models.PositiveIntegerField(default=0)
    category_title = TranslatedField(models.CharField(_("category_title"),max_length=200,blank=True),)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.category_title}"


class Foods(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    dish_name = models.CharField(max_length=200)
    dish_description = models.TextField(null=True, blank=True)
    dish_image = models.ImageField(upload_to='food_imgs', default='media/no-img-available.png')
    allergies = models.CharField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    enabled = models.BooleanField(default=1)
    hidden = models.BooleanField()
    has_options = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Food"
    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.category}:{self.dish_name}"

    def save(self, *args, **kwargs):
        # Set the upload_to parameter based on the form data
        self.dish_image.field.upload_to = f'food_images/{self.category}'
        # Save the image
        super().save(*args, **kwargs)

    def food_image(self):
        return mark_safe('<img src="/media/%s" style="width: 20rem; object-fit: cover;" />' % (self.dish_image))
    food_image.short_description = 'Image Preview'


class FoodOption(models.Model):
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    allergies = models.CharField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.food.dish_name} - {self.name}"

class Drinks(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='drinks', default='media/no-img-available.png')
    available = models.BooleanField(default=True)
    has_options = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Drink"
        verbose_name_plural = "Drinks"

    def __str__(self):
        return self.name


class DrinkOption(models.Model):
    drink = models.ForeignKey(Drinks, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.drink.name} - {self.name}"


class Allergens(models.Model):
    allergen_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Allergen"
        verbose_name_plural = "Allergens"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.allergen_name}"

class Table(models.Model):
    table_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.table_number}"

class UserOrder(models.Model):
    username = models.CharField(max_length=200) #who placed the order
    order = models.TextField() #this will be a string representation of the cart from localStorage
    comments = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) #how much was the order
    table_number = models.IntegerField()
    time_of_order  = models.DateTimeField(default=datetime.now, blank=True)
    delivered = models.BooleanField()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Order placed by  : {self.username} on {self.time_of_order.date()} at {self.time_of_order.time().strftime('%H:%M:%S')}"

class SavedCarts(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    cart = models.TextField() #this will be a string representation of the cart from localStorage

    class Meta:
        verbose_name = "Saved Cart"
        verbose_name_plural = "Saved Carts"


    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Saved cart for {self.username}"
