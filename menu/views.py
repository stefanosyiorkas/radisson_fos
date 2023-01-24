from . import forms
from .common_views import *

if Configuration.ordering:
    from menu.ordering_functionality.ordering_views import *

import json
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

def index(request):
    # Save table
    if request.user.is_authenticated:
        table = request.GET.get('table')
        tables = [str(table.table_number) for table in Table.objects.all()]
        try:
            if table in tables:
                request.session['table'] = int(table)
        except (TypeError, ValueError):
            print(f"Table << {table} >> is not valid")

    if 'Guest' not in request.user.username:
        request.session['username'] = request.user.username

    main_context["all_dishes"] = get_all_dishes()

    # Get last order
    try:
        last_order = UserOrder.objects.filter(username=request.user.username).order_by('-time_of_order')[0]
        minutes_diff = ((datetime.now() - timedelta(hours=2)) - last_order.time_of_order.replace(
            tzinfo=None)).total_seconds() / 60.0
        main_context['last_order'] = last_order if round(minutes_diff) < 15 else None
    except IndexError:
        main_context['last_order'] = None

    # Setup allergens.txt for all dishes
    allergens = main_context["allergens"]
    allergens_dict = {str(allergen.id): allergen.allergen_name for allergen in allergens}
    for dish in main_context['all_dishes']:
        try:
            allergens_temp = [[allergie, allergens_dict[allergie]] for allergie in dish.allergies.split(",")]
            dish.allergies = allergens_temp
        except AttributeError as e:
            print(e)
            pass
        except KeyError as e:
            print(f"ALLERGENS KeyError: {e}")
            if len(dish.allergies) > 0:
                dish.allergies = dish.allergies.split(",")
            pass
    return render(request, "menu/home.html", main_context)

def login_request(request):
    if request.method == 'POST':
        form = forms.Login(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('/')
        else:
            return render(request=request,
                          template_name="menu/login.html",
                          context={"form": form, "error": "Incorrect Username or Password"})
    form = forms.Login()
    return render(request=request,
                  template_name="menu/login.html",
                  context={"form": form})

def logout_request(request):
    logout(request)
    return render(request, "menu/home.html", main_context)

def register(request):
    if request.method == "POST":
        form = forms.Registration(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("menu:index")

        return render(request=request,
                      template_name="menu/register.html",
                      context={"form": form})
    form = forms.Registration()
    return render(request=request,
                  template_name="menu/register.html",
                  context={"form": form})

def contact(request):
    return render(request, "menu/contact.html")

def set_default_image(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        item = Foods.objects.filter(pk=id)
        item.first().dish_image.delete()
        item.update(dish_image='media/no-img-available.png')

        return HttpResponse(
            json.dumps({"good": "boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def check_superuser(request):
    return HttpResponse(request.user.is_superuser)

def check_staff_user(request):
    return HttpResponse(request.user.is_staff)


def handle_404(request, exception):
    return render(request, 'menu/404.html')

def handle_500(request):
    return render(request, 'menu/500.html')

def handle_403(request, exception):
    return render(request, 'menu/403.html')
