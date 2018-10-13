from django.shortcuts import HttpResponse, render, redirect, reverse
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection

from .graphs import *
from .models import Car, Store, Order, User, UserProfile
from .forms import *
from .custom_sql import top3cars, seasonal_cars_preview, store_activity_preview
from .recommendation import handle_recommendation
from .filter_cars import *
from django.contrib.auth import (authenticate, login, get_user_model, logout)
from django.core import serializers

# -------- CARS -------- #
'''
' SPRINT 1
' The following are sprint 1:
'''
def cars(request):
    form = CarFilterForm()
    filtered_cars = ""
    filters = ["Sort by: Make (A-Z)"]
    # check if the car filter form has been submitted
    if request.method == "GET":
        # pull the values posted into a python dictionary
        fields = request.GET
        # pull list of cars based on these filters
        filtered_cars = handle_filter_cars(fields)
        # pull list of filters used if the filters returned values
        if filtered_cars != -1 and filtered_cars != -2:
            filters = get_current_filter(fields)
    #render cars.html passing all relevant variables
    return render(request,
                  'CarRentalCompany/cars.html',
                  {'cars_list': Car.objects.order_by('car_makename'),
                   'form': form,
                   'filtered_cars': filtered_cars,
                   'filters': filters})

def car_recommend(request):
    recommendation_form = RecommendForm()
    feedback_form = RecommendationFeedbackForm()
    recommended_cars = []
    no_results = False
    form_actioned = False
    feedback_given = False
    if request.method == "POST" and 'purpose' in request.POST:
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
    if request.method == "POST" and 'helpful' in request.POST:
        helpful = request.POST['helpful']
        comment = request.POST['comment']
        feedback_given = True
    return render(request,
                  'CarRentalCompany/car_recommend.html',
                  {'recommendation_form': recommendation_form,
                   'recommended_cars': recommended_cars,
                   'no_results': no_results,
                   'form_actioned': form_actioned,
                   'feedback_form': feedback_form,
                   'feedback_given': feedback_given})

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



