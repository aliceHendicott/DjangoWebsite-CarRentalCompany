from .models import Car

def handle_filter_cars(series_year, body_type, seating_capacity, make, engine_size, fuel_system, tank_capacity, power):
    # create where sql statements based on the entered data
    series_sql = ""
    body_type_sql = ""
    seating_capacity_sql = ""
    make_sql = ""
    engine_size_sql = ""
    fuel_system_sql = ""
    tank_capacity_sql = ""
    power_sql = ""

    if series_year != "Null":
        series_sql = "CarRentalCompany_car.car_series_year>=%s" % series_year
    if body_type != "Null":
        body_type_sql = "CarRentalCompany_car.car_bodytype='%s'" % body_type
    if seating_capacity != "Null":
        seating_capacity_sql = "CarRentalCompany_car.car_seating_capacity>=%s" % seating_capacity
    if make != "Null":
        make_sql = "CarRentalCompany_car.car_makename='%s'" % make
    if engine_size != "Null":
        engine_size_sql = "CarRentalCompany_car.car_engine_size='%s'" % engine_size
    if fuel_system != "Null":
        fuel_system_sql = "CarRentalCompany_car.car_fuel_system='%s"'' % fuel_system
    if tank_capacity != "Null":
        tank_capacity_sql = "CarRentalCompany_car.car_tank_capacity='%s'" % tank_capacity
    if power != "Null":
        power_sql = "CarRentalCompany_car.car_power='%s'" % power

    # determine the first sql statement
    field_sql = [series_sql, body_type_sql, seating_capacity_sql, make_sql, engine_size_sql, fuel_system_sql, tank_capacity_sql, power_sql]
    starting_field = 0
    for field in field_sql:
        if field != "":
            break
        else:
            starting_field += 1
    # if all fields are null return -1
    if starting_field == 8:
        return -2

    # join where statements to create sql query
    base_sql = "SELECT * FROM CarRentalCompany_car WHERE " + field_sql[starting_field]
    for i in range(starting_field + 1, 8):
        if field_sql[i] != "":
            base_sql = base_sql + " AND " + field_sql[i]

    #run SQL
    results = Car.objects.raw(base_sql)
    num_results = len(list(results))

    if num_results != 0:
        return results
    else:
        return -1

def current_filter(series_year, body_type, seating_capacity, make, engine_size, fuel_system, tank_capacity, power):
    filters = []
    if series_year != "Null":
        filters.append('Minimum series year: %s' % series_year)
    if body_type != "Null":
        filters.append('Body Type: %s' % body_type)
    if seating_capacity != "Null":
        filters.append('Minimum seating capacity: %s' % seating_capacity)
    if make != "Null":
        filters.append('Make name: %s' % make)
    if engine_size != "Null":
        filters.append('Engine size: %s' % engine_size)
    if fuel_system != "Null":
        filters.append('Fuel system: %s' % fuel_system)
    if tank_capacity != "Null":
        filters.append('Tank capacity: %s' % tank_capacity)
    if power != "Null":
        filters.append('Power: %s' % power)

    return filters
