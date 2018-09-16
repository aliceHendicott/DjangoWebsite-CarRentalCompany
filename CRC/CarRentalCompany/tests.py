from django.test import TestCase

# Create your tests here.
from .models import Car, Store, Order, User
from django.utils import timezone 
from datetime import *


class UserSetup(TestCase):
    example_date = "2000-01-01 00:00:00.000000"
    def setUp(self):
        car_obj = Car.objects.create(car_name="Forester",
                                     car_bodytype="Hatchback")
        Order.objects.create(car=car_obj,
                             order_location = "Brisbane",
                             order_date = self.example_date)

    # TODO: make this a proper test case
    def test_order_create(self):
        global example_date
        order = Order.objects.get(car=Car.objects.get(car_name="Forester")) 
        self.assertEqual(str(order), "Brisbane: 01-Jan-00 12:00:00AM")
        self.assertEqual(order.order_location, "Brisbane")
        self.assertEqual(order.order_date.strftime("%Y-%m-%d %H:%M:%S.%f"), self.example_date)