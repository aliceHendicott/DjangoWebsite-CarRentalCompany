from .models import Car

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
