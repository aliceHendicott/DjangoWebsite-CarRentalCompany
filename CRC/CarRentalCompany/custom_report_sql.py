def handle_cars_custom_report(fields):
    sql_where_statements = []
    num_orders = ""
    more_than_orders = ""
    order_end = ""
    order_start = ""
    car_filters = ""
    orders_include = ""
    for field, value in fields.items():
        # ignore the field if it is the csrf token
        if field == 'csrfmiddlewaretoken':
            continue
        if field == 'num_orders':
            num_orders = value
        if field == 'more_than_orders':
            more_than_orders = value
        if field == 'ordered_between_start':
            order_start = value
        if field == 'ordered_between_end':
            order_end = value
        if field == 'car_filters':
            car_filters = value
        if field == 'orders_include':
            orders_include = value
        else:
            # check if field is filled out
            if value != "Null":
                # create where statement
                where_statement = "CarRentalCompany_car.car_" + field + "='" + value + "'"
                sql_where_statements.append(where_statement)

        if orders_include and not car_filters:
            if num_orders:
                base_query = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
                       FROM crc_central_database.CarRentalCompany_car
                       LEFT JOIN crc_central_database.CarRentalCompany_order
                       ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)'''

