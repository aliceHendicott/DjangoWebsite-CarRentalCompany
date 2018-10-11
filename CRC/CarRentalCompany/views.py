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
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomerRegisterForm(request.POST)
            if form.is_valid():
                user_new = form.save()
                user_new.refresh_from_db()  # load the profile instance created by the signal
                user_new.userprofile.customer_number = form.cleaned_data.get('customer_number')
                user_new.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user_new.username, password=raw_password)
                login(request, user)
                return redirect('index')
            else:
                return render(request,
                              'CarRentalCompany/register.html',
                              {'form': form})
        else:
            form = CustomerRegisterForm()
            return render(request,
                          'CarRentalCompany/register.html',
                          {'form': form})
    else:
        return redirect('index')

# Tutorial on AJAX
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

class SignUpView(CreateView):
    template_name = 'CarRentalCompany/signup.html'
    form_class = UserCreationForm

from django.http import JsonResponse

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Car.objects.filter(car_makename__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)