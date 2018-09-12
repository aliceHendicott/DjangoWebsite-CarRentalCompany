from django.shortcuts import HttpResponse, render
from django.template import loader

from .models import Car, Store, Order, User


# Create your views here #
# ---------------------- #


# ------- GENERAL ------ #
'''
' SPRINT 1
' The following are sprint 1:
'''
def index(request):
    return render(request,
                  'CarRentalCompany/home.html',
                  {'car_list': Car.objects.all(),
                   'store_list' : Store.objects.all()})
def login(request):
    return render(request,
                  'CarRentalCompany/login.html',
                  {})

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
    return render(request,
                  'CarRentalCompany/car_recommend.html',
                  {'cars_list': Car.objects.all()})
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
def reports_dashboard(request):
    return render(request,
                  'CarRentalCompany/reports_dashboard.html',
                  {'cars_list': Car.objects.all(),
                   'stores_list': Store.objects.all(),
                   'users_list': User.objects.all()})
def reports_cars_seasonal(request):
    return render(request,
                  'CarRentalCompany/reports_cars_seasonal.html',
                  {'cars_list': Car.objects.all()})
def reports_cars_inactive(request):
    return render(request,
                  'CarRentalCompany/reports_cars_inactive.html',
                  {'cars_list': Car.objects.all()})
def reports_store_activity(request):
    return render(request,
                  'CarRentalCompany/reports_store_activity.html',
                  {'stores_list': Store.objects.all()})
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


# -------- TEST -------- #
