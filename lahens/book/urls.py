"""lahens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path("home/", views.index, name="home"),
    path("", views.buseslist, name="Allbuses"),
    path("addbus/", views.busadd, name="Addbuses"),
    path("state/", views.stateadd, name="stateAdd"),
    path("city/<int:pk>/", views.cityadd, name="cityAdd"),
    path("pathadd/<int:pk>/", views.pathadd, name="pathAdd"),
    path("checkspot/<int:pk>/", views.checkspot, name="pathcheck"),
    path("editbus/<int:pk>/", views.editbus, name="editbus"),

    path('load-cities/', views.load_cities, name='ajax_load_cities'),
    path('load-villages/', views.load_villages, name='ajax_load_villages'),




    path("buses/", views.buses, name="AboutBuses"),
    path("contact/", views.contact, name="ContactUs"),
    path("seat/<int:uid>/<int:ty>", views.seats, name="SeatStatus"),
    path("seatsuc/<int:uid>", views.seatssuc, name="SeatSuccess"),
    path("seatcheck/<str:froml>/<str:tol>/<int:uid>/<int:ty>", views.seatsch, name="SeatCheck"),
    path("busview/<int:uid>", views.busview, name="BusView"),
    path("account/", views.account, name="Account"),
    path("bookings/", views.bookings, name="bookings"),

]
