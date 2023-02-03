from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Allergens(models.Model):
    allergen_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Allergen"
        verbose_name_plural = "Allergens"

    def __str__(self):
        return f"{self.allergen_name}"