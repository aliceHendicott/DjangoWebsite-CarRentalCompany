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

# Stores page
def stores(request):
    # Get a list of all the stores and their locations
    locations = []
    for store in Store.objects.all():
        locations.append([eval(store.store_latitude), # latitude
                          eval(store.store_longitude),  # longitude
                          [store.store_name, store.id]]) # [name, id]
    # Pass the context to a render
    return render(request,
                  'CarRentalCompany/stores.html',
                  {'stores_list': Store.objects.all(),
                   'location_maps': locations})

def store(request, store_id):
    store = Store.objects.get(pk = store_id)

    locations = [[eval(store.store_latitude), eval(store.store_longitude), [store.store_name, store.id]]]
    return render(request,
                  'CarRentalCompany/store.html',
                  {'store': store,
                   'location_maps': locations})
