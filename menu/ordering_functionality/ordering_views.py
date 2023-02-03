import logging
import json

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.exceptions import PermissionDenied

from guest_user.decorators import allow_guest_user

from ..models import *
from ..views import main_context
from ..apps import MenuConfig as Configuration
@allow_guest_user
def hello_guest(request):
    table = request.GET.get('table')
    tables = [str(table.table_number) for table in Table.objects.all()]
    try:
        if table in tables:
            request.session['table'] = int(table)
            request.session['username'] = f'Table {table}'
        else:
            logging.error(f'Table {table} does not exist')
    except (TypeError, ValueError):
        logging.error(f"Table << {table} >> is not valid")
    return redirect(f"{Configuration.name}:index")

@login_required(login_url='main:login')
def cart(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, "menu/cart.html", context)

def save_cart(request):
    if request.method == 'POST':
        if not request.user.is_superuser or not request.user.is_staff:
            if 'Guest' not in request.user.username:
                cart = request.POST.get('cart')
                saved_cart = SavedCarts(username=request.user.username, cart=cart)  # create the row entry
                saved_cart.save()  # save row entry in database
        return HttpResponse(
            json.dumps({"good": "boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def retrieve_saved_cart(request):
    try:
        saved_cart = SavedCarts.objects.get(username=request.user.username)
        return HttpResponse(saved_cart.cart)
    except:
        return HttpResponse('')

def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart'))
        price = request.POST.get('price_of_cart')
        table_num = request.POST.get('table_number')
        username = request.user.username
        response_data = {}
        list_of_items = [item["item_description"] for item in cart]
        list_of_comments = [item['comments'] for item in cart]

        order = UserOrder(username=username, order=list_of_items, comments=list_of_comments, price=float(price),
                          table_number=table_num, delivered=False)
        order.save()

        response_data['result'] = 'Order Recieved!'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required(login_url='main:login')
def order_success(request):
    try:
        order = UserOrder.objects.filter(username=request.user.username).order_by('-time_of_order')[0]
        order_list = [[item, comment] for item, comment in zip(order.order.strip('][').replace("'", "").split(', '),
                                                               order.comments.strip('][').replace("'", "").split(', '))]
        all_dishes_prices = {dish.dish_name: dish.price for dish in main_context["all_dishes"]}
        for dish in order_list:
            dish.append(all_dishes_prices[dish[0]])
    except KeyError as e:
        print(e)

    return render(request, "menu/order_received.html", context={"order": order, "order_list": order_list})

@login_required(login_url='main:login')
def view_orders(request):
    if request.user.is_superuser or request.user.is_staff:
        rows = UserOrder.objects.all().order_by('-time_of_order')
        for row in rows:
            order_list = row.order.strip('][').replace("'", "").split(', ')
            comment_list = row.comments.strip('][').replace("'", "").split(', ')
            row_temp = [item + f" ({comment})" if comment else item for item, comment in zip(order_list, comment_list)]
            row.orderlist = str(row_temp)
        return render(request, "menu/orders.html", context={"rows": rows})
    else:
        rows = UserOrder.objects.all().filter(username=request.user.username).order_by('-time_of_order')
        return render(request, "menu/orders.html", context={"rows": rows})

@login_required(login_url='main:login')
def update_orders(request):
    if request.method == "GET":
        if request.user.is_superuser or request.user.is_staff:
            rows = UserOrder.objects.all().order_by('-time_of_order')
            json_data = serializers.serialize("json", rows)
            return HttpResponse(json_data, content_type='application/json')
        else:
            raise PermissionDenied

@login_required(login_url='main:login')
def order_approved(request):
    if request.method == "GET":
        try:
            order = UserOrder.objects.filter(username=request.user.username).order_by('-time_of_order')[0]
            return HttpResponse(order.delivered)
        except KeyError as e:
            logging.error(e)

def mark_order_as_delivered(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        UserOrder.objects.filter(pk=id).update(delivered=True)
        return HttpResponse(
            json.dumps({"good": "boy"}),
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
            json.dumps({"good": "boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )