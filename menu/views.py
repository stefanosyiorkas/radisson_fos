import json
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from main.models import Allergens
from .apps import MenuConfig as Configuration
ORDERING = Configuration.ordering

def get_all_dishes():
    try:
        return Foods.objects.all()
    except Exception as e:
        print("DISHES ERROR " + str(e))
        return []

main_context = {
    "restaurant": 'restaurant1',
    "ordering": ORDERING,
    "categories": Category.objects.all(),
    "all_dishes": get_all_dishes(),
    "allergens": Allergens.objects.all()
}

if ORDERING:
    from .ordering_functionality.ordering_views import *

def save_table(request):
    if request.user.is_authenticated:
        table = request.GET.get('table')
        tables = [str(table.table_number) for table in Table.objects.all()]
        try:
            if table in tables:
                return int(table)
        except (TypeError, ValueError):
            logging.error(f"Table << {table} >> is not valid")
            return None
    else:
        return None

def get_last_order(request):
    try:
        last_order = UserOrder.objects.filter(username=request.user.username).order_by('-time_of_order')[0]
        minutes_diff = ((datetime.now() - timedelta(hours=2)) - last_order.time_of_order.replace(
            tzinfo=None)).total_seconds() / 60.0
        return last_order if round(minutes_diff) < 15 else None
    except IndexError:
        return None

def setup_allergens(allergens_table, all_dishes):
    allergens_dict = {str(allergen.id): allergen.allergen_name for allergen in allergens_table.objects.all()}
    for dish in all_dishes:
        try:
            allergens_temp = [[allergie, allergens_dict[allergie]] for allergie in dish.allergies.split(",")]
            dish.allergies = allergens_temp
        except AttributeError as e:
            logging.error(e)
        except KeyError as e:
            logging.error(f"ALLERGENS KeyError for {dish}: {e}")
            if len(dish.allergies) > 0:
                dish.allergies = dish.allergies.split(",")

def index(request):
    request.session['restaurant'] = main_context['restaurant']

    if ORDERING:
        request.session['table'] = save_table(request)
        request.session['username'] = request.user.username
        main_context['last_order'] = get_last_order(request)

    setup_allergens(Allergens, main_context['all_dishes'])
    return render(request, "menu/home.html", main_context)

def contact(request):
    return render(request, "menu/contact.html")

def set_default_image(request, category):
    if request.method == 'POST':
        if category == 'food':
            table = Foods
        elif category == 'drinks':
            table = Drinks
        else:
            table = None
        image_id = request.POST.get('id')
        item = table.objects.filter(pk=image_id)
        item.first().image.delete()
        item.update(image=None)
        return HttpResponse('Default image set to default')