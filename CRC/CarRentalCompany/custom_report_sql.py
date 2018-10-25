from .models import *


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
        elif field == 'num_orders':
            num_orders = value
            continue
        elif field == 'more_than_orders':
            more_than_orders = value
            continue
        elif field == 'ordered_between_start':
            order_start = value
            continue
        elif field == 'ordered_between_end':
            order_end = value
            continue
        elif field == 'car_filters':
            car_filters = value
            continue
        elif field == 'orders_include':
            orders_include = value
            continue
        else:
            # check if field is filled out
            if value != "Null":
                # create where statement
                where_statement = "CarRentalCompany_car.car_" + field + "='" + value + "'"
                sql_where_statements.append(where_statement)
            continue

    base_query = '''SELECT CarRentalCompany_car.*
                FROM crc_central_database.CarRentalCompany_car'''
    if orders_include == 'on':
        base_query = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_orders
                   FROM crc_central_database.CarRentalCompany_car
                   LEFT JOIN crc_central_database.CarRentalCompany_order
                   ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)'''
        if num_orders == 'on':
            base_query = '''SELECT CarRentalCompany_car.*, count(CarRentalCompany_order.car_id_id) as number_of_orders
                   FROM crc_central_database.CarRentalCompany_car
                   LEFT JOIN crc_central_database.CarRentalCompany_order
                   ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)'''
        if not order_start == "":
            if "WHERE" not in base_query:
                base_query = base_query + " WHERE CarRentalCompany_order.order_pickup_date >= '" + order_start + "'"
            else:
                base_query = base_query + " AND  CarRentalCompany_order.order_pickup_date >= '" + order_start + "'"
        if not order_end == "":
            if "WHERE" not in base_query:
                base_query = base_query + " WHERE CarRentalCompany_order.order_pickup_date <= '" + order_end + "'"
            else:
                base_query = base_query + " AND  CarRentalCompany_order.order_pickup_date <= '" + order_end + "'"
    if car_filters == 'on':
        if "WHERE" not in base_query:
            if len(sql_where_statements) > 0:
                base_query = base_query + " WHERE " + sql_where_statements[0]
                for index in range(1, len(sql_where_statements)):
                    base_query = base_query + " AND " + sql_where_statements[index]
        else:
            for index in range(1, len(sql_where_statements)):
                base_query = base_query + " AND " + sql_where_statements[index]

    if orders_include == 'on':
        base_query = base_query + " GROUP BY CarRentalCompany_car.id"

    if more_than_orders != '0':
        if num_orders == 'on':
            base_query = base_query + " HAVING number_of_orders > " + more_than_orders
        else:
            base_query = base_query + " HAVING number_orders > " + more_than_orders

    results = Car.objects.raw(base_query)
    return results


def handle_customer_custom_report(fields):
    sql_where_statements = []
    num_orders = ""
    more_than_orders = ""
    order_end = ""
    order_start = ""
    customer_filters = ""
    orders_include = ""
    for field, value in fields.items():
        # ignore the field if it is the csrf token
        if field == 'csrfmiddlewaretoken':
            continue
        elif field == 'num_orders':
            num_orders = value
            continue
        elif field == 'more_than_orders':
            more_than_orders = value
            continue
        elif field == 'ordered_between_start':
            order_start = value
            continue
        elif field == 'ordered_between_end':
            order_end = value
            continue
        elif field == 'customer_filters':
            customer_filters = value
            continue
        elif field == 'orders_include_customer':
            orders_include = value
            continue
        elif field == 'from_age' and value != '':
            where_statement = "FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25) > " + value
            sql_where_statements.append(where_statement)
            continue
        elif field == 'to_age' and value != '':
            where_statement = "FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25) < " + value
            sql_where_statements.append(where_statement)
            continue
        elif (field == 'occupation' or field == 'gender') and value != "Null":
            where_statement = "CarRentalCompany_user.user_" + field + "='" + value + "'"
            sql_where_statements.append(where_statement)
            continue

    base_query = '''SELECT CarRentalCompany_user.*
                    FROM crc_central_database.CarRentalCompany_user'''
    if orders_include == 'on':
        base_query = '''SELECT CarRentalCompany_user.*, count(CarRentalCompany_order.customer_id_id) as number_orders
                       FROM crc_central_database.CarRentalCompany_user
                       LEFT JOIN crc_central_database.CarRentalCompany_order
                       ON (CarRentalCompany_order.customer_id_id = CarRentalCompany_user.id)'''
        if num_orders == 'on':
            base_query = '''SELECT CarRentalCompany_user.*, count(CarRentalCompany_order.customer_id_id) as number_of_orders
                       FROM crc_central_database.CarRentalCompany_user
                       LEFT JOIN crc_central_database.CarRentalCompany_order
                       ON (CarRentalCompany_order.customer_id_id = CarRentalCompany_user.id)'''
        if not order_start == "":
            if "WHERE" not in base_query:
                base_query = base_query + " WHERE CarRentalCompany_order.order_pickup_date >= '" + order_start + "'"
            else:
                base_query = base_query + " AND  CarRentalCompany_order.order_pickup_date >= '" + order_start + "'"
        if not order_end == "":
            if "WHERE" not in base_query:
                base_query = base_query + " WHERE CarRentalCompany_order.order_pickup_date <= '" + order_end + "'"
            else:
                base_query = base_query + " AND  CarRentalCompany_order.order_pickup_date <= '" + order_end + "'"
    if customer_filters == 'on':
        if "WHERE" not in base_query:
            if len(sql_where_statements) > 0:
                base_query = base_query + " WHERE " + sql_where_statements[0]
                for index in range(1, len(sql_where_statements)):
                    base_query = base_query + " AND " + sql_where_statements[index]
        else:
            for index in range(1, len(sql_where_statements)):
                base_query = base_query + " AND " + sql_where_statements[index]

    if orders_include == 'on':
        base_query = base_query + " GROUP BY CarRentalCompany_user.id"

    if more_than_orders != '0':
        if num_orders == 'on':
            base_query = base_query + " HAVING number_of_orders > " + more_than_orders
        else:
            base_query = base_query + " HAVING number_orders > " + more_than_orders

    results = Car.objects.raw(base_query)
    return results


def handle_order_custom_report(fields):
    sql_where_statements = []
    order_filters = ""
    cars_include = ""
    customers_include = ""

    for field, value in fields.items():
        # ignore the field if it is the csrf token
        if field == 'csrfmiddlewaretoken':
            continue
        elif field == 'order_filters_order':
            order_filters = value
            continue
        elif field == 'customers_include_order':
            customers_include = value
            continue
        elif field == 'cars_include_order':
            cars_include = value
            continue
        elif field == 'pickup_location' and value != "Null":
            where_statement = "CarRentalCompany_order.order_pickup_store_id_id = " + value
            sql_where_statements.append(where_statement)
            continue
        elif field == 'return_location' and value != "Null":
            where_statement = "CarRentalCompany_order.order_return_store_id_id = " + value
            sql_where_statements.append(where_statement)
            continue
        elif field == 'ordered_between_start' and value != '':
            where_statement = "CarRentalCompany_order.order_pickup_date > '" + value + "'"
            sql_where_statements.append(where_statement)
            continue
        elif field == 'ordered_between_end' and value != '':
            where_statement = "CarRentalCompany_order.order_pickup_date < '" + value + "'"
            sql_where_statements.append(where_statement)
            continue
        elif field == 'order_checked' and value != "Null":
            where_statement = "CarRentalCompany_order.order_checked = " + value
            sql_where_statements.append(where_statement)
            continue
        elif field == 'occupation_orders' and value != "Null":
            where_statement = "CarRentalCompany_user.user_occupation = '" + value + "'"
            sql_where_statements.append(where_statement)
            continue
        elif field == 'from_age' and value != '':
            where_statement = "FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25) > " + value
            sql_where_statements.append(where_statement)
            continue
        elif field == 'to_age' and value != '':
            where_statement = "FLOOR(DATEDIFF(curdate(), CarRentalCompany_user.user_birthday) / 365.25) < " + value
            sql_where_statements.append(where_statement)
            continue
        elif field == 'gender' and value != "Null":
            where_statement = "CarRentalCompany_user.user_gender = '" + value + "'"
            sql_where_statements.append(where_statement)
            continue
        elif field == 'make' and value != "Null":
            where_statement = "CarRentalCompany_car.car_makename = '" + value + "'"
            sql_where_statements.append(where_statement)
            continue
        elif field == 'body_type_orders' and value != "Null":
            where_statement = "CarRentalCompany_car.car_bodytype = '" + value + "'"
            sql_where_statements.append(where_statement)
            continue
        elif field == 'transmission' and value != "Null":
            where_statement = "CarRentalCompany_car.car_transmission = '" + value + "'"
            sql_where_statements.append(where_statement)
            continue

    base_query = '''SELECT CarRentalCompany_order.* FROM CarRentalCompany_order'''
    if cars_include == 'on':
        base_query = base_query + ''' LEFT JOIN crc_central_database.CarRentalCompany_car 
                            ON (CarRentalCompany_order.car_id_id = CarRentalCompany_car.id)'''
    if customers_include == 'on':
        base_query = base_query + ''' LEFT JOIN crc_central_database.CarRentalCompany_user
                            ON (CarRentalCompany_order.customer_id_id = CarRentalCompany_user.id)'''

    if len(sql_where_statements) > 0:
        base_query = base_query + " WHERE " + sql_where_statements[0]
        for index in range(1, len(sql_where_statements)):
            base_query = base_query + " AND " + sql_where_statements[index]

    results = Order.objects.raw(base_query)
    return results


def handle_location_custom_report(fields):
    sql_where_statements = []
    num_orders = ""
    num_customers = ""
    add_order_table = False

    for field, value in fields.items():
        if field == "state" and value !="Null":
            where_statement = "CarRentalCompany_store.store_state = '" + value + "'"
            sql_where_statements.append(where_statement)
            continue
        elif field == "num_orders":
            num_orders = value
            continue
        elif field == "num_customers":
            num_customers = value
            continue
        elif field == 'ordered_between_start' and value != '':
            where_statement = "CarRentalCompany_order.order_pickup_date > '" + value + "'"
            sql_where_statements.append(where_statement)
            add_order_table = True
            continue
        elif field == 'ordered_between_end' and value != '':
            where_statement = "CarRentalCompany_order.order_pickup_date < '" + value + "'"
            sql_where_statements.append(where_statement)
            add_order_table = True
            continue

    base_query = '''SELECT CarRentalCompany_store.* FROM CarRentalCompany_store'''
    add_on = " GROUP BY CarRentalCompany_store.id"
    if num_orders == "on":
        base_query = '''SELECT CarRentalCompany_store.*, Count(CarRentalCompany_order.order_pickup_store_id) as 'number_of_orders'
                        FROM CarRentalCompany_store
                        LEFT JOIN CarRentalCompany_order
                        ON carrentalcompany_order.order_pickup_store_id_id = carrentalcompany_store.id'''

    if num_customers == 'on':
        if "LEFT JOIN" in base_query:
            base_query = '''SELECT CarRentalCompany_store.*, count(CarRentalCompany_order.order_pickup_store_id_id) as 'number_of_orders', count(DISTINCT CarRentalCompany_order.customer_id_id) as 'number_of_customers'
                            FROM CarRentalCompany_store
                            LEFT JOIN CarRentalCompany_order
                            ON CarRentalCompany_order.order_pickup_store_id_id = CarRentalCompany_store.id
                            LEFT JOIN CarRentalCompany_user
                            ON CarRentalCompany_order.customer_id_id = CarRentalCompany_user.id'''
        else:
            base_query = '''SELECT CarRentalCompany_store.*, count(DISTINCT CarRentalCompany_order.customer_id_id) as 'number_of_customers'
                            FROM CarRentalCompany_store
                            LEFT JOIN CarRentalCompany_order
                            ON CarRentalCompany_order.order_pickup_store_id_id = CarRentalCompany_store.id
                            LEFT JOIN CarRentalCompany_user
                            ON CarRentalCompany_order.customer_id_id = CarRentalCompany_user.id'''

    if add_order_table and "LEFT JOIN" not in base_query:
        base_query = base_query + ''' LEFT JOIN CarRentalCompany_order
                        ON carrentalcompany_order.order_pickup_store_id_id = carrentalcompany_store.id'''

    if len(sql_where_statements) > 0:
        base_query = base_query + " WHERE " + sql_where_statements[0]
        for index in range(1, len(sql_where_statements)):
            base_query = base_query + " AND " + sql_where_statements[index]

    base_query = base_query + add_on

    results = Store.objects.raw(base_query)
    return results

