from django.shortcuts import HttpResponse, render, redirect, reverse
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection

from .graphs import *
from .models import Car, Store, Order, User, UserProfile
from .forms import RecommendForm
from .custom_sql import *
from .recommendation import handle_recommendation
from django.contrib.auth import (authenticate, login, get_user_model, logout)


# ------- REPORTS ------ #

## Supporting
def cars_seasonal_graph(data):
    graphdata = []
    for car in data:
        graphdata.append([car.car_makename, car.number_of_orders])
    return drawGraph('bar', 'cars_seasonal', graphdata)

def cars_inactive_graph():
    graphdata = [['VW Golf', 5],
                 ['Getz', 12],
                 ['Falcon', 13],
                 ['Vento', 14],
                 ['Lotus x', 15],
                 ['Tesla', 16]]
    return drawGraph('horizBar', 'cars_inactive', graphdata)

def store_parking_graph():
    graphdata = [['Brisbane', 16],
                 ['Warrnambool', 15],
                 ['Sydney', 14],
                 ['Gold Coast', 13],
                 ['Adelaide', 5]]
    return drawGraph('horizBar', 'store_parking', graphdata)

def store_activity_graph(data):
    graphdata = []
    for store in data:
        graphdata.append([store.store_city, store.total_activity])
    return drawGraph('pie', 'store_activity', graphdata)

def customer_demographics_graph():
    graphdata = [['Female 18-25', 1],
                 ['Male 35-45', 3],
                 ['Male 18-25', 6],
                 ['Female 65+', 2],
                 ['Female 35-45', 9]]
    return drawGraph('pie', 'customer_demographics', graphdata)


'''
' SPRINT 1
' The following are sprint 1:
'''

def dashboard(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        customer = user_profile.is_customer
        floor_staff = user_profile.is_floorStaff
        if not customer and not floor_staff:
            seasonal_cars = Car.top_cars(5)
            store_activity = Store.store_activity(5)
            car_parks = Car.inactive_cars()
            return render(request,
                          'CarRentalCompany/reports_dashboard.html',
                          {'seasonal_cars': seasonal_cars,
                           'store_activity': store_activity,
                           'cars_seasonal_graph': cars_seasonal_graph(seasonal_cars),
                           'cars_inactive_graph': cars_inactive_graph(),
                           'store_parking_graph': store_parking_graph(),
                           'store_activity_graph': store_activity_graph(store_activity),
                           'customer_demographics_graph': customer_demographics_graph()})
        else:
            return redirect('index')
    else:
        return redirect('index')

def cars_seasonal(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        customer = user_profile.is_customer
        floor_staff = user_profile.is_floorStaff
        if not customer and not floor_staff:
            seasonal_cars_results = seasonal_cars()
            return render(request,
                          'CarRentalCompany/reports_cars_seasonal.html',
                          {'cars_list': Car.objects.all(),
                           'seasonal_cars':  seasonal_cars_results,
                           'cars_seasonal_graph': cars_seasonal_graph()})
        else:
            return redirect('index')
    else:
        return redirect('index')

def cars_inactive(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        customer = user_profile.is_customer
        floor_staff = user_profile.is_floorStaff
        if not customer and not floor_staff:
            inactive_car_results = inactive_cars()
            return render(request,
                          'CarRentalCompany/reports_cars_inactive.html',
                          {'cars_list': Car.objects.all(),
                           'inactive_cars': inactive_car_results,
                           'cars_inactive_graph': cars_inactive_graph()})
        else:
            return redirect('index')
    else:
        return redirect('index')

def store_activity(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        customer = user_profile.is_customer
        floor_staff = user_profile.is_floorStaff
        if not customer and not floor_staff:
            locations = []
            for store in Store.objects.all():
                locations.append([eval(store.store_latitude), eval(store.store_longitude), store.store_name])
            store_results = store_activity_query()
            return render(request,
                          'CarRentalCompany/reports_store_activity.html',
                          {'stores_list': Store.objects.all(),
                           'location_maps': locations,
                           'store_results': store_results,
                           'store_activity_graph': store_activity_graph()})
        else:
            return redirect('index')
    else:
        return redirect('index')

def store_parking(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        customer = user_profile.is_customer
        floor_staff = user_profile.is_floorStaff
        if not customer and not floor_staff:
            results = store_parking_query()
            return render(request,
                          'CarRentalCompany/reports_store_parking.html',
                          {'queried_stores': results,
                           'stores': Store.objects.all(),
                           'store_parking_graph': store_parking_graph()})
        else:
            return redirect('index')
    else:
        return redirect('index')

def customer_demographics(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        customer = user_profile.is_customer
        floor_staff = user_profile.is_floorStaff
        if not customer and not floor_staff:
            results = customer_demographics_query()
            return render(request,
                          'CarRentalCompany/reports_customer_demographics.html',
                          {'users_list': User.objects.all(),
                           'results': results,
                           'customer_demographics_graph': customer_demographics_graph()})
        else:
            return redirect('index')
    else:
        return redirect('index')

'''
' SPRINT 2
' The following are sprint 2:
'''
def custom(request):
    if request.user.is_authenticated:
        return render(request,
                      'CarRentalCompany/xxx.html',
                      {})
    else:
        return redirect('index')