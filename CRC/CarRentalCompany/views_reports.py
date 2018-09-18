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


# ------- REPORTS ------ #
'''
' SPRINT 1
' The following are sprint 1:
'''

@login_required
def dashboard(request):
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
    drawGraph('bar', 'cars_seasonal', 1)
    return render(request,
                  'CarRentalCompany/reports_cars_seasonal.html',
                  {'cars_list': Car.objects.all()})
def cars_inactive(request):
    drawGraph('horizBar', 'cars_inactive', 1)
    return render(request,
                  'CarRentalCompany/reports_cars_inactive.html',
                  {'cars_list': Car.objects.all()})
def store_activity(request):
    drawGraph('pie', 'store_activity', 1)
    locations = []
    for store in Store.objects.all():
        locations.append([eval(store.store_latitude), eval(store.store_longitude), store.store_name])
    return render(request,
                  'CarRentalCompany/reports_store_activity.html',
                  {'stores_list': Store.objects.all(),
                   'location_maps' : locations})
def store_parking(request):
    drawGraph('horizBar', 'store_parking', 1)
    return render(request,
                  'CarRentalCompany/reports_store_parking.html',
                  {'stores_list': Store.objects.all()})
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