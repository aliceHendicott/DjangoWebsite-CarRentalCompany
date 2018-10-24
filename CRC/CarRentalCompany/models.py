from django.db import models
from django.utils import timezone
from datetime import *
from django.contrib.auth.models import User as auth_User
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import *


# Create your models here.
'''SETUP USER GROUPS'''


class UserProfile(models.Model):
    user = models.OneToOneField(auth_User, unique=True, on_delete=models.CASCADE)
    is_customer = models.BooleanField(default=True)
    is_floorStaff = models.BooleanField(default=False)
    is_generalManager = models.BooleanField(default=False)
    is_boardMember = models.BooleanField(default=False)
    customer_number = models.IntegerField(default=-1)

    @receiver(post_save, sender=auth_User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        instance.userprofile.save()

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
    def get_car_makename(self):
        return self.car_makename
    def set_car_makename(self, new_makename):
        setattr(self, 'car_makename', new_makename)
    # Data Extraction
    def top_cars(limit = -1, 
                 start_date = datetime(1, 1, 1).strftime("%Y-%m-%d"), 
                 end_date = datetime.today().strftime("%Y-%m-%d")):
        query = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
                   FROM CarRentalCompany_car
                   LEFT JOIN CarRentalCompany_order
                   ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)
                   WHERE
                       order_pickup_date BETWEEN "''' + start_date + '''" AND "''' + end_date + '''"
                   GROUP BY
	                   CarRentalCompany_car.car_model, CarRentalCompany_car.car_makename
                   ORDER BY number_of_orders DESC'''
        if (limit > 0):
            query += " LIMIT " + str(limit)
        return Car.objects.raw(query)
    def inactive_cars(limit = -1, 
                 end_date = datetime.today().strftime("%Y-%m-%d")):
        query = '''SELECT CarRentalCompany_car.id, car_makename, car_model, car_series, car_series_year, MAX(order_pickup_date), MAX(order_return_date), GREATEST(MAX(order_return_date), MAX(order_pickup_date)) AS Return_Date
                   FROM CarRentalCompany_order
                   INNER JOIN CarRentalCompany_car 
                   ON CarRentalCompany_order.car_id_id=CarRentalCompany_car.id
                   WHERE
                       order_pickup_date < "''' + end_date + '''" AND order_return_date < "''' + end_date + '''"
                   GROUP BY car_model, car_makename
                   ORDER BY Return_Date ASC'''
        if (limit > 0):
            query += " LIMIT " + str(limit)
        return Car.objects.raw(query)

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
    # Data Extraction
    def store_activity(limit=-1, 
                       start_date = datetime(1, 1, 1).strftime("%Y-%m-%d"), 
                       end_date = datetime.today().strftime("%Y-%m-%d")):
        query = '''SELECT CarRentalCompany_store.*, count(CarRentalCompany_order.order_pickup_store_id_id) as number_of_pickups, count(CarRentalCompany_order.order_return_store_id_id) as number_of_returns,
                   (count(CarRentalCompany_order.order_pickup_store_id_id) + count(CarRentalCompany_order.order_return_store_id_id)) as total_activity
                   FROM CarRentalCompany_store
                   LEFT JOIN CarRentalCompany_order
                   ON (CarRentalCompany_order.order_pickup_store_id_id = CarRentalCompany_store.id)
                   WHERE
                       order_pickup_date BETWEEN "''' + start_date + '''" AND "''' + end_date + '''"
                   GROUP BY
	                   CarRentalCompany_store.id
                   ORDER BY total_activity DESC'''
        if (limit > 0):
            query += " LIMIT " + str(limit)
        return Store.objects.raw(query)
    def store_parking(limit = -1, 
                      end_date = datetime.today().strftime("%Y-%m-%d")):
        # Stores
        stores = Store.objects.raw("SELECT *, id as parking FROM CarRentalCompany_store")
        # Pickups
        query_pickup = '''SELECT carrentalcompany_order.id, store_name, carrentalcompany_store.id as store_id, COUNT(CarRentalCompany_order.id) as picked_up 
                          FROM CarRentalCompany_order 
                          INNER JOIN CarRentalCompany_store 
                          ON CarRentalCompany_store.id = CarRentalCompany_order.order_pickup_store_id_id 
                          WHERE
                              order_pickup_date < "''' + end_date + '''"
                          GROUP BY CarRentalCompany_order.order_pickup_store_id_id
                          '''
        pickups = Order.objects.raw(query_pickup)
        # Returns
        query_return = '''SELECT carrentalcompany_order.id, store_name, carrentalcompany_store.id as store_id, COUNT(CarRentalCompany_order.id) as returned 
                          FROM CarRentalCompany_order 
                          INNER JOIN CarRentalCompany_store 
                          ON CarRentalCompany_store.id = CarRentalCompany_order.order_return_store_id_id 
                          WHERE
                              order_return_date < "''' + end_date + '''"
                          GROUP BY CarRentalCompany_order.order_return_store_id_id
                          '''
        returns = Order.objects.raw(query_return)
        
        # Add to lists
        pickup_nums = [0] * len(stores)
        for pickup in pickups:
            pickup_nums[pickup.store_id-1] = pickup.picked_up
        return_nums = [0] * len(stores)
        for returner in returns:
            return_nums[returner.store_id-1] = returner.returned
        # Find the difference
        for index in range(len(stores)):            
            # Find the difference
            stores[index].parking = pickup_nums[index] - return_nums[index] + 10
       
        # Create a list of [store_id, store_parking] sorted by parking availability
        maxes = [0] * len(stores)
        for index in range(len(stores)):
            maxes[index] = [stores[index].id, stores[index].parking]
        maxes.sort(key=lambda x: x[1])
        for index in range(len(stores)):
            this_store = Store.objects.get(pk = maxes[index][0])
            stores[index].id = maxes[index][0]
            stores[index].store_name  = this_store.store_name
            stores[index].store_city  = this_store.store_city
            stores[index].store_address = this_store.store_address
            stores[index].store_phone = this_store.store_phone
            stores[index].store_state = this_store.store_state
            stores[index].store_latitude = this_store.store_latitude
            stores[index].store_longitude = this_store.store_longitude
            stores[index].parking = maxes[index][1]
            
        # Limit the results
        if (limit > 0):
            stores = stores[0:limit]
        return stores

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
    # Data Extraction
    def user_demographics(limit = -1, 
                          start_date = datetime(1, 1, 1).strftime("%Y-%m-%d"), 
                          end_date = datetime.today().strftime("%Y-%m-%d")):
        # Write queries
        query_total_customer = """SELECT CarRentalCompany_user.id, 
                                   CASE
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 10 AND 29 AND CarRentalCompany_user.user_gender = 'M' THEN '18-29M'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 10 AND 29 AND CarRentalCompany_user.user_gender = 'F' THEN '18-29F'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 30 AND 39 AND CarRentalCompany_user.user_gender = 'M' THEN '30-39M' 
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 30 AND 39 AND CarRentalCompany_user.user_gender = 'F' THEN '30-39F'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 40 AND 49 AND CarRentalCompany_user.user_gender = 'M' THEN '40-49M'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 40 AND 49 AND CarRentalCompany_user.user_gender = 'F' THEN '40-49F'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 50 AND 59 AND CarRentalCompany_user.user_gender = 'M' THEN '50-59M'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 50 AND 59 AND CarRentalCompany_user.user_gender = 'F' THEN '50-59F'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 60 AND 1000 AND CarRentalCompany_user.user_gender = 'M' THEN '60+M'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 60 AND 1000 AND CarRentalCompany_user.user_gender = 'F' THEN '60+F'
                                   END AS UserCategory, 
                                   COUNT(CarRentalCompany_user.id) as NumberUsers, 
                                   CarRentalCompany_user.id as NumberOrders,
                                   CarRentalCompany_user.id as FavoriteBodytype,
                                   CarRentalCompany_user.id as FavoritePickup
                                   FROM CarRentalCompany_user
                                   GROUP BY UserCategory"""
        query_customers_active = """SELECT carrentalcompany_user.id, carrentalcompany_user.user_gender, carrentalcompany_user.user_birthday, MAX(carrentalcompany_order.order_pickup_date) as latest_order
                                    FROM carrentalcompany_user
                                    INNER JOIN carrentalcompany_order
                                    ON carrentalcompany_user.id = carrentalcompany_order.customer_id_id
                                    WHERE carrentalcompany_order.order_pickup_date <= "{0}"
                                    GROUP BY carrentalcompany_user.id""".format(end_date)
        query_total_order = """SELECT CarRentalCompany_order.id, 
                               CASE
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 10 AND 29 AND CarRentalCompany_user.user_gender = 'M' THEN '18-29M'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 10 AND 29 AND CarRentalCompany_user.user_gender = 'F' THEN '18-29F'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 30 AND 39 AND CarRentalCompany_user.user_gender = 'M' THEN '30-39M' 
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 30 AND 39 AND CarRentalCompany_user.user_gender = 'F' THEN '30-39F'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 40 AND 49 AND CarRentalCompany_user.user_gender = 'M' THEN '40-49M'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 40 AND 49 AND CarRentalCompany_user.user_gender = 'F' THEN '40-49F'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 50 AND 59 AND CarRentalCompany_user.user_gender = 'M' THEN '50-59M'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 50 AND 59 AND CarRentalCompany_user.user_gender = 'F' THEN '50-59F'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 60 AND 1000 AND CarRentalCompany_user.user_gender = 'M' THEN '60+M'
                                       WHEN (FLOOR(DATEDIFF("{0}", CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 60 AND 1000 AND CarRentalCompany_user.user_gender = 'F' THEN '60+F'
                               END AS UserCategory, 
                               COUNT(CarRentalCompany_order.id) as NumberOrders
                               FROM CarRentalCompany_user
                               INNER JOIN CarRentalCompany_order
                                   ON CarRentalCompany_order.customer_id_id = CarRentalCompany_user.id
                               WHERE CarRentalCompany_order.order_pickup_date BETWEEN "{1}" AND "{0}"
                               GROUP BY UserCategory""".format(end_date, start_date)
        query_popular_bodytype = """SELECT CarRentalCompany_car.car_bodytype,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 10 AND 29 then 1 end) as F18_29,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 10 AND 29 then 1 end) as M18_29,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as F30_39,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as M30_39,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as F40_49,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as M40_49,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as F50_59,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as M50_59,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 60 AND 1000 then 1 end) as F60plus,
                                    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 60 AND 1000 then 1 end) as M60plus
                                    FROM CarRentalCompany_user
                                    INNER JOIN CarRentalCompany_order 
                                        ON CarRentalCompany_user.id=CarRentalCompany_order.customer_id_id
                                    INNER JOIN CarRentalCompany_car 
                                        ON CarRentalCompany_order.car_id_id=CarRentalCompany_car.id
                                    WHERE CarRentalCompany_order.order_pickup_date BETWEEN "{1}" AND "{0}"
                                    GROUP BY CarRentalCompany_car.car_bodytype""".format(end_date, start_date)
        query_popular_pickup_store = '''SELECT CarRentalCompany_store.store_city,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 10 AND 29 then 1 end) as F18_29,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 10 AND 29 then 1 end) as M18_29,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as F30_39,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as M30_39,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as F40_49,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as M40_49,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as F50_59,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as M50_59,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 60 AND 1000 then 1 end) as F60plus,
                                        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF("{0}", user_birthday) / 365.25)) BETWEEN 60 AND 1000 then 1 end) as M60plus
                                        FROM CarRentalCompany_user
                                        INNER JOIN CarRentalCompany_order ON CarRentalCompany_user.id=CarRentalCompany_order.customer_id_id
                                        INNER JOIN CarRentalCompany_store ON CarRentalCompany_store.id = CarRentalCompany_order.order_pickup_store_id_id
                                        WHERE CarRentalCompany_order.order_pickup_date BETWEEN "{1}" AND "{0}"
                                        GROUP BY CarRentalCompany_order.order_pickup_store_id_id'''.format(end_date, start_date)         

        # Dictionary for indeces
        category_dict =	{
            "18-29F": 0,
            "18-29M": 1,
            "30-39F": 2,
            "30-39M": 3,
            "40-49F": 4,
            "40-49M": 5,
            "50-59F": 6,
            "50-59M": 7,
            "60+F": 8,
            "60+M": 9,
        }
                                        
        # Execute queries
        standard = User.objects.raw(query_total_customer.format("2007-01-01", "2001-01-01"))
        for x in standard:
            x.NumberUsers = 0
            x.NumberOrders = 0
            x.FavoriteBodytype = '-'
            x.FavoritePickup = '-'

        # Replace Number customers
        active_customers = User.objects.raw(query_customers_active.format(end_date))
        for customer in active_customers:
            customer_age = (datetime.strptime(end_date, '%Y-%m-%d').date() - customer.user_birthday).days//365
            if (customer_age < 30):
                key = "18-29"
            elif (customer_age < 40):
                key = "30-39"
            elif (customer_age < 50):
                key = "40-49"
            elif (customer_age < 60):
                key = "50-59"
            else:
                key = "60+"
            key += customer.user_gender.replace(" ", "")
            standard[category_dict[key]].NumberUsers += 1


        # Replace Orders
        total_orders = User.objects.raw(query_total_order)
        for total_order in total_orders:
            index = category_dict[str(total_order.UserCategory)]
            standard[index].NumberOrders = total_order.NumberOrders

        # Replace popular body
        cursor = connection.cursor()
        cursor.execute(query_popular_bodytype)
        popular_bodytype = cursor.fetchall()
        for category in range(1, len(popular_bodytype[0])):
            sub = []
            for body in range(len(popular_bodytype)):
                sub.append(popular_bodytype[body][category])
            if (max(sub) > 0):
                standard[category-1].FavoriteBodytype = popular_bodytype[sub.index(max(sub))][0]

        # Replace popular body
        cursor.execute(query_popular_pickup_store)
        popular_pickup_store = cursor.fetchall()
        for category in range(1, len(popular_pickup_store[0])):
            sub = []
            for store in range(len(popular_pickup_store)):
                sub.append(popular_pickup_store[store][category])
            if(max(sub) > 0):
                standard[category-1].FavoritePickup = popular_pickup_store[sub.index(max(sub))][0]

        return standard

class Order(models.Model):
    car_id = models.ForeignKey(Car, on_delete = models.CASCADE) 
    customer_id = models.ForeignKey(User, on_delete = models.CASCADE)
    order_create_date = models.DateField('order create date', default=datetime.today, blank=True)
    order_pickup_store_id = models.ForeignKey(Store, related_name = 'pickup_store_order_set', on_delete = models.CASCADE)
    order_pickup_date = models.DateField('order pickup date', default=datetime.today, blank=True)
    order_return_store_id = models.ForeignKey(Store, related_name = 'return_store_order_set', on_delete = models.CASCADE)
    order_return_date = models.DateField('order return date', default=datetime.today, blank=True)
    order_checked = models.BooleanField('checked', default=True)
    def __str__(self):
        return self.order_pickup_store_id.store_name + ": " + self.order_pickup_date.strftime("%d-%b-%y")


'''
carObj = Car(id = row['Car_ID'],
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

storeObj = Store(id = row['Store_ID'],
                 store_name = row['Store_Name'],
                 store_address = row['Store_Address'],
                 store_phone = int(row['Store_Phone'].replace("-", "").replace(" ", "")[-10:]),
                 store_city = row['Store_City'],
                 store_state = row['Store_State_Name'],
                 store_latitude = row['Store_Latitude'],
                 store_longitude = row['Store_Longitude'])

userObj = User(id = row['Customer_ID'],
               user_name = row['Customer_Name'],
               user_phone = int(row['Customer_Phone'].replace("-", "")),
               user_address = row['Customer_Address'],
               user_birthday = date((int(row['Customer_Birthday'].split("-")[2]) + 1900),
                                    int(row['Customer_Birthday'].split("-")[1]),
                                    int(row['Customer_Birthday'].split("-")[0])),
               user_occupation = row['Customer_Occupation'],
               user_gender = row['Customer_Gender'],V
               user_password = row['Customer_Password'])
    
orderObj = Order(id = row['Order_ID'],
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