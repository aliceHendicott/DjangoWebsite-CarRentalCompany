from .models import Car

def handle_recommendation(purpose, seats, transmission, month):
    if purpose == "1":
        purpose_sql = "CarRentalCompany_car.car_drive='4WD'"
    if purpose == "2":
        purpose_sql = "CarRentalCompany_car.car_seating_capacity>4"
    if purpose == "3":
        purpose_sql = "CarRentalCompany_car.car_tank_capacity>=70"
    # set up SQL based on seats field
    if seats == "1":
        seats_sql = "CarRentalCompany_car.car_seating_capacity>=1"
    if seats == "2":
        seats_sql = "CarRentalCompany_car.car_seating_capacity>=3"
    if seats == "3":
        seats_sql = "CarRentalCompany_car.car_seating_capacity>=5"
    # set up SQL based on transmission field
    if transmission == "1":
        transmission_sql = "CarRentalCompany_car.car_standard_transmission LIKE '%%A%%'"
    if transmission == "2":
        transmission_sql = "CarRentalCompany_car.car_standard_transmission LIKE '%%M%%'"
    # set up SQL based on month field
    months_sql = ("MONTH(CarRentalCompany_order.order_create_date)=%s" % month)
    # set up SQL by joining all above SQL as where statements
    join1 = " "
    sql1 = ["SELECT * FROM CarRentalCompany_car INNER JOIN CarRentalCompany_order ON CarRentalCompany_order.car_id_id = CarRentalCompany_car.id WHERE", purpose_sql]
    join1 = join1.join(sql1)
    join2 = " AND "
    sql2 = [join1, seats_sql, transmission_sql, months_sql]
    join2 = join2.join(sql2)
    join3 = " "
    sql3 = [join2, "ORDER BY CarRentalCompany_car.car_price_new DESC LIMIT 15"]
    join3 = join3.join(sql3)
    # run SQL
    recommended_cars = Car.objects.raw(join3)
    return recommended_cars
