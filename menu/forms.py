from django import forms
from .models import Foods, Drinks
from .apps import MenuConfig as Configuration
restaurant = Configuration.restaurant

image_help_text = """<button id="removeItemImage" type="button" class="btn btn-danger btn-sm mx-auto mt-2" onclick="removeImageAdmin('{restaurant}','{category}')">Remove Image</button>"""

class FoodsForm(forms.ModelForm):
    class Meta:
        model = Foods
        fields = '__all__'

    image = forms.ImageField(help_text=image_help_text.format(restaurant=restaurant,category='food'), required=False)

    file = open("templates/admin/forms/allergens.html", "r")
    allergens_table = file.read()
    file.close()
    allergies = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter allergen number and seperate with a comma (e.g. 1,2,3)'}),
        help_text=allergens_table)

class DrinksForm(forms.ModelForm):
    class Meta:
        model = Drinks
        fields = '__all__'

    image = forms.ImageField(help_text=image_help_text.format(restaurant=restaurant,category='drinks'), required=False)