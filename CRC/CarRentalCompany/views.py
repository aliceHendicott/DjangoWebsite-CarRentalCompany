from django.shortcuts import HttpResponse, render
from django.template import loader

from .models import Car, Store, Order

# Create your views here #
# ---------------------- #


# ------- GENERAL ------ #
def index(request):
    return render(request,
                  'CarRentalCompany/home.html',
                  {'car_list': Car.objects.all(),
                   'store_list' : Store.objects.all()})
def login(request):
    return HttpResponse("Login")
def register(request):
    return HttpResponse("Register")


# ------ CUSTOMERS ----- #
def my_account(request):
    return HttpResponse("My Account")


# -------- STAFF ------- #
def staff_orders(request):
    return HttpResponse("Orders:")
def staff_order(request, order_id):
    return HttpResponse("Order:")
def staff_customers(request):
    return HttpResponse("Customers:")
def staff_customer(request, customer_id):
    return HttpResponse("Customer:")


# -------- CARS -------- #
def cars(request):
    return render(request,
                  'CarRentalCompany/cars.html',
                  {'cars_list': Car.objects.all()})
def car(request, car_id):
    car = Car.objects.get(pk = car_id)
    return render(request,
                  'CarRentalCompany/car.html',
                  {'car': car})
def car_request(request, car_id):
    car = Car.objects.get(pk = car_id)
    return HttpResponse("<b>REQUEST CAR:</b> <br>{0}<br>{1}".format(car.car_name, car.car_bodytype))
def car_recommend(request):
    return HttpResponse("<b>RECOMMENDATIONS:</b>")


# ------- STORES -------- #
def stores(request):
    return render(request,
                  'CarRentalCompany/stores.html',
                  {'store_list': Store.objects.all()})
def store(request, store_id):
    store = Store.objects.get(pk = store_id)
    return render(request,
                  'CarRentalCompany/store.html',
                  {'store': store})


# ------- REPORTS ------ #
def reports_dashboard(request):
    return HttpResponse("<b>REPORTS DASH:</b>")
def reports_cars_seasonal(request):
    return HttpResponse("<b>SEASONAL CARS:</b>")
def reports_cars_inactive(request):
    return HttpResponse("<b>INACTIVE CARS:</b>")
def reports_store_activity(request):
    return HttpResponse("<b>STORE ACTIVIY:</b>")
def reports_store_parking(request):
    return HttpResponse("<b>STORE PARKING:</b>")
def reports_customer_demographics(request):
    return HttpResponse("<b>CUSTOMER DEMOGRAPHICS:</b>")


# --------- FAQ -------- #
def FAQ(request):
    return render(request,
                  'CarRentalCompany/faq.html',
                  {'store_list': Store.objects.all()})

# -------- TEST -------- #
import random
import datetime
import time

#from graphos.sources.simple import SimpleDataSource
#   from graphos.renderers.gchart import LineChart

def TEST_PAGE(request):
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
    }
    return render(request, 'CarRentalCompany/test.html', data)