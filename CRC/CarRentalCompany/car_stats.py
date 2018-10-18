from .models import *


def popularity_place(car_id):
    cars_by_popularity = Car.top_cars()
    popularity_place = 1
    for car in cars_by_popularity:
        if car.id == car_id:
            break
        else:
            popularity_place += 1

    return popularity_place


def popular_age_group(car_id):
    age_groups = [30, 40, 50, 60, 70, 80]
    count_orders = []
    cursor = connection.cursor()
    for age_group in age_groups:
        query = ('''SELECT count(carrentalcompany_order.car_id_id)
                FROM carrentalcompany_order
                LEFT JOIN carrentalcompany_car
                ON carrentalcompany_car.id = carrentalcompany_order.car_id_id
                LEFT JOIN carrentalcompany_user
                ON carrentalcompany_order.customer_id_id = carrentalcompany_user.id
                WHERE carrentalcompany_car.id = %d and (FLOOR(DATEDIFF(curdate(), carrentalcompany_user.user_birthday) / 365.25)) BETWEEN %d AND %d''' % (car_id, age_group, age_group + 9))
        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            count_orders.append(result[0])
    index = 0
    current_max = 0
    max_index = 0
    for count in count_orders:
        if count > current_max:
            current_max = count
            max_index = index
        index += 1
    return age_groups[max_index]


def best_suited_for(car_id):
    car = Car.objects.get(pk=car_id)
    tank_capacity = int(car.car_tank_capacity.replace("L", ""))
    if tank_capacity > 70:
        suited_for = "Long Distance Driving (tank capacity is %d" % car.car_tank_capacity
    elif car.car_seating_capacity > 4:
        suited_for = "Family trips (seating capacity is %d" % car.car_seating_capacity
    elif car.car_drive == "4WD":
        suited_for = "Four wheel driving (drive type is 4WD)"
    else:
        suited_for = "General driving"

    return suited_for

