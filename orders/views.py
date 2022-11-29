from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Category, Salad, AllDaySnacks, MainDishes, Burgers, Desserts, Allergens, UserOrder, SavedCarts, Table
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
import json
from . import forms
import requests
from urllib.parse import urlencode
from guest_user.decorators import allow_guest_user
from itertools import chain
from datetime import datetime, timedelta, timezone

def get_all_dishes():
    try:
        return list(chain(Salad.objects.all(), AllDaySnacks.objects.all(), MainDishes.objects.all(), Burgers.objects.all(),Desserts.objects.all(),))
    except Exception as e:
        print("DISHES ERROR "+str(e))
        return None

main_context = {
    "categories": Category.objects.all(),
    "all_dishes": get_all_dishes(),
    "allergens": Allergens.objects.all()
}

def index(request):
    main_context["all_dishes"] = get_all_dishes()

    try:
        last_order = UserOrder.objects.filter(username=request.user.username).order_by('-time_of_order')[0]
        minutes_diff = (datetime.now() - last_order.time_of_order.replace(tzinfo=None)).total_seconds() / 60.0
        main_context['last_order'] = last_order if round(minutes_diff) < 15 else None
    except IndexError:
        main_context['last_order'] = None

    # Setup allergens for all dishes
    allergens = main_context["allergens"]
    allergens_dict = { str(allergen.id):allergen.allergen_name for allergen in allergens}
    for dish in main_context['all_dishes']:
        try:
            allergens_temp = [allergens_dict[allergie] for allergie in dish.allergies.split(",")]
            dish.allergies = allergens_temp
        except AttributeError as e:
            pass
            # print(f"Error in ({dish}):", e)

    return render(request, "orders/home.html", main_context)

@allow_guest_user
def hello_guest(request):
    table = request.GET.get('table')
    tables = [str(table.table_number) for table in Table.objects.all()]
    try:
        if table in tables:
            request.session['table'] = int(table)
    except (TypeError, ValueError):
        print(f"Table << {table} >> is not valid")

    """
    SOURCE: https://django-guest-user.readthedocs.io/en/latest/usage.html
    This view will always have an authenticated user, but some may be guests.
    The default username generator will create a UUID4.

    Example response: "Hello, b5daf1dd-1a2f-4d18-a74c-f13bf2f086f7!"
    """
    # return HttpResponse(f"Hello, {request.user.username}!")
    return redirect("orders:index")

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
            return render(request = request,
                    template_name = "orders/login.html",
                    context={"form":form,"error":"Incorrect Username or Password"})
    form = forms.Login()
    return render(request = request,
                    template_name = "orders/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    return render(request, "orders/home.html",  main_context)

def register(request):
    if request.method == "POST":
        form = forms.Registration(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("orders:index")

        return render(request = request,
                          template_name = "orders/register.html",
                          context={"form":form})
    form = forms.Registration()
    return render(request = request,
                  template_name = "orders/register.html",
                  context={"form":form})

def directions(request):
    return render(request, "orders/directions.html")

def hours(request):
    return render(request, "orders/hours.html")

def contact(request):
    return render(request, "orders/contact.html")

@login_required(login_url='orders:login')
def cart(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, "orders/cart.html", context)

def send_slack(username, message, icon=None):
    post_data = {"payload": {"username": username, "text": message}}
    if icon is not None:
        post_data = {'payload': '{"username": "' + username + '", '
                                    '"icon_emoji": "' + icon + '", '
                                    '"text": "' + message + '"}'
                            }
    requests.post("https://hooks.slack.com/services/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", data=urlencode(post_data), headers={'Content-Type': 'application/x-www-form-urlencoded'})

def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart'))
        price = request.POST.get('price_of_cart')
        table_num = request.POST.get('table_number')
        username = request.user.username
        response_data = {}
        list_of_items = [item["item_description"] for item in cart]
        list_of_comments = [item['comments'] for item in cart]

        order = UserOrder(username=username, order=list_of_items, comments=list_of_comments, price=float(price), table_number=table_num, delivered=False) #create the row entry
        order.save() #save row entry in database

        response_data['result'] = 'Order Recieved!'
        # send_slack(username='Lobby Lounge', message=f'*{strftime("%Y-%m-%d %H:%M:%S", gmtime())}* - New order received')
        # requests.post('https://api.mynotifier.app', {
        #       "apiKey": '0326b712-bb7e-4860-97bc-b3205482232b', # This is your own private key
        #       "message": f"New Order!", # Could be anything
        #       "description": f"New Order placed by {request.user.username}", # Optional
        #       "body": "", # Optional
        #       "type": "info", # info, error, warning or success
        #       "project": "" # Optional. Project ids can be found in project tab <-
        #     })
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required(login_url='orders:login')
def order_success(request):
    try:
        order = UserOrder.objects.filter(username=request.user.username).order_by('-time_of_order')[0]
        order_list = [[item,comment] for item,comment in zip(order.order.strip('][').replace("'","").split(', '),order.comments.strip('][').replace("'","").split(', ')) ]
        all_dishes_prices = { dish.dish_name:dish.price for dish in main_context["all_dishes"]}
        for dish in order_list:
            dish.append(all_dishes_prices[dish[0]])
        print(order_list)
    except KeyError as e:
        print(e)

    return render(request, "orders/order_received.html", context={"order": order, "order_list":order_list})

@login_required(login_url='orders:login')
def view_orders(request):
    if request.user.is_superuser or request.user.is_staff:
        #make a request for all the orders in the database
        rows = UserOrder.objects.all().order_by('-time_of_order')
        for row in rows:
            order_list = row.order.strip('][').replace("'","").split(', ')
            comment_list = row.comments.strip('][').replace("'","").split(', ')
            row_temp = [item + f" ({comment})" if comment else item for item,comment in zip(order_list,comment_list)]
            row.orderlist = str(row_temp)
        return render(request, "orders/orders.html", context = {"rows":rows})
    else:
        rows = UserOrder.objects.all().filter(username = request.user.username).order_by('-time_of_order')
        return render(request, "orders/orders.html", context = {"rows":rows})

def mark_order_as_delivered(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        UserOrder.objects.filter(pk=id).update(delivered=True)
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def mark_order_as_pending(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        UserOrder.objects.filter(pk=id).update(delivered=False)
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def save_cart(request):
    if request.method == 'POST':
        if not request.user.is_superuser or not request.user.is_staff:
            if 'Guest' not in request.user.username:
                cart = request.POST.get('cart')
                saved_cart = SavedCarts(username=request.user.username, cart=cart) #create the row entry
                saved_cart.save() #save row entry in database
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def retrieve_saved_cart(request):
    try:
        saved_cart = SavedCarts.objects.get(username = request.user.username)
        return HttpResponse(saved_cart.cart)
    except:
        return HttpResponse('')

def check_superuser(request):
    print(f"User super??? {request.user.is_superuser}")
    return HttpResponse(request.user.is_superuser)

def check_staff_user(request):
    print(f"User staff??? {request.user.is_staff}")
    return HttpResponse(request.user.is_staff)

def handle_404(request,exception):
    return render(request, 'orders/404.html')
