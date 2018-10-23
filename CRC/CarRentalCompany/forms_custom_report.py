from django import forms
from .models import Car
from datetime import datetime, date

class choose_report_type(forms.Form):
    choices = [["Cars", "Cars"], ["Customers", "Customers"], ["Orders", "Orders"], ["Locations", "Locations"]]
    report_type = forms.ChoiceField(choices=choices)

class custom_report_cars(forms.Form):

    car_filters = forms.BooleanField(required=False)
    orders_include = forms.BooleanField(required=False)

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

    more_than_orders = forms.IntegerField(label='More than ___ fields', required=False, initial=0)
    num_orders = forms.BooleanField(required=False)
    ordered_between_start = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y", attrs={'type': 'date'}), label="Ordered after", required=False, initial=date(2005, 7, 1))
    ordered_between_end = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y", attrs={'type': 'date'}), label="Ordered before", required=False, initial=date(datetime.today().year, datetime.today().month, datetime.today().day))
