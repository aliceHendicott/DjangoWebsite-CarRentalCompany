from .models import Car, Store

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

