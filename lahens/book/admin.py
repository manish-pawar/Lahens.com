from django.contrib import admin

# Register your models here.

from .models import Bookings, BusI, Contact, State, City, Customer, Pathtk, Rate

admin.site.register(Bookings)

admin.site.register(Rate)

admin.site.register(Contact)

admin.site.register(BusI)

admin.site.register(Customer)

admin.site.register(State)

admin.site.register(City)

admin.site.register(Pathtk)