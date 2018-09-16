from django.db import models
from django.utils import timezone
from datetime import *
from django.contrib.auth.models import User

# Create your models here.
'''SETUP USER GROUPS'''

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    is_customer = models.BooleanField(default=False)
    is_floorStaff = models.BooleanField(default=False)
    is_generalManager = models.BooleanField(default=False)
    is_boardMember = models.BooleanField(default=False)

'''
PROCESS ---
Added to helloworld/settings

python manage.py makemigrations CRC
python manage.py sqlmigrate CRC 00##
python manage.py migrate


python manage.py shell ....
    from CRC.models import Car, Order
    from django.utils import timezone
    c = Car(car_name = "", car_bodytype = "")
    c.save()
    Car.objects.get(pk=1)
    c.order_set.create(order_location = "", order_date=timezone.now())
    c.order_set.all()
'''

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
        return self.car_makename + ": " + self.car_model

class Store(models.Model):
    store_name = models.CharField(max_length = 128, default = "null")
    store_address = models.CharField(max_length = 128, default = "null")
    store_phone = models.BigIntegerField(default = -1)
    store_city = models.CharField(max_length = 128, default = "null")
    store_state = models.CharField(max_length = 128, default = "null")
    store_latitude = models.CharField(max_length = 128, default = "null")
    store_longitude = models.CharField(max_length = 128, default = "null")
    def __str__(self):
        return self.store_name

class User(models.Model):
    user_name = models.CharField(max_length = 32, default = "null")
    user_phone = models.IntegerField(default = -1)
    user_address = models.CharField(max_length = 32, default = "null")
    user_birthday = models.DateField('user birthday', default=datetime.today, blank=True)
    user_occupation = models.CharField(max_length = 32, default = "null")
    user_gender = models.CharField(max_length = 32, default = "null")
    user_password = models.CharField(max_length = 128, default = "null")
    def __str__(self):
        return self.user_name

class Order(models.Model):
    car_id = models.ForeignKey(Car, on_delete = models.CASCADE) 
    customer_id = models.ForeignKey(User, on_delete = models.CASCADE)
    order_create_date = models.DateField('order create date', default=datetime.today, blank=True)
    order_pickup_store_id = models.ForeignKey(Store, related_name = 'pickup_store_order_set', on_delete = models.CASCADE)
    order_pickup_date = models.DateField('order pickup date', default=datetime.today, blank=True)
    order_return_store_id = models.ForeignKey(Store, related_name = 'return_store_order_set', on_delete = models.CASCADE)
    order_return_date = models.DateField('order return date', default=datetime.today, blank=True)
    def __str__(self):
        return self.order_pickup_store_id.store_name + ": " + self.order_pickup_date.strftime("%d-%b-%y")


'''
c = Car(id = row['Car_ID'],
    car_makename = row['Car_MakeName'],
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

s = Store(id = row['Store_ID'],
    store_name = row['Store_Name'],
	store_address = row['Store_Address'],
	store_phone = int(row['Store_Phone'].replace("-", "").replace(" ", "")[-10:]),
	store_city = row['Store_City'],
	store_state = row['Store_State_Name'],
    store_latitude = row['Store_Latitude'],
    store_longitude = row['Store_Longitude'])

u = User(id = row['Customer_ID'],
    user_name = row['Customer_Name'],
	user_phone = int(row['Customer_Phone'].replace("-", "")),
	user_address = row['Customer_Address'],
	user_birthday = date((int(row['Customer_Birthday'].split("-")[2]) + 1900),
                      int(row['Customer_Birthday'].split("-")[1]),
                      int(row['Customer_Birthday'].split("-")[0])),
	user_occupation = row['Customer_Occupation'],
	user_gender = row['Customer_Gender'],
	user_password = row['Customer_Password'])
    
o = Order(id = row['Order_ID'],
    car_id = Car.objects.get(pk = row['Car_ID']),
    customer_id = User.objects.get(pk = row['Customer_ID']),
    order_create_date = date((int(row['Order_Create_Date'].split("-")[2]) + 2000),
                             int(row['Order_Create_Date'].split("-")[1]),
                             int(row['Order_Create_Date'].split("-")[0])),
    order_pickup_store_id = Store.objects.get(pk = row['Order_Pickup_Store']),
    order_pickup_date = date((int(row['Order_Pickup_Date'].split("-")[2]) + 2000), 
                             int(row['Order_Pickup_Date'].split("-")[1]),
                             int(row['Order_Pickup_Date'].split("-")[0])),
    order_return_store_id = Store.objects.get(pk = row['Order_Return_Store']),
    order_return_date = date((int(row['Order_Return_Date'].split("-")[2]) + 2000), 
                             int(row['Order_Return_Date'].split("-")[1]), 
                             int(row['Order_Return_Date'].split("-")[0])))
'''