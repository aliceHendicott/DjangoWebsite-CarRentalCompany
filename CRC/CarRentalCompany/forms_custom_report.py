from django import forms
from .models import Car, User as dbUser, Order, Store
from datetime import datetime, date

class choose_report_type(forms.Form):
    choices = [["Cars", "Cars"], ["Customers", "Customers"], ["Orders", "Orders"], ["Locations", "Locations"]]
    report_type = forms.ChoiceField(choices=choices)

class custom_report_cars(forms.Form):

    car_filters = forms.BooleanField(required=False, label="Filter Car")
    orders_include = forms.BooleanField(required=False,  label="Filter Orders")

    seriesYearOptions = []
    bodyTypeOptions = []
    transmissionOptions = []
    seatingCapacityOptions = []
    makeOptions = []
    engineOptions = []
    fuelOptions = []
    tankCapacity = []
    powerOptions = []

    # add data from database to lists
    cars = Car.objects.all()
    for car in cars:
        if car.car_series_year not in seriesYearOptions:
            seriesYearOptions.append(car.car_series_year)
        if car.car_bodytype not in bodyTypeOptions:
            bodyTypeOptions.append(car.car_bodytype)
        if car.car_standard_transmission not in transmissionOptions:
            transmissionOptions.append(car.car_standard_transmission)
        if car.car_seating_capacity not in seatingCapacityOptions:
            seatingCapacityOptions.append(car.car_seating_capacity)
        if car.car_makename not in makeOptions:
            makeOptions.append(car.car_makename)
        if car.car_engine_size not in engineOptions:
            engineOptions.append(car.car_engine_size)
        if car.car_fuel_system not in fuelOptions:
            fuelOptions.append(car.car_fuel_system)
        if car.car_tank_capacity not in tankCapacity:
            tankCapacity.append(car.car_tank_capacity)
        if car.car_power not in powerOptions:
            powerOptions.append(car.car_power)

    # sort lists
    seriesYearOptions.sort()
    bodyTypeOptions.sort()
    transmissionOptions.sort()
    seatingCapacityOptions.sort()
    makeOptions.sort()
    engineOptions.sort()
    fuelOptions.sort()
    tankCapacity.sort()
    powerOptions.sort()

    # set years up as list of list and set up field
    year_options = [["Null", "Please Select"]]
    for year in seriesYearOptions:
        year_options.append([year, year])
    series_year = forms.ChoiceField(choices=year_options, required=False)

    # set body type up as list of list and set up field
    bodyType_options = [["Null", "Please Select"]]
    for type in bodyTypeOptions:
        bodyType_options.append([type, type])
    bodytype = forms.ChoiceField(choices=bodyType_options, label='Body Type', required=False)

    # set seating capacity up as list of list and set up field
    seating_options = [["Null", "Please Select"]]
    for seats in seatingCapacityOptions:
        seating_options.append([seats, seats])
    seating_capacity = forms.ChoiceField(choices=seating_options, required=False)

    # set make name up as list of list and set up field
    make_options = [["Null", "Please Select"]]
    for make in makeOptions:
        make_options.append([make, make])
    makename = forms.ChoiceField(choices=make_options, label='Make Name', required=False)

    # set engine size up as list of list and set up field
    engine_options = [["Null", "Please Select"]]
    for engine in engineOptions:
        engine_options.append([engine, engine])
    engine_size = forms.ChoiceField(choices=engine_options, required=False)

    fuel_options = [["Null", "Please Select"]]
    for fuel in fuelOptions:
        fuel_options.append([fuel, fuel])
    fuel_system = forms.ChoiceField(choices=fuel_options, required=False)

    tank_options = [["Null", "Please Select"]]
    for tank in tankCapacity:
        tank_options.append([tank, tank])
    tank_capacity = forms.ChoiceField(choices=tank_options, required=False)

    power_options = [["Null", "Please Select"]]
    for power in powerOptions:
        power_options.append([power, power])
    power = forms.ChoiceField(choices=power_options, required=False)

    more_than_orders = forms.IntegerField(label='More than ___ orders', required=False, initial=0)
    num_orders = forms.BooleanField(required=False)
    ordered_between_start = forms.DateField(widget=forms.widgets.DateInput(format="%Y/%m/%d", attrs={'type': 'date'}),
                                            label="Ordered after", required=False)
    ordered_between_end = forms.DateField(widget=forms.widgets.DateInput(format="%Y/%m/%d", attrs={'type': 'date'}),
                                          label="Ordered before", required=False)


