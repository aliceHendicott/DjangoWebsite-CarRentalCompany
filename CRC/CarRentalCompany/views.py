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


# Create your views here #
# ---------------------- #


# ------- GENERAL ------ #
'''
' SPRINT 1
' The following are sprint 1:
'''
def index(request):
    form = RecommendForm()
    if request.method == "POST":
        # pull data from form if filled out
        purpose = request.POST['purpose']
        seats = request.POST['seats']
        transmission = request.POST['transmission']
        month = request.POST['month']
        recommended_cars = handle_recommendation(purpose, seats, transmission, month)
        num_results = len(list(recommended_cars))
        no_results = False
        if num_results == 0:
            no_results = True
        form_actioned = True
        return redirect("car_recommend",
                        {'form': form,
                         'recommended_cars': recommended_cars,
                         'no_results': no_results,
                         'form_actioned': form_actioned})
    top_3_cars = top3cars()
    return render(request,
                  'CarRentalCompany/home.html',
                  {'car_list': Car.objects.all(),
                   'store_list': Store.objects.all(),
                   'form': form,
                   'top_3_cars': top_3_cars})


'''
' LOGIN FUNCTIONS
'''

def logout_view(request):
    logout(request)
    return redirect("index")


def handle_login(request):
    if request.method == "POST":
        # handle login as JSON
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        a = login(request, user)

        if (user.is_authenticated):
            return JsonResponse({'response': '200'})
        else:
            return JsonResponse({'response': '403'})

    return JsonResponse({'response': '500'})



'''
' SPRINT 2
' The following are sprint 2:
'''
def FAQ(request):
    return render(request,
                  'CarRentalCompany/faq.html',
                  {'store_list': Store.objects.all()})
def register(request):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})



# ------ CUSTOMERS ----- #
'''
' SPRINT 1
' The following are sprint 1:
'''
pass

'''
' SPRINT 2
' The following are sprint 2:
'''
def my_account(request):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})



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
def staff_orders(request):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})
def staff_order(request, order_id):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})
def staff_customers(request):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})
def staff_customer(request, customer_id):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})



# -------- CARS -------- #
'''
' SPRINT 1
' The following are sprint 1:
'''
def cars(request):
    return render(request,
                  'CarRentalCompany/cars.html',
                  {'cars_list': Car.objects.all()})

def car_recommend(request):
    form = RecommendForm()
    recommended_cars = []
    no_results = False
    form_actioned = False
    if request.method == "POST":
        # pull data from form if filled out
        purpose = request.POST['purpose']
        seats = request.POST['seats']
        transmission = request.POST['transmission']
        month = request.POST['month']
        recommended_cars = handle_recommendation(purpose, seats, transmission, month)
        num_results = len(list(recommended_cars))
        if num_results == 0:
            no_results = True
        form_actioned = True
    return render(request,
                  'CarRentalCompany/car_recommend.html',
                  {'form': form,
                   'recommended_cars': recommended_cars,
                   'no_results': no_results,
                   'form_actioned': form_actioned})

'''
' SPRINT 2
' The following are sprint 2:
'''
def car(request, car_id):
    car = Car.objects.get(pk = car_id)
    return render(request,
                  'CarRentalCompany/car.html',
                  {'car': car})
def car_request(request, car_id):
    car = Car.objects.get(pk = car_id)
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})



# ------- STORES -------- #
'''
' SPRINT 1
' The following are sprint 1:
'''
pass

'''
' SPRINT 2
' The following are sprint 2:
'''
def stores(request):
    return render(request,
                  'CarRentalCompany/stores.html',
                  {'stores_list': Store.objects.all()})

def store(request, store_id):
    store = Store.objects.get(pk = store_id)
    return render(request,
                  'CarRentalCompany/store.html',
                  {'store': store})


# ------- REPORTS ------ #
'''
' SPRINT 1
' The following are sprint 1:
'''


@login_required
def reports_dashboard(request):
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

def reports_cars_seasonal(request):
    return render(request,
                  'CarRentalCompany/reports_cars_seasonal.html',
                  {'cars_list': Car.objects.all()})
def reports_cars_inactive(request):
    return render(request,
                  'CarRentalCompany/reports_cars_inactive.html',
                  {'cars_list': Car.objects.all()})
def reports_store_activity(request):
    locations = []
    for store in Store.objects.all():
        locations.append([eval(store.store_latitude), eval(store.store_longitude), store.store_name])
    testGraph()
    testGraph1()
    testGraph2()
    return render(request,
                  'CarRentalCompany/reports_store_activity.html',
                  {'stores_list': Store.objects.all(),
                   'location_maps' : locations})
def reports_store_parking(request):
    return render(request,
                  'CarRentalCompany/reports_store_parking.html',
                  {'stores_list': Store.objects.all()})
def reports_customer_demographics(request):
    return render(request,
                  'CarRentalCompany/reports_customer_demographics.html',
                  {'users_list': User.objects.all()})

'''
' SPRINT 2
' The following are sprint 2:
'''
def reports_custom(request):
    return render(request,
                  'CarRentalCompany/xxx.html',
                  {})