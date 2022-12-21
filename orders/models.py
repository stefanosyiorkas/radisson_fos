from django.db import models
from datetime import datetime
from django.utils.translation import gettext as _
from translated_fields import TranslatedField

# Create your models here.

class Category(models.Model):
    category_title = TranslatedField(models.CharField(_("category_title"),max_length=200,null=True),)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.category_title}"

    def has_add_permission(self):
        return False

class Salad(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    dish_name = models.CharField(max_length=200)
    dish_description = models.TextField(null=True, blank=True)
    dish_image = models.ImageField(upload_to='salads', default='media/no-img-available.png')
    allergies = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    enabled = models.BooleanField(default=1)

    class Meta:
        verbose_name = "Salad"
        verbose_name_plural = "Salads"


    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Salad : {self.dish_name}"

class AllDaySnacks(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    dish_name = models.CharField(max_length=200)
    dish_description = models.TextField(null=True, blank=True)
    dish_image = models.ImageField(upload_to='snacks', default='media/no-img-available.png')
    allergies = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    enabled = models.BooleanField()

    class Meta:
        verbose_name = "All Day Snack"
        verbose_name_plural = "All Day Snacks"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Snack : {self.dish_name}"

class MainDishes(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    dish_name = models.CharField(max_length=200)
    dish_description = models.TextField(null=True, blank=True)
    dish_image = models.ImageField(upload_to='mains', default='media/no-img-available.png')
    allergies = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    enabled = models.BooleanField()

    class Meta:
        verbose_name = "Main Dish"
        verbose_name_plural = "Main Dishes"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Main : {self.dish_name}"

class Burgers(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    dish_name = models.CharField(max_length=200)
    dish_description = models.TextField(null=True, blank=True)
    dish_image = models.ImageField(upload_to='burgers', default='media/no-img-available.png')
    allergies = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    enabled = models.BooleanField()

    class Meta:
        verbose_name = "Burger"
        verbose_name_plural = "Burgers"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Burger : {self.dish_name}"

class Desserts(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    dish_name = models.CharField(max_length=200)
    dish_description = models.TextField(null=True, blank=True)
    dish_image = models.ImageField(upload_to='desserts', default='media/no-img-available.png')
    allergies = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    enabled = models.BooleanField()

    class Meta:
        verbose_name = "Dessert"
        verbose_name_plural = "Desserts"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Dessert : {self.dish_name}"


class Allergens(models.Model):
    allergen_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Allergen"
        verbose_name_plural = "Allergens"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.allergen_name}"

class Table(models.Model):
    table_number = models.IntegerField()

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
        verbose_name = "User Order List"
        verbose_name_plural = "User Order List"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Order placed by  : {self.username} on {self.time_of_order.date()} at {self.time_of_order.time().strftime('%H:%M:%S')}"

class SavedCarts(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    cart = models.TextField() #this will be a string representation of the cart from localStorage

    class Meta:
        verbose_name = "Saved Users Cart"
        verbose_name_plural = "Saved Users Cart"


    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Saved cart for {self.username}"
