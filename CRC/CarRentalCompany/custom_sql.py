from .models import Car, Store, Order, User
from django.db import connection

def top3cars():
    query = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
                FROM CarRentalCompany_car
                LEFT JOIN CarRentalCompany_order
                ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)
                GROUP BY
	                CarRentalCompany_car.id
                ORDER BY number_of_orders DESC
                LIMIT 3'''
    results = Car.objects.raw(query)
    return results

def seasonal_cars_preview():
    query = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
                FROM CarRentalCompany_car
                LEFT JOIN CarRentalCompany_order
                ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)
                WHERE
					MONTH(CarRentalCompany_order.order_pickup_date)=2 AND YEAR(CarRentalCompany_order.order_pickup_date)=2007
                GROUP BY
	                CarRentalCompany_car.id
                ORDER BY number_of_orders DESC
                LIMIT 5'''
    results = Car.objects.raw(query)
    return results

def seasonal_cars():
    query = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
                FROM CarRentalCompany_car
                LEFT JOIN CarRentalCompany_order
                ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)
                WHERE
					MONTH(CarRentalCompany_order.order_pickup_date)=2 AND YEAR(CarRentalCompany_order.order_pickup_date)=2007
                GROUP BY
	                CarRentalCompany_car.id
                ORDER BY number_of_orders DESC'''
    results = Car.objects.raw(query)
    return results

def store_activity_preview():
    query = ('''SELECT CarRentalCompany_store.*, count(CarRentalCompany_order.order_pickup_store_id_id) as number_of_orders
                FROM CarRentalCompany_store
                LEFT JOIN CarRentalCompany_order
                ON (CarRentalCompany_order.order_pickup_store_id_id = CarRentalCompany_store.id)
                WHERE
					MONTH(CarRentalCompany_order.order_pickup_date)=2 AND YEAR(CarRentalCompany_order.order_pickup_date)=2007
                GROUP BY
	                CarRentalCompany_store.id
                ORDER BY number_of_orders DESC
                LIMIT 5''')
    results = Store.objects.raw(query)
    return results

def store_activity_query():
    query = ('''SELECT CarRentalCompany_store.*, count(CarRentalCompany_order.order_pickup_store_id_id) as number_of_orders
                FROM CarRentalCompany_store
                LEFT JOIN CarRentalCompany_order
                ON (CarRentalCompany_order.order_pickup_store_id_id = CarRentalCompany_store.id)
                WHERE
					MONTH(CarRentalCompany_order.order_pickup_date)=2 AND YEAR(CarRentalCompany_order.order_pickup_date)=2007
                GROUP BY
	                CarRentalCompany_store.id
                ORDER BY number_of_orders DESC''')
    results = Store.objects.raw(query)
    return results

def store_parking_query():
    query_pickup = 'SELECT *, COUNT(CarRentalCompany_order.id) as picked_up FROM CarRentalCompany_order LEFT JOIN CarRentalCompany_store ON CarRentalCompany_store.id = CarRentalCompany_order.order_pickup_store_id_id GROUP BY CarRentalCompany_order.order_pickup_store_id_id'
    results = Order.objects.raw(query_pickup)

    query_return = 'SELECT *, COUNT(CarRentalCompany_order.id) as returned FROM CarRentalCompany_order GROUP BY CarRentalCompany_order.order_return_store_id_id'
    return_count = Order.objects.raw(query_return)

    i = 0
    for pickup in results:
        pickup.picked_up = abs(pickup.picked_up - return_count[i].returned)
        i += 1
    return results

def inactive_cars():
    query = ('''SELECT CarRentalCompany_car.*,  MAX(CarRentalCompany_order.order_return_date) AS `Return_Date`
                FROM CarRentalCompany_order
                INNER JOIN CarRentalCompany_car ON CarRentalCompany_order.car_id_id=CarRentalCompany_car.id
                GROUP BY CarRentalCompany_car.car_model
                ORDER BY `Return_Date` ASC;''')
    results = Store.objects.raw(query)
    return results

def customer_demographics_query():
    query_ages_by_range = '''SELECT COUNT(*) AS 'number_of_users', user_gender,
            CASE
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 AND user_gender = 'M' THEN '30-39, M' 
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 AND user_gender = 'F' THEN '30-39, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 AND user_gender = 'M' THEN '40-49, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 AND user_gender = 'F' THEN '40-49, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 AND user_gender = 'M'  THEN '50-59, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 AND user_gender = 'F' THEN '50-59, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 AND user_gender = 'M' THEN '60-69, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 AND user_gender = 'F' THEN '60-69, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 AND user_gender = 'M' THEN '70-79, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 AND user_gender = 'F' THEN '70-79, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 AND user_gender = 'M' THEN '80-89, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 AND user_gender = 'F' THEN '80-89, F'
            END AS Ages
            FROM CarRentalCompany_User
            GROUP BY 
            CASE
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 AND user_gender = 'M' THEN '30-39, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 AND user_gender = 'M' THEN '40-49, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 AND user_gender = 'M'  THEN '50-59, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 AND user_gender = 'M' THEN '60-69, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 AND user_gender = 'M' THEN '70-79, M'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 AND user_gender = 'M' THEN '80-89, M' 
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 30 AND 39 AND user_gender = 'F' THEN '30-39, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 40 AND 49 AND user_gender = 'F' THEN '40-49, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 50 AND 59 AND user_gender = 'F' THEN '50-59, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 60 AND 69 AND user_gender = 'F' THEN '60-69, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 70 AND 79 AND user_gender = 'F' THEN '70-79, F'
                WHEN (FLOOR(DATEDIFF(curdate(), user_birthday) / 365.25)) BETWEEN 80 AND 89 AND user_gender = 'F' THEN '80-89, F'
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


    #ages_by_ranges = User.objects.raw(query_ages_by_range)
    #ages_by_ranges = list(ages_by_ranges)

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
GROUP BY CarRentalCompany_car.car_bodytype'''
    cursor.execute(query_popular_body_type)
    results = cursor.fetchall()
    for column in range(0, 12):
        most_popular_body_type = results[0][0]
        for row in range(0, 17):
            if results[row][column] > results[row-1][column]:
                most_popular_body_type = results[row][0]
        ages_by_range[column].append(most_popular_body_type)

    return ages_by_range
