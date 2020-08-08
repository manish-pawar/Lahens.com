from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Rate(models.Model):
    rate = models.FloatField(null=True)


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BusI(models.Model):
    bus_id = models.AutoField
    bus_name = models.CharField(max_length=50)
    seat_count = models.IntegerField(default=0)
    desc = models.CharField(max_length=200)
    froml = models.CharField(max_length=200)
    tol = models.CharField(max_length=200)

    def __str__(self):
        return self.bus_name


class Pathtk(models.Model):
    path_id = models.AutoField
    spot_name = models.CharField(max_length=100)
    bus = models.ForeignKey(BusI, null=True, on_delete=models.SET_NULL)
    state_name = models.ForeignKey(State, null=True, on_delete=models.SET_NULL)
    city_name = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    spot_time = models.CharField(max_length=100)
    spot_distance = models.IntegerField(default=0)
    pref_no = models.IntegerField(default=0)
    last_spot = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.spot_name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    state_name = models.ForeignKey(State, null=True, on_delete=models.SET_NULL)
    city_name = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=2000)

    def __str__(self):
        return self.name


class Bookings(models.Model):
    book_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    bus = models.ForeignKey(BusI, null=True, on_delete=models.SET_NULL)
    seat_no = models.IntegerField(default=0)
    type = models.CharField(max_length=20, default="")
    book_date = models.DateTimeField()
    froml = models.CharField(max_length=100, default="")
    tol = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.customer.name


