from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views, views_customer, views_reports, views_staff, views_store

urlpatterns = [
    ## General
    #  Home page
    path('', views.index, name='index'),
    # Login & Register
    path('loginjs/', views.handle_login, name="loginjs"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name='register'),
    # FAQ
    path('FAQ/', views.FAQ, name='FAQ'),
    
    ## Customers
    # Customer account
    path('my_account/', views_customer.my_account, name='my_account'),

    ## Staff
    #  Orders
    path('staff/orders/', views_staff.orders, name='staff_orders'),
    path('staff/orders/<int:order_id>', views_staff.order, name='staff_order'),
    #  Customers
    path('staff/customers/', views_staff.customers, name='staff_customers'),
    path('staff/customers/<int:customer_id>', views_staff.customer, name='staff_customer'),
    
    ## Cars
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>/', views.car, name='car'),
    path('cars/<int:car_id>/request/', views.car_request, name='car_request'),
    path('cars/recommend_me/', views.car_recommend, name='car_recommend'),

    ## Stores
    path('stores/', views_store.stores, name='stores'),
    path('stores/<int:store_id>/', views_store.store, name='store'),

    ## Reports
    path('reports/dashboard/', views_reports.dashboard, name='reports_dashboard'),
    #  Car reports
    path('reports/cars/seasonal/', views_reports.cars_seasonal, name='reports_cars_seasonal'),
    path('reports/cars/inactive/', views_reports.cars_inactive, name='reports_cars_inactive'),
    #  Store reports
    path('reports/stores/activity/', views_reports.store_activity, name='reports_store_activity'),
    path('reports/stores/parking/', views_reports.store_parking, name='reports_store_parking'),
    #  Customer reports
    path('reports/customers/demographics/', views_reports.customer_demographics, name='reports_customer_demographics'),

    ## TEST
    path('connection/', TemplateView.as_view(template_name ='CarRentalCompany/../templates/registration/login.html')),
]
