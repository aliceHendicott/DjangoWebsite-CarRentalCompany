from django.contrib import admin

from .models import Car, Store, UserProfile

# Register your models here.
admin.site.register(Car)
admin.site.register(Store)
admin.site.register(UserProfile)
