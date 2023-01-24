import logging
from .models import *
from .apps import MenuConfig as Configuration

ORDERING = Configuration.ordering

def get_all_dishes():
    try:
        return Foods.objects.all()
    except Exception as e:
        print("DISHES ERROR " + str(e))
        return []

# def get_all_drinks():
#     try:
#         return Foods.objects.all()
#     except Exception as e:
#         print("DISHES ERROR "+str(e))
#         return []

main_context = {
    "ordering": ORDERING,
    "categories": Category.objects.all(),
    "all_dishes": get_all_dishes(),
    "allergens": Allergens.objects.all()
}