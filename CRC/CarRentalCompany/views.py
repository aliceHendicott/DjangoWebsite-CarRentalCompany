from django.shortcuts import HttpResponse, render, redirect, reverse
from django.template import loader
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection

from .models import Car, Store, Order, User, UserProfile
from .forms import RecommendForm

from django.contrib.auth import (authenticate, login, get_user_model, logout)


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
        # set up SQL based on purpose field
        if purpose == "1":
            purpose_sql = "CarRentalCompany_car.car_drive='4WD'"
        if purpose == "2":
            purpose_sql = "CarRentalCompany_car.car_seating_capacity>4"
        if purpose == "3":
            purpose_sql = "CarRentalCompany_car.car_tank_capacity>=70"
        # set up SQL based on seats field
        if seats == "1":
            seats_sql = "CarRentalCompany_car.car_seating_capacity>=1"
        if seats == "2":
            seats_sql = "CarRentalCompany_car.car_seating_capacity>=3"
        if seats == "3":
            seats_sql = "CarRentalCompany_car.car_seating_capacity>=5"
        # set up SQL based on transmission field
        if transmission == "1":
            transmission_sql = "CarRentalCompany_car.car_standard_transmission LIKE '%%A%%'"
        if transmission == "2":
            transmission_sql = "CarRentalCompany_car.car_standard_transmission LIKE '%%M%%'"
        # set up SQL based on month field
        months_sql = ("MONTH(CarRentalCompany_order.order_create_date)=%s" % month)
        # set up SQL by joining all above SQL as where statements
        join1 = " "
        sql1 = ["SELECT CarRentalCompany_car.id, CarRentalCompany_car.car_bodytype, CarRentalCompany_car.car_makename, CarRentalCompany_car.car_seating_capacity, CarRentalCompany_car.car_standard_transmission, CarRentalCompany_car.car_drive FROM CarRentalCompany_car INNER JOIN CarRentalCompany_order ON CarRentalCompany_order.car_id_id = CarRentalCompany_car.id WHERE", purpose_sql]
        join1 = join1.join(sql1)
        join2 = " AND "
        sql2 = [join1, seats_sql, transmission_sql, months_sql]
        join2 = join2.join(sql2)
        join3 = " "
        sql3 = [join2, "LIMIT 3"]
        join3 = join3.join(sql3)
        # run SQL
        recommended_cars = Car.objects.raw(join3)
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
        return render(request,
                      'CarRentalCompany/reports_dashboard.html',
                      {'cars_list': Car.objects.all(),
                       'stores_list': Store.objects.all(),
                       'users_list': User.objects.all()})
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