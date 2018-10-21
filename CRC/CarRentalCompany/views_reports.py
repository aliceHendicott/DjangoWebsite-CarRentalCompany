from django.db import connection
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import HttpResponse, render, redirect, reverse
from django.contrib.auth import (authenticate, login, get_user_model, logout)
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .forms import RecommendForm
from .graphs import *
from .models import Car, Store, Order, User, UserProfile
from .custom_sql import *
from .recommendation import handle_recommendation


# ------- REPORTS ------ #

## Supporting
# Authentication
def is_management(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        customer = user_profile.is_customer
        floor_staff = user_profile.is_floorStaff
        if not customer and not floor_staff:
           return True
    return False

# Graphs
def cars_seasonal_graph(data):
    graphdata = []
    for car in data:
        graphdata.append([car.car_makename, car.number_of_orders])
    return drawGraph('bar', 'cars_seasonal', graphdata)
def cars_inactive_graph(data = 0):
    graphdata = []
    for car in data:
        graphdata.append([car.car_makename, (date.today() - car.Return_Date).days])
    return drawGraph('horizBar', 'cars_inactive', graphdata)
def store_parking_graph(data = 0):
    graphdata = []
    for store in data:
        graphdata.append([store.store_city.replace(" ", ""), store.picked_up])
    return drawGraph('horizBar', 'store_parking', graphdata)
def store_activity_graph(data):
    graphdata = []
    for store in data:
        graphdata.append([store.store_city, store.total_activity])
    return drawGraph('pie', 'store_activity', graphdata)
def customer_demographics_graph(data=0):
    graphdata = []
    for demographic in data:
        graphdata.append([demographic[2], demographic[0]])
    return drawGraph('pie', 'customer_demographics', graphdata)


'''
' SPRINT 1
' The following are sprint 1:
'''
##### Reports Dashboard #####
def dashboard_context(dates = 1, limit = 5):
    seasonal_cars = Car.top_cars(limit)
    car_inactive = Car.inactive_cars(limit)
    store_activity = Store.store_activity(limit)
    store_parks = Store.store_parking(limit)
    customer_demographics = User.user_demographics(limit)
    context =  {'seasonal_cars': seasonal_cars,
                'store_activity': store_activity,
                'cars_seasonal_graph': cars_seasonal_graph(seasonal_cars),
                'cars_inactive_graph': cars_inactive_graph(car_inactive),
                'store_parking_graph': store_parking_graph(store_parks),
                'store_activity_graph': store_activity_graph(store_activity),
                'customer_demographics_graph': customer_demographics_graph(customer_demographics)}
    return context
def json_dashboard_context(request):
    dates = (request.GET.get('start_date', None), request.GET.get('end_date', None))
    data_rendered = {
        'html_response': render_to_string("CarRentalCompany/Includes/reports_dashboard_content.html", dashboard_context(dates=dates, limit=10))
    }
    return JsonResponse(data_rendered)
def dashboard(request):
    if is_management(request):
        return render(request,
                      'CarRentalCompany/reports_dashboard.html',
                      dashboard_context())
    return redirect('index')


##### Seasonal Cars Report #####
def cars_seasonal_context(dates=(1,2), limit = 5):
    seasonal_cars_results = seasonal_cars()
    context =  {'cars_list': Car.objects.all(),
                'seasonal_cars':  seasonal_cars_results,
                'cars_seasonal_graph': cars_seasonal_graph(seasonal_cars_results)}
    return context
def json_cars_seasonal_context(request):
    dates = (request.GET.get('start_date', None), request.GET.get('end_date', None))
    data_rendered = {
        'html_response': render_to_string("CarRentalCompany/Includes/reports_cars_seasonal_content.html", cars_seasonal_context(dates))
    }
    return JsonResponse(data_rendered)
def cars_seasonal(request):
    if is_management(request):
        return render(request,
                      'CarRentalCompany/reports_cars_seasonal.html',
                      cars_seasonal_context())
    return redirect('index')


##### Inactive Cars Report #####
def cars_inactive_context(dates=(1,2), limit = 5):
    car_inactive = Car.inactive_cars()
    inactive_car_results = Car.inactive_cars()
    context =  {'cars_list': Car.objects.all(),
                'inactive_cars': car_inactive,
                'cars_inactive_graph': cars_inactive_graph(car_inactive)}
    return context
def json_cars_inactive_context(request):
    dates = (request.GET.get('start_date', None), request.GET.get('end_date', None))
    data_rendered = {
        'html_response': render_to_string("CarRentalCompany/Includes/reports_cars_inactive_content.html", cars_inactive_context(dates))
    }
    return JsonResponse(data_rendered)
def cars_inactive(request):
    if is_management(request):
        return render(request,
                      'CarRentalCompany/reports_cars_inactive.html',
                      cars_inactive_context())
    return redirect('index')


##### Store Activity Report #####
def store_activity_context(dates=(1,2), limit = 5):
    locations = []
    for store in Store.objects.all():
        locations.append([eval(store.store_latitude), eval(store.store_longitude), store.store_name])
    store_results = Store.store_activity()
    context =  {'stores_list': Store.objects.all(),
                'location_maps': locations,
                'store_results': store_results,
                'store_activity_graph': store_activity_graph(store_results)}
    return context
def json_store_activity_context(request):
    dates = (request.GET.get('start_date', None), request.GET.get('end_date', None))
    data_rendered = {
        'html_response': render_to_string("CarRentalCompany/Includes/reports_store_activity_content.html", store_activity_context(dates))
    }
    return JsonResponse(data_rendered)
def store_activity(request):
    if is_management(request):
        return render(request,
                      'CarRentalCompany/reports_store_activity.html',
                      store_activity_context())
    return redirect('index')


##### Store Parking Report #####
def store_parking_context(dates=(1,2), limit = 5):
    results = Store.store_parking()
    context =  {'queried_stores': results,
                'stores': Store.objects.all(),
                'store_parking_graph': store_parking_graph(results)}
    return context
def json_store_parking_context(request):
    dates = (request.GET.get('start_date', None), request.GET.get('end_date', None))
    data_rendered = {
        'html_response': render_to_string("CarRentalCompany/Includes/reports_store_parking_content.html", store_parking_context(dates))
    }
    return JsonResponse(data_rendered)
def store_parking(request):
    if is_management(request):
        return render(request,
                      'CarRentalCompany/reports_store_parking.html',
                      store_parking_context())
    return redirect('index')


##### Customer Demographics Report #####
def customer_demographics_context(dates=(1,2), limit = 5):
    results = User.user_demographics()
    context =  {'users_list': User.objects.all(),
                'results': results,
                'customer_demographics_graph': customer_demographics_graph(results)}
    return context
def json_customer_demographics_context(request):
    dates = (request.GET.get('start_date', None), request.GET.get('end_date', None))
    data_rendered = {
        'html_response': render_to_string("CarRentalCompany/Includes/reports_customer_demographics_content.html", customer_demographics_context(dates))
    }
    return JsonResponse(data_rendered)
def customer_demographics(request):
    if is_management(request):
        results = customer_demographics_query()
        return render(request,
                      'CarRentalCompany/reports_customer_demographics.html',
                      customer_demographics_context())
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