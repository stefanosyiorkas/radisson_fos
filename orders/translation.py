from modeltranslation.translator import register, TranslationOptions
from .models import Category,Salad

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_title',)

@register(Salad)
class SaladTranslationOptions(TranslationOptions):
    fields = ('dish_name','dish_description')