class custom_report_customers(forms.Form):
    customer_filters = forms.BooleanField(required=False, label="Filter Customer")
    orders_include_customer = forms.BooleanField(required=False, label="Filter Orders")

    occupation_options = []
    customers = dbUser.objects.all()
    for customer in customers:
        if customer.user_occupation not in occupation_options:
            occupation_options.append(customer.user_occupation)
    occupation_options.sort()
    occupation_options_list = [["Null", "Please Select"]]
    for occupation in occupation_options:
        occupation_options_list.append([occupation, occupation])
    occupation = forms.ChoiceField(choices=occupation_options_list)

    from_age = forms.IntegerField(label="Customer above age", required=False)
    to_age = forms.IntegerField(label="Customer below age", required=False)

    gender_options = [["Null", "Please Select"], ["F", "Female"], ["M", "Male"]]
    gender = forms.ChoiceField(choices=gender_options)

    more_than_orders = forms.IntegerField(label='More than ___ orders', required=False, initial=0)
    num_orders = forms.BooleanField(required=False)
    ordered_between_start = forms.DateField(widget=forms.widgets.DateInput(format="%Y/%m/%d", attrs={'type': 'date'}),
                                            label="Ordered after", required=False)
    ordered_between_end = forms.DateField(widget=forms.widgets.DateInput(format="%Y/%m/%d", attrs={'type': 'date'}),
                                          label="Ordered before", required=False)

class custom_report_orders(forms.Form):
    order_filters_order = forms.BooleanField(required=False, label="Filter Orders")
    customers_include_order = forms.BooleanField(required=False, label="Filter Customers")
    cars_include_order = forms.BooleanField(required=False, label="Filter Cars")

    occupation_options = []
    occupations_single_list = []
    customers = dbUser.objects.all()
    for customer in customers:
        if customer.user_occupation not in occupations_single_list:
            occupation_options.append(customer.user_occupation)
            occupations_single_list.append(customer.user_occupation)
    occupation_options.sort()
    occupation_options_list = [["Null", "Please Select"]]
    for occupation in occupation_options:
        occupation_options_list.append([occupation, occupation])
    occupation_orders = forms.ChoiceField(choices=occupation_options_list, label="Occupation")

    from_age = forms.IntegerField(label="Customer above age", required=False)
    to_age = forms.IntegerField(label="Customer below age", required=False)

    gender_options = [["Null", "Please Select"], ["F", "Female"], ["M", "Male"]]
    gender = forms.ChoiceField(choices=gender_options)

    orders = Order.objects.all()
    pickup_location_options = [["Null", "Please select"]]
    pickup_single_list = []
    return_location_options = [["Null", "Please select"]]
    return_single_list = []
    for order in orders:
        if order.order_pickup_store_id not in pickup_single_list:
            pickup_location_options.append([order.order_pickup_store_id.id, order.order_pickup_store_id.store_city])
            pickup_single_list.append(order.order_pickup_store_id)
        if order.order_return_store_id not in return_single_list:
            return_location_options.append([order.order_return_store_id.id, order.order_return_store_id.store_city])
            return_single_list.append(order.order_return_store_id)

    pickup_location = forms.ChoiceField(choices=pickup_location_options)
    return_location = forms.ChoiceField(choices=return_location_options)

    cars = Car.objects.all()
    body_type_options = [["Null", "Please select"]]
    body_single_list = []
    make_options = [["Null", "Please select"]]
    make_single_list = []
    transmission_options = [["Null", "Please select"]]
    transmission_single_list = []
    for car in cars:
        if car.car_makename not in make_single_list:
            make_options.append([car.car_makename, car.car_makename])
            make_single_list.append(car.car_makename)
        if car.car_bodytype not in body_single_list:
            body_type_options.append([car.car_bodytype, car.car_bodytype])
            body_single_list.append(car.car_bodytype)
        if car.car_standard_transmission not in transmission_single_list:
            transmission_options.append([car.car_standard_transmission, car.car_standard_transmission])
            transmission_single_list.append(car.car_standard_transmission)

    make = forms.ChoiceField(choices=make_options)
    body_type_orders = forms.ChoiceField(choices=body_type_options)
    transmission = forms.ChoiceField(choices=transmission_options)

    ordered_between_start = forms.DateField(widget=forms.widgets.DateInput(format="%Y/%m/%d", attrs={'type': 'date'}),
                                            label="Ordered after", required=False)
    ordered_between_end = forms.DateField(widget=forms.widgets.DateInput(format="%Y/%m/%d", attrs={'type': 'date'}),
                                          label="Ordered before", required=False)

    checked_options = [["Null", "Please select"], ["1", "Yes"], ["0", "No"]]
    order_checked = forms.ChoiceField(choices=checked_options)


class custom_report_locations(forms.Form):

    state_options = [["Null", "Please select"]]
    state_single_options = []
    stores = Store.objects.all()
    for store in stores:
        if store.store_state not in state_single_options:
            state_single_options.append(store.store_state)
            state_options.append([store.store_state, store.store_state])
    state = forms.ChoiceField(choices=state_options)

    num_orders = forms.BooleanField(required=False, label="Show number of orders")
    ordered_between_start = forms.DateField(widget=forms.widgets.DateInput(format="%Y/%m/%d", attrs={'type': 'date'}),
                                            label="Ordered after", required=False)
    ordered_between_end = forms.DateField(widget=forms.widgets.DateInput(format="%Y/%m/%d", attrs={'type': 'date'}),
                                          label="Ordered before", required=False)

    num_customers = forms.BooleanField(required=False, label="Show number of customers")