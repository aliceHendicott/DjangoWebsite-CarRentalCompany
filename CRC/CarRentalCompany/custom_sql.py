from .models import Car, Store, Order

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

