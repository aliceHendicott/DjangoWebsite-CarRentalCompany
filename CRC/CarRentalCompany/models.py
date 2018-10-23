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
	                   CarRentalCompany_car.id
                   ORDER BY number_of_orders DESC'''
        if (limit > 0):
            query += " LIMIT " + str(limit)
        return Car.objects.raw(query)
    def seasonal_cars(limit = -1, 
                 start_date = datetime(1, 1, 1).strftime("%Y-%m-%d"), 
                 end_date = datetime.today().strftime("%Y-%m-%d")):
        query = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
                    FROM CarRentalCompany_car
                    LEFT JOIN CarRentalCompany_order
                    ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)
                    WHERE
                       order_pickup_date BETWEEN "''' + start_date + '''" AND "''' + end_date + '''"
                    GROUP BY
	                    CarRentalCompany_car.id
                    ORDER BY number_of_orders DESC'''
        if (limit > 0):
            query += " LIMIT " + str(limit)
        return Car.objects.raw(query)
    def inactive_cars(limit = -1, 
                 start_date = datetime(1, 1, 1).strftime("%Y-%m-%d"), 
                 end_date = datetime.today().strftime("%Y-%m-%d")):
        query = '''SELECT CarRentalCompany_car.id, car_makename, car_model, car_series, car_series_year, MAX(order_pickup_date), MAX(order_return_date), GREATEST(MAX(order_return_date), MAX(order_pickup_date)) AS Return_Date
                   FROM CarRentalCompany_order
                   INNER JOIN CarRentalCompany_car 
                   ON CarRentalCompany_order.car_id_id=CarRentalCompany_car.id
                   WHERE
                       order_pickup_date < "''' + end_date + '''" AND order_return_date < "''' + end_date + '''"
                   GROUP BY car_model, car_makename, car_series, car_series_year
                   ORDER BY Return_Date ASC'''
        if (limit > 0):
            query += " LIMIT " + str(limit)
        return Store.objects.raw(query)

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
                   #WHERE
				   #    MONTH(CarRentalCompany_order.order_pickup_date)=2 AND YEAR(CarRentalCompany_order.order_pickup_date)=2007
        if (limit > 0):
            query += " LIMIT " + str(limit)
        return Store.objects.raw(query)
    def store_parking(limit = -1, 
                      start_date = datetime(1, 1, 1).strftime("%Y-%m-%d"), 
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
        maxes.sort(key=lambda x: x[1], reverse=True)
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
        query_ages_by_range = '''SELECT COUNT(*) AS 'number_of_users', CarRentalCompany_user.user_gender,
            CASE
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 30 AND 39 AND CarRentalCompany_user.user_gender = 'M' THEN '30-39, M' 
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 30 AND 39 AND CarRentalCompany_user.user_gender = 'F' THEN '30-39, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 40 AND 49 AND CarRentalCompany_user.user_gender = 'M' THEN '40-49, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 40 AND 49 AND CarRentalCompany_user.user_gender = 'F' THEN '40-49, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 50 AND 59 AND CarRentalCompany_user.user_gender = 'M'  THEN '50-59, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 50 AND 59 AND CarRentalCompany_user.user_gender = 'F' THEN '50-59, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 60 AND 69 AND CarRentalCompany_user.user_gender = 'M' THEN '60-69, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 60 AND 69 AND CarRentalCompany_user.user_gender = 'F' THEN '60-69, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 70 AND 79 AND CarRentalCompany_user.user_gender = 'M' THEN '70-79, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 70 AND 79 AND CarRentalCompany_user.user_gender = 'F' THEN '70-79, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 80 AND 89 AND CarRentalCompany_user.user_gender = 'M' THEN '80-89, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 80 AND 89 AND CarRentalCompany_user.user_gender = 'F' THEN '80-89, F'
            END AS Ages
            FROM CarRentalCompany_User
            LEFT JOIN CarRentalCompany_order ON (CarRentalCompany_order.customer_id_id = CarRentalCompany_user.id)
            WHERE CarRentalCompany_order.order_pickup_date BETWEEN "''' + start_date +'''" AND "'''+ end_date +'''"
            GROUP BY 
            CASE
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 30 AND 39 AND CarRentalCompany_user.user_gender = 'M' THEN '30-39, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 40 AND 49 AND CarRentalCompany_user.user_gender = 'M' THEN '40-49, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 50 AND 59 AND CarRentalCompany_user.user_gender = 'M' THEN '50-59, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 60 AND 69 AND CarRentalCompany_user.user_gender = 'M' THEN '60-69, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 70 AND 79 AND CarRentalCompany_user.user_gender = 'M' THEN '70-79, M'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 80 AND 89 AND CarRentalCompany_user.user_gender = 'M' THEN '80-89, M' 
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 30 AND 39 AND CarRentalCompany_user.user_gender = 'F' THEN '30-39, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 40 AND 49 AND CarRentalCompany_user.user_gender = 'F' THEN '40-49, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 50 AND 59 AND CarRentalCompany_user.user_gender = 'F' THEN '50-59, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 60 AND 69 AND CarRentalCompany_user.user_gender = 'F' THEN '60-69, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 70 AND 79 AND CarRentalCompany_user.user_gender = 'F' THEN '70-79, F'
                WHEN (FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25)) BETWEEN 80 AND 89 AND CarRentalCompany_user.user_gender = 'F' THEN '80-89, F'
            END 
            ORDER BY Ages'''
        cursor = connection.cursor()
        cursor.execute(query_ages_by_range)
        results = cursor.fetchall()
        ages_by_range = []
        for result in results:
            sublist = []
            for item in result:
                sublist.append(item)
            ages_by_range.append(sublist)

        query_popular_body_type = '''SELECT CarRentalCompany_car.car_bodytype,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as Male_30_39,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as Male_39_49,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as Male_50_59,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 then 1 end) as Male_60_69,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 then 1 end) as Male_70_79,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 then 1 end) as Male_80_89,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as Female_30_39,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as Female_40_49,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as Female_50_59,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 then 1 end) as Female_60_69,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 then 1 end) as Female_70_79,
    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 then 1 end) as Female_80_79
FROM CarRentalCompany_user
INNER JOIN CarRentalCompany_order ON CarRentalCompany_user.id=CarRentalCompany_order.customer_id_id
INNER JOIN CarRentalCompany_car ON CarRentalCompany_order.car_id_id=CarRentalCompany_car.id
WHERE CarRentalCompany_order.order_pickup_date BETWEEN "''' + start_date +'''" AND "'''+ end_date +'''"
GROUP BY CarRentalCompany_car.car_bodytype'''
        cursor.execute(query_popular_body_type)
        results = cursor.fetchall()
        for column in range(1, 13):
            most_popular_body_type_index = 0
            for row in range(0, 17):
                if results[row][column] > most_popular_body_type_index:
                    most_popular_body_type_index = row
            ages_by_range[column-1].append(results[most_popular_body_type_index][0])

        query_popular_pickup_store = '''SELECT CarRentalCompany_store.store_city,
	    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as Male_30_39,
	    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as Male_39_49,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as Male_50_59,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 then 1 end) as Male_60_69,
	    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 then 1 end) as Male_70_79,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 then 1 end) as Male_80_89,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as Female_30_39,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as Female_40_49,
	    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as Female_50_59,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 then 1 end) as Female_60_69,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 then 1 end) as Female_70_79,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 then 1 end) as Female_80_79
        FROM CarRentalCompany_user
        INNER JOIN CarRentalCompany_order ON CarRentalCompany_user.id=CarRentalCompany_order.customer_id_id
        INNER JOIN CarRentalCompany_store ON CarRentalCompany_store.id = CarRentalCompany_order.order_pickup_store_id_id
        WHERE CarRentalCompany_order.order_pickup_date BETWEEN "''' + start_date +'''" AND "'''+ end_date +'''"
        GROUP BY CarRentalCompany_order.order_pickup_store_id_id'''
        cursor.execute(query_popular_pickup_store)
        results = cursor.fetchall()
        for column in range(1, 13):
            most_popular_pickup_store_index = 0
            for row in range(0, 40):
                if results[row][column] > most_popular_pickup_store_index:
                    most_popular_pickup_store_index = row
            ages_by_range[column-1].append(results[most_popular_pickup_store_index][0])

        query_popular_return_store='''SELECT CarRentalCompany_store.store_city,
	    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as Male_30_39,
	    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as Male_39_49,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as Male_50_59,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 then 1 end) as Male_60_69,
	    COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 then 1 end) as Male_70_79,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='M' AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 then 1 end) as Male_80_89,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 then 1 end) as Female_30_39,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 then 1 end) as Female_40_49,
	    COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 then 1 end) as Female_50_59,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 then 1 end) as Female_60_69,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 then 1 end) as Female_70_79,
        COUNT(CASE WHEN CarRentalCompany_user.user_gender='F'  AND (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 then 1 end) as Female_80_79
        FROM CarRentalCompany_user
        INNER JOIN CarRentalCompany_order ON CarRentalCompany_user.id=CarRentalCompany_order.customer_id_id
        INNER JOIN CarRentalCompany_store ON CarRentalCompany_store.id = CarRentalCompany_order.order_return_store_id_id
        WHERE CarRentalCompany_order.order_pickup_date BETWEEN "''' + start_date +'''" AND "'''+ end_date +'''"
        GROUP BY CarRentalCompany_order.order_return_store_id_id'''
        cursor.execute(query_popular_return_store)
        results = cursor.fetchall()
        for column in range(1, 13):
            most_popular_return_store_index = 0
            for row in range(0, 40):
                if results[row][column] > most_popular_return_store_index:
                    most_popular_return_store_index = row
            ages_by_range[column - 1].append(results[most_popular_return_store_index][0])
        ages_by_range.sort(key=lambda x: x[0])
        if (limit > 0):
            ages_by_range = ages_by_range[0:limit]
        return ages_by_range

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