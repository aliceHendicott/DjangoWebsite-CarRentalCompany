from django.shortcuts import HttpResponse, render, redirect, reverse
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection

from .graphs import *
from .models import Car, Store, Order, User as modelUser
from .forms import *
from .customer_search import *
from .custom_sql import top3cars, seasonal_cars_preview, store_activity_preview
from .recommendation import handle_recommendation
from django.contrib.auth import (authenticate, login, get_user_model, logout)


# -------- STAFF ------- #
'''
' SPRINT 1
' The following are sprint 1:
'''
pass

'''
' SPRINT 2
' The following are sprint 2:
'''
def staff(request):
    return render(request, 'CarRentalCompany/data.html', {})

def orders(request):
    orders = []
    for order in Order.objects.all():
        new_order = {}
        car_info = Car.objects.get(pk=order.car_id_id)
        car_make_model = car_info.car_model + " " + car_info.car_makename
        car_id = car_info.id
        pickup_store_info = Store.objects.get(id=order.order_pickup_store_id_id)
        pickup_store = pickup_store_info.store_city
        pickup_store_id = pickup_store_info.id
        return_store_info = Store.objects.get(pk=order.order_return_store_id_id)
        return_store = return_store_info.store_city
        return_store_id = return_store_info.id
        customer_info = modelUser.objects.get(pk=order.customer_id_id)
        customer_name = customer_info.user_name
        customer_phone = customer_info.user_phone
        customer_id = customer_info.id
        new_order.update({'id': order.id,
                          'pickup_date': order.order_pickup_date,
                          'return_date': order.order_return_date,
                          'car_make_model': car_make_model,
                          'car_id': car_id,
                          'return_store': return_store,
                          'return_store_id': return_store_id,
                          'pickup_store': pickup_store,
                          'pickup_store_id': pickup_store_id,
                          'customer_name': customer_name,
                          'customer_phone': customer_phone,
                          'customer_id': customer_id})
        orders.append(new_order)
    return render(request,
                  'CarRentalCompany/orders.html',
                  {'orders_list': orders,
                   'cars': Car.objects.all()})
def order(request, order_id):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})

def customers(request):
    form = CustomerSearchForm
    customers_list = modelUser.objects.all()
    customers_list_searched = ""
    if request.method == "POST":
        fields = request.POST
        customers_list_searched = handle_customer_search(fields)
    return render(request,
                  'CarRentalCompany/customers.html',
                  {'form': form,
                   'customers_list': customers_list,
                   'customers_list_searched': customers_list_searched})

def customer(request, customer_id):
    customer = modelUser.objects.get(pk=customer_id)
    form = UpdateCustomerDetailsForm(request.POST or None, instance=customer,
                                     initial={'user_address': customer.user_address,
                                              'user_birthday': customer.user_birthday,
                                              'user_gender': customer.user_gender,
                                              'user_name': customer.user_name,
                                              'user_occupation': customer.user_occupation,
                                              'user_phone': customer.user_phone})
    if form.is_valid():
        form.save()
        return redirect('/staff/customers/')
    else:
        return render(request,
                      'CarRentalCompany/customer_update.html',
                      {'customer': customer,
                       'form': form,
                       'customer_id': customer_id})
