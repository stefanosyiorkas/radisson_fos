from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Category, RegularPizza, SicilianPizza, Toppings, Sub, Pasta, Salad, DinnerPlatters, AllDaySnacks, MainDishes, Burgers, Desserts, Allergens, UserOrder, SavedCarts, Table
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
import json
from . import forms
import requests
from urllib.parse import urlencode
from guest_user.decorators import allow_guest_user

# Create your views here.
main_context = {
    "categories": Category.objects.all(),
    "salads": Salad.objects.all(),
    "all_day_snacks": AllDaySnacks.objects.all(),
    "main_dishes": MainDishes.objects.all(),
    "burgers": Burgers.objects.all(),
    "desserts": Desserts.objects.all(),
    "allergens": Allergens.objects.all()

}

def index(request):
    allergens = main_context["allergens"]
    allergens_dict = { str(allergen.id):allergen.allergen_name for allergen in allergens}
    categories = [cat for cat in main_context.keys()]
    for cat in categories:
        if cat not in ('categories', 'allergens'):
            category_object = main_context[cat]
            try:
                for item in category_object:
                    allergens_temp = [allergens_dict[allergie] for allergie in item.allergies.split(",")]
                    item.allergies = allergens_temp
            except (AttributeError, KeyError) as e:
                print("Error:", cat, e)
            main_context[cat] = category_object
    # salads = Salad.objects.all()
    # for salad in salads:
    #     allergens_temp = [allergens_dict[allergie] for allergie in salad.allergies.split(",")]
    #     salad.allergies = ", ".join(allergens_temp)
    # main_context['salads'] = salads
    return render(request, "orders/home.html", main_context)
    # if request.user.is_authenticated:
    #     #we are passing in the data from the category model
    #     return render(request, "orders/home.html", {"categories":Category.objects.all})
    # else:
    #     return redirect("orders:login")

@allow_guest_user
def hello_guest(request):
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

def pizza(request):
    if request.user.is_authenticated:
        return render(request, "orders/pizza.html", context = {"regular_pizza":RegularPizza.objects.all, "sicillian_pizza":SicilianPizza.objects.all , "toppings":Toppings.objects.all, "number_of_toppings":3})
    else:
        return redirect("orders:login")

def pasta(request):
    if request.user.is_authenticated:
        return render(request, "orders/pasta.html", context = {"dishes":Pasta.objects.all})
    else:
        return redirect("orders:login")


def salad(request):
    salads = Salad.objects.all()
    allergens = Allergens.objects.all()
    allergens_dict = {}
    for salad in salads:
        allergies_list = salad.allergies.split(",")
        salad_allergens = []
        for i in allergies_list:
            salad_allergens.append(allergens.get(id=i).allergen_name)
        allergens_dict[salad.dish_name] = salad_allergens

    print(allergens_dict)
    return render(request, "orders/salad.html", context={"dishes": Salad.objects.all, "allergies": allergens_dict})
    # if request.user.is_authenticated:
    #     return render(request, "orders/salad.html", context = {"dishes":Salad.objects.all, "allergies":allergens_dict})
    # else:
    #     return redirect("orders:login")


def subs(request):
    if request.user.is_authenticated:
        return render(request, "orders/sub.html", context = {"dishes":Sub.objects.all})
    else:
        return redirect("orders:login")


def dinner_platters(request):
    if request.user.is_authenticated:
        return render(request, "orders/dinner_platters.html", context = {"dishes":DinnerPlatters.objects.all})
    else:
        return redirect("orders:login")

def all_day_snacks(request):
    if request.user.is_authenticated:
        return render(request, "orders/salad.html", context = {"dishes":AllDaySnacks.objects.all})
    else:
        return redirect("orders:login")

def directions(request):
    # if request.user.is_authenticated:
    return render(request, "orders/directions.html")
    # else:
    #     return redirect("orders:login")

def hours(request):
    # if request.user.is_authenticated:
    return render(request, "orders/hours.html")
    # else:
    #     return redirect("orders:login")

def contact(request):
    # if request.user.is_authenticated:
    return render(request, "orders/contact.html")
    # else:
    #     return redirect("orders:login")

def cart(request):

    tables = Table.objects.all()
    if request.user.is_authenticated:
        context = {'tables': tables}
        return render(request, "orders/cart.html", context)
    else:
        return redirect("orders:login")

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

        order = UserOrder(username=username, order=list_of_items, price=float(price), table_number=table_num, delivered=False) #create the row entry
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

def order_success(request):
    order = UserOrder.objects.filter(username=request.user.username).order_by('-time_of_order')[0]
    return render(request, "orders/order_received.html", context={"order": order})

@login_required(login_url='orders:login')
def view_orders(request):
    if request.user.is_superuser or request.user.is_staff:
        #make a request for all the orders in the database
        rows = UserOrder.objects.all().order_by('-time_of_order')
        #orders.append(row.order[1:-1].split(","))
        pending_orders = 0
        for row in rows:
            if not row.delivered:
                pending_orders+=1
        return render(request, "orders/orders.html", context = {"rows":rows, "pending_orders":pending_orders})
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

def save_cart(request):
    if request.method == 'POST':
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

# def session_expired(request):
#     return render(request, "orders/session_expired.html", {})
