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
    if request.user.is_authenticated and request.user.userprofile.is_customer:
        user = request.user
        orders = Order.objects.all()
        orders = orders.filter(customer_id=user.userprofile.customer_number)
        user_details = User.objects.get(id=user.userprofile.customer_number)
        return render(request,
                      'CarRentalCompany/customer_account.html',
                      {'user': user,
                       'orders': orders,
                       'user_details': user_details})
    else:
        return redirect('index.html')
