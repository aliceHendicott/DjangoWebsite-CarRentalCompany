from django.shortcuts import HttpResponse, render, redirect, reverse
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection

from .graphs import *
from .models import Car, Store, Order, User, UserProfile
from .forms import RecommendForm
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
    return render(request,
                  'CarRentalCompany/orders.html',
                  {'orders_list': Order.objects.all()})
def order(request, order_id):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})

def customers(request):
    return render(request,
                  'CarRentalCompany/customers.html',
                  {'customers_list': User.objects.all()})

def customer(request, customer_id):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})
