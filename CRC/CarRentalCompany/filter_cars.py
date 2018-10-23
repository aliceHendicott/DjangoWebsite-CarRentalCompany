from .models import Car


def handle_filter_cars(fields):

    # set up where statements based on fields filled out
    sql_where_statements = []
    sort_type = ""
    for field, value in fields.items():
        # ignore the field if it is the csrf token
        if field == 'csrfmiddlewaretoken':
            continue
        if field == 'sort_by':
            sort_type = value
        else:
            # check if field is filled out
            if value != "Null":
                # create where statement
                where_statement = "CarRentalCompany_car.car_" + field + "='" + value + "'"
                sql_where_statements.append(where_statement)

    if sort_type == "":
        sort_type = 'car_makename'

    # join where statements to create sql query
    if len(sql_where_statements) != 0:
        if sort_type == 'popularity':
            base_sql = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
                       FROM crc_central_database.CarRentalCompany_car
                       LEFT JOIN crc_central_database.CarRentalCompany_order
                       ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)'''
            for index in range(1, len(sql_where_statements)):
                base_sql = base_sql + " AND " + sql_where_statements[index]
            base_sql = base_sql + "GROUP BY CarRentalCompany_car.id ORDER BY number_of_orders DESC"
            # run SQL statement
            results = Car.objects.raw(base_sql)
        else:
            base_sql = "SELECT * FROM CarRentalCompany_car WHERE " + sql_where_statements[0]
            for index in range(1, len(sql_where_statements)):
                base_sql = base_sql + " AND " + sql_where_statements[index]
            # run SQL statement
            base_sql = base_sql + "ORDER BY " + sort_type + " ASC"
            results = Car.objects.raw(base_sql)
    else:
        if sort_type == 'popularity':
            sql = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
            FROM crc_central_database.CarRentalCompany_car
            LEFT JOIN crc_central_database.CarRentalCompany_order
            ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)
            GROUP BY CarRentalCompany_car.id
            ORDER BY number_of_orders DESC'''
            results = Car.objects.raw(sql)
        else:
            results = Car.objects.order_by(sort_type)
    num_results = len(list(results))

    # return results or -1 if there are no results
    if num_results != 0:
        return results
    else:
        return -1

def get_current_filter(fields):

    # set up list to return filters
    filters = []

    # go through each field and if a value was entered, add a string containing the filter applied
    if not fields:
        filters = ["sort by: car make name"]
    else:
        for field, value in fields.items():
            # if the field is the csrf token, ignore
            if field == 'csrfmiddlewaretoken':
                continue
            else:
                if value != "Null":
                    filter_data = field + ": " + value
                    # replace underscores with spaces
                    filter_data = filter_data.replace("_", " ")
                    filters.append(filter_data)

    return filters
