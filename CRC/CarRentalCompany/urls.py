from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    ## General
    #  Home page
    path('', views.index, name='index'),
    # Login & Register
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    # FAQ
    path('FAQ/', views.FAQ, name='FAQ'),
    
    ## Customers
    # Customer acount
    path('my_account/', views.my_account, name='my_account'),

    ## Staff
    #  Orders
    path('staff/orders/', views.staff_orders, name='staff_orders'),
    path('staff/orders/<int:order_id>', views.staff_order, name='staff_order'),
    #  Customers
    path('staff/customers/', views.staff_customers, name='staff_customers'),
    path('staff/customers/<int:customer_id>', views.staff_customer, name='staff_customer'),
    
    ## Cars
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>/', views.car, name='car'),
    path('cars/<int:car_id>/request/', views.car_request, name='car_request'),
    path('cars/recommend_me/', views.car_recommend, name='car_recommend'),

    ## Stores
    path('stores/', views.stores, name='stores'),
    path('stores/<int:store_id>/', views.store, name='store'),

    ## Reports
    path('reports/dashboard/', views.reports_dashboard, name='reports_dashboard'),
    #  Car reports
    path('reports/cars/seasonal/', views.reports_cars_seasonal, name='reports_cars_seasonal'),
    path('reports/cars/inactive/', views.reports_cars_inactive, name='reports_cars_inactive'),
    #  Store reports
    path('reports/stores/activity/', views.reports_store_activity, name='reports_store_activity'),
    path('reports/stores/parking/', views.reports_store_parking, name='reports_store_parking'),
    #  Customer reports
    path('reports/customers/demographics/', views.reports_customer_demographics, name='reports_customer_demographics'),

    ## TEST
    path('connection/', TemplateView.as_view(template_name ='CarRentalCompany/../templates/registration/login.html')),
]
