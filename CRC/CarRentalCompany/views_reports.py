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
def cars_seasonal_graph():
    pass
def cars_inactive_graph():
    pass
def store_parking_graph():
    pass
def store_activity_graph():
    pass
def cars_seasonal_graph():
    pass


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
            seasonal_cars = seasonal_cars_preview()
            store_activity = store_activity_preview()
            return render(request,
                          'CarRentalCompany/reports_dashboard.html',
                          {'seasonal_cars': seasonal_cars,
                           'store_activity': store_activity})
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
            drawGraph('bar', 'cars_seasonal', 1)
            return render(request,
                          'CarRentalCompany/reports_cars_seasonal.html',
                          {'cars_list': Car.objects.all()})
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
            drawGraph('horizBar', 'cars_inactive', 1)
            return render(request,
                          'CarRentalCompany/reports_cars_inactive.html',
                          {'cars_list': Car.objects.all()})
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
            drawGraph('pie', 'store_activity', 1)
            locations = []
            for store in Store.objects.all():
                locations.append([eval(store.store_latitude), eval(store.store_longitude), store.store_name])
            return render(request,
                          'CarRentalCompany/reports_store_activity.html',
                          {'stores_list': Store.objects.all(),
                           'location_maps': locations})
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
            drawGraph('horizBar', 'store_parking', 1)
            results = store_parking_query()
            return render(request,
                          'CarRentalCompany/reports_store_parking.html',
                          {'queried_stores': results,
                           'stores': Store.objects.all()})
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
                           'results': results})
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