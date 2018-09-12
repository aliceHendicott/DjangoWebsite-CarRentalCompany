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
    car_name = models.CharField(max_length = 128)
    car_bodytype = models.CharField(max_length = 200)
    def __str__(self):
        return self.car_name

class Store(models.Model):
    store_location = models.CharField(max_length = 128)
    store_phone_number = models.IntegerField()
    def __str__(self):
        return self.store_location

class Order(models.Model):
    car = models.ForeignKey(Car, on_delete = models.CASCADE)
    order_location = models.CharField(default = "Brisbane", max_length = 128)
    order_date = models.DateTimeField('date published')
    def __str__(self):
        return self.order_location + ": " + self.order_date.strftime("%d-%b-%y %I:%M:%S%p")
    
class User(models.Model):
    name = models.CharField(max_length = 32)
    email = models.EmailField()
    password = models.CharField(max_length = 128)
    def __str__(self):
        return self.name