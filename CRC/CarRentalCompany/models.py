from django.db import models
from django.utils import timezone
from datetime import *

# Create your models here.

##Process
# Added to helloworld/settings
# python manage.py makemigrations CRC
# python manage.py sqlmigrate CRC 00##
# python manage.py migrate
# python manage.py shell ....
    #from CRC.models import Car, Order
    #from django.utils import timezone
    #c = Car(car_name = "", car_bodytype = "")
    #c.save()
    #Car.objects.get(pk=1)
    #c.order_set.create(order_location = "", order_date=timezone.now())
    #c.order_set.all()



class Car(models.Model):
    car_makename = models.CharField(max_length = 128, default = "null")
    car_model = models.CharField(max_length = 128, default = "null")
    car_series = models.CharField(max_length = 128, default = "null")
    car_series_year = models.CharField(max_length = 128, default = "null")
    car_price_new = models.IntegerField(default = -1)
    car_engine_size = models.CharField(max_length = 128, default = "null")
    car_fuel_system = models.CharField(max_length = 128, default = "null")
    car_tank_capacity = models.CharField(max_length = 128, default = "null")
    car_power = models.CharField(max_length = 128, default = "null")
    car_seating_capacity = models.IntegerField(default = -1)
    car_standard_transmission = models.CharField(max_length = 128, default = "null")
    car_bodytype = models.CharField(max_length = 128, default = "null")
    car_drive = models.CharField(max_length = 128, default = "null")
    car_wheelbase = models.CharField(max_length = 128, default = "null")
    car_bodytype = models.CharField(max_length = 128, default = "null")
    def __str__(self):
        return self.car_make_name

class Store(models.Model):
    store_name = models.CharField(max_length = 128, default = "null")
    store_address = models.CharField(max_length = 128, default = "null")
    store_phone = models.IntegerField(default = -1)
    store_city = models.CharField(max_length = 128, default = "null")
    store_state = models.CharField(max_length = 128, default = "null")
    def __str__(self):
        return self.store_location

class User(models.Model):
    user_name = models.CharField(max_length = 32, default = "null")
    user_phone = models.IntegerField(default = -1)
    user_address = models.CharField(max_length = 32, default = "null")
    user_birthday = models.DateTimeField('user birthday', default=datetime.now, blank=True)
    user_occupation = models.CharField(max_length = 32, default = "null")
    user_gender = models.CharField(max_length = 32, default = "null")
    email = models.EmailField(default = -1)
    password = models.CharField(max_length = 128, default = "null")
    def __str__(self):
        return self.name

class Order(models.Model):
    car_id = models.ForeignKey(Car, on_delete = models.CASCADE) 
    customer_id = models.ForeignKey(User, on_delete = models.CASCADE)
    order_create_date = models.DateTimeField('order create date', default=datetime.now, blank=True)
    order_pickup_store_id = models.ForeignKey(Store, related_name = 'pickup_store_order_set', on_delete = models.CASCADE)
    order_pickup_date = models.DateTimeField('order pickup date', default=datetime.now, blank=True)
    order_return_store_id = models.ForeignKey(Store, related_name = 'return_store_order_set', on_delete = models.CASCADE)
    order_return_date = models.DateTimeField('order return date', default=datetime.now, blank=True)
    def __str__(self):
        return self.order_location + ": " + self.order_date.strftime("%d-%b-%y %I:%M:%S%p")
    
'''
p = Car(car_makename = row['Car_MakeName'],
    car_model = row['Car_Model'],
    car_series = row['Car_Series'],
    car_series_year = row['Car_SeriesYear'],
    car_price_new = row['Car_PriceNew'],
    car_engine_size = row['Car_EngineSize'],
    car_fuel_system = row['Car_FuelSystem'],
    car_tank_capacity = row['Car_TankCapacity'],
    car_power = row['Car_Power'],
    car_seating_capacity = row['Car_SeatingCapacity'],
    car_standard_transmission = row['Car_StandardTransmission'],
    car_bodytype = row['Car_BodyType'],
    car_drive = row['Car_Drive'],
    car_wheelbase = row['Car_Wheelbase'])
'''