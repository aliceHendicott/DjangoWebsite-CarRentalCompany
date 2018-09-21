from django.shortcuts import HttpResponse, render, redirect, reverse
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection

from .graphs import *
from .models import Car, Store, Order, User, UserProfile
from .forms import RecommendForm,CarFilterForm
from .custom_sql import top3cars, seasonal_cars_preview, store_activity_preview
from .recommendation import handle_recommendation
from .filter_cars import *
from django.contrib.auth import (authenticate, login, get_user_model, logout)
from django.core import serializers


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


# -------- CARS -------- #
'''
' SPRINT 1
' The following are sprint 1:
'''
def cars(request):
    form = CarFilterForm()
    filtered_cars = ""
    filters = ""
    # check if the car filter form has been submitted
    if request.method == "POST":
        # pull the values posted into a python dictionary
        fields = request.POST
        # pull list of cars based on these filters
        filtered_cars = handle_filter_cars(fields)
        # pull list of filters used if the filters returned values
        if filtered_cars != -1:
            filters = get_current_filter(fields)
    if filtered_cars == "" or filtered_cars == -1 or filtered_cars == -2:
        cars_json = serializers.serialize("json", Car.objects.all())
    else:
        cars_json = serializers.serialize("json", filtered_cars)
    #render cars.html passing all relevant variables
    return render(request,
                  'CarRentalCompany/cars.html',
                  {'cars_list': Car.objects.all(),
                   'form': form,
                   'filtered_cars': filtered_cars,
                   'filters': filters,
                   'cars_json': cars_json})

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
