from .models import Car

def handle_filter_cars(fields):

    #set up where statements based on fields filled out
    sql_where_statements = []
    for field, value in fields.items():
        #ignore the field if it is the csrf token
        if field == 'csrfmiddlewaretoken':
            continue
        else:
            #check if field is filled out
            if value != "Null":
                #create where statement
                where_statement = "CarRentalCompany_car.car_" + field + "=" + value
                sql_where_statements.append(where_statement)

    # if all fields are null (no fields entered when 'Apply' clicked) return -1
    if len(sql_where_statements) == 0:
        return -2

    # join where statements to create sql query
    base_sql = "SELECT * FROM CarRentalCompany_car WHERE " + sql_where_statements[0]
    for index in range(1, len(sql_where_statements)):
        base_sql = base_sql + " AND " + sql_where_statements[index]

    #run SQL statement
    results = Car.objects.raw(base_sql)
    num_results = len(list(results))

    #return results or -1 if there are no results
    if num_results != 0:
        return results
    else:
        return -1

def get_current_filter(fields):

    # set up list to return filters
    filters = []

    # go through each field and if a value was entered, add a string containing the filter applied
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
