from django.shortcuts import HttpResponse, render, redirect, reverse
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection

from .graphs import *
from .models import Car, Store, Order, User, UserProfile
from .forms import RecommendForm
from .custom_sql import top3cars, seasonal_cars_preview, store_activity_preview, store_parking_query
from .recommendation import handle_recommendation
from django.contrib.auth import (authenticate, login, get_user_model, logout)


# ------- REPORTS ------ #

## Supporting
def cars_seasonal_graph():
    graphdata = [['Fibonaccia', 11],
                 ['Fibonaccib', 12],
                 ['Fibonaccic', 13],
                 ['Fibonaccid', 14],
                 ['Fibonaccie', 15],
                 ['Fibonaccif', 16]]
    drawGraph('bar', 'cars_seasonal', graphdata)

def cars_inactive_graph():
    graphdata = [['Fibonaccia', 11],
                 ['Fibonaccib', 12],
                 ['Fibonaccic', 13],
                 ['Fibonaccid', 14],
                 ['Fibonaccie', 15],
                 ['Fibonaccif', 16]]
    drawGraph('horizBar', 'cars_inactive', graphdata)

def store_parking_graph():
    graphdata = [['Fibonaccia', 11],
                 ['Fibonaccib', 12],
                 ['Fibonaccic', 13],
                 ['Fibonaccid', 14],
                 ['Fibonaccie', 15],
                 ['Fibonaccif', 16]]
    drawGraph('horizBar', 'store_parking', graphdata)

def store_activity_graph():
    graphdata = [['Fibonaccia', 11],
                 ['Fibonaccib', 12],
                 ['Fibonaccic', 13],
                 ['Fibonaccid', 14],
                 ['Fibonaccie', 15],
                 ['Fibonaccif', 16]]
    drawGraph('pie', 'store_activity', graphdata)



'''
' SPRINT 1
' The following are sprint 1:
'''

@login_required
def dashboard(request):
    cars_seasonal_graph()
    cars_inactive_graph()
    store_parking_graph()
    store_activity_graph()
    user_profile = request.user.userprofile
    customer = user_profile.is_customer
    floor_staff = user_profile.is_floorStaff
    if not customer and not floor_staff:
        seasonal_cars = seasonal_cars_preview()
        store_activity = store_activity_preview()
        return render(request,
                      'CarRentalCompany/reports_dashboard.html',
                      {'seasonal_cars': seasonal_cars,
                       'store_activity': store_activity})
    else:
        return redirect('index')
def cars_seasonal(request):
    cars_seasonal_graph();
    return render(request,
                  'CarRentalCompany/reports_cars_seasonal.html',
                  {'cars_list': Car.objects.all()})
def cars_inactive(request):
    cars_inactive_graph()
    return render(request,
                  'CarRentalCompany/reports_cars_inactive.html',
                  {'cars_list': Car.objects.all()})
def store_activity(request):
    store_activity_graph()
    locations = []
    for store in Store.objects.all():
        locations.append([eval(store.store_latitude), eval(store.store_longitude), store.store_name])
    return render(request,
                  'CarRentalCompany/reports_store_activity.html',
                  {'stores_list': Store.objects.all(),
                   'location_maps' : locations})

def store_parking(request):
    store_parking_graph();
    results = store_parking_query()
    return render(request,
                  'CarRentalCompany/reports_store_parking.html',
                  {'queried_stores': results,
                   'stores': Store.objects.all()})

def customer_demographics(request):
    return render(request,
                  'CarRentalCompany/reports_customer_demographics.html',
                  {'users_list': User.objects.all()})

'''
' SPRINT 2
' The following are sprint 2:
'''
def custom(request):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})