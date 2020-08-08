from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from math import ceil
from .forms import PathForm, CreateUserForm, CustomerForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, admin_only, require_details
from django.contrib.auth.decorators import login_required

from datetime import datetime, timezone, timedelta
import json
# Create your views here.


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'book/register.html', context)


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Allbuses')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'book/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def buseslist(request):

    buses1 = BusI.objects.all()
    if len(buses1) == 0:
        context = {'emptyb': True}

    else:
        pathe = []
        regularb = []
        for i in buses1:
            if i.pathtk_set.count() == 0:
                pathe.append(i)
            else:
                regularb.append(i)
        if len(pathe) == 0:
            context = {'buses': buses, 'emptym': False, 'regulars': regularb}
        else:
            context = {'buses': buses, 'emptym': True, 'emptys': pathe, 'regulars': regularb}
    return render(request, 'book/buslist.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def pathadd(request, pk):
    bus = BusI.objects.get(id=pk)
    states = State.objects.all()

    if request.method == 'POST':
        spotname = request.POST.get('spotname')
        spottime = request.POST.get('spottime')
        spotd = request.POST.get('spotd')
        state = request.POST.get('states')
        city = request.POST.get('cities')
        state1 = State.objects.get(id=state)
        city1 = City.objects.get(id=city)

        if bus.pathtk_set.count() == 0:
            pathk = Pathtk(spot_name=spotname, bus=bus, state_name=state1, city_name=city1, spot_time=spottime,
                           spot_distance=spotd, pref_no=0, last_spot='start')
        else:
            print('doneif')
            path1 = bus.pathtk_set.order_by('-id')[0]
            pathk = Pathtk(spot_name=spotname, bus=bus, state_name=state1, city_name=city1, spot_time=spottime,
                           spot_distance=spotd, pref_no=path1.pref_no, last_spot=path1)
        pathk.save()

    bup = bus.pathtk_set.count()
    if bup == 0:
        context = {'states': states}
    else:
        buk = bus.pathtk_set.order_by('-id')
        context = {'states': states, 'liste': buk}

    return render(request, 'book/add_path.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def checkspot(request, pk):
    bus = BusI.objects.get(id=pk)
    pathli = bus.pathtk_set.order_by('-id')
    context = {'paths': pathli,'bus': bus}
    return render(request, 'book/checkspot.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def load_cities(request):
    state_id = request.GET.get('state')
    state = State.objects.get(id=state_id)
    cities = state.city_set.order_by('name')
    print("hello")
    return render(request, 'book/city_dropdown_list_options.html', {'cities': cities})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def load_villages(request):
    city_id = request.GET.get('city')
    city = City.objects.get(id=city_id)
    villages = city.pathtk_set.order_by('spot_name')

    return render(request, 'book/village_dropdown_list_options.html', {'villages': villages})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def busadd(request):
    if request.method == 'POST':
        bname = request.POST.get('busname')
        scount = request.POST.get('scount')
        desc = request.POST.get('desc')
        froml = request.POST.get('froml')
        tol = request.POST.get('tol')
        bus = BusI(bus_name=bname, seat_count=scount, desc=desc, froml=froml, tol=tol)
        bus.save()
        return redirect('Allbuses')
    return render(request, 'book/bus_add.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def stateadd(request):
    if request.method == 'POST':
        name = request.POST.get('statename')
        state = State(name=name)
        state.save()

    states = State.objects.all().order_by('-id')
    print(len(states))
    if len(states) == 0:
        empt = True
        context = {'empty': empt}
    else:
        context = {'states': states}
    return render(request, 'book/stateadd.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def cityadd(request, pk):
    state = State.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('cityname')
        city = City(state=state, name=name)
        city.save()

    cities = state.city_set.all().order_by('-id')
    print(len(cities))
    if len(cities) == 0:
        empt = True
        context = {'empty': empt, 's_id': pk}
    else:
        context = {'cities': cities, 's_id': pk}
    return render(request, 'book/cityadd.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editbus(request, pk):
    bus = BusI.objects.get(id=pk)
    if request.method == 'POST':
        bname = request.POST.get('busname')
        scount = request.POST.get('scount')
        desc = request.POST.get('desc')
        froml = request.POST.get('froml')
        tol = request.POST.get('tol')
        bus.bus_name = bname
        bus.seat_count = scount
        bus.desc = desc
        bus.froml = froml
        bus.tol = tol
        bus.save()
    context = {'bus': bus}
    return render(request, 'book/editbus.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
@require_details
def index(request):
    return render(request, 'book/index.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account(request):
    user1 = request.user
    states = State.objects.all()
    customer = request.user.customer
    if request.method == 'POST':
        phno = request.POST.get('phno')
        state = request.POST.get('states')
        city = request.POST.get('cities')
        village = request.POST.get('villages')
        state1 = State.objects.get(id=state)
        city1 = City.objects.get(id=city)

        cus = Customer.objects.get(user=user1)
        cus.phone = phno
        cus.city_name = city1
        cus.state_name = state1
        cus.save()
        return redirect('home')
    context = {'states': states, 'customer': customer}
    return render(request, 'book/settings.html', context)


def searchmatch(froml, tol, item):
    '''return true only if query matches items'''
    pathd = [item1.spot_name.lower() for item1 in item.pathtk_set.order_by('id')]
    print(pathd)
    if (froml in pathd) and (tol in pathd):
        return True
    else:
        return False


def typechecker(froml, tol, item):
    pathd = [item1.spot_name.lower() for item1 in item.pathtk_set.order_by('id')]

    if pathd.index(froml) < pathd.index(tol):
        return True
    else:
        return False


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
@require_details
def buses(request):
    user1 = request.user
    params = {}
    if request.method == 'POST':
        fromls = request.POST.get('froml')
        tols = request.POST.get('tol')
        froml = fromls.lower()
        tol = tols.lower()
        if froml == "" and tol == "":

            messages.warning(request, "Please make sure  to enter relevant spots")
        elif froml == tol:

            messages.warning(request, "You can not travel from same starting and ending location")
        else:

            allProds = []

            allProd = []
            cllProd = []

            busesi = BusI.objects.all()
            prod = [item for item in busesi if searchmatch(froml, tol, item)]
            print(prod)
            for item in prod:
                if typechecker(froml, tol, item):
                    allProd.append(item)

                else:
                    cllProd.append(item)

            print(allProd)
            print(cllProd)
            n = len(allProd)
            m = len(cllProd)

            if len(allProd) != 0 or len(cllProd) != 0:
                allProds.append([allProd, cllProd])

            params = {'allProds': allProds, 'froml': froml, 'tol': tol}

            if len(allProds) == 0:
                messages.warning(request, "sorry we dont have any transport services for your route!!")

    return render(request, 'book/buses.html', params)





def contact(request):
    return render(request, 'book/contact.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
@require_details
def busview(request, uid):
    bus = BusI.objects.get(id=uid)
    bup = bus.pathtk_set.order_by('id')
    context = {'busV': bus, 'busp': bup}
    return render(request, 'book/busview.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
@require_details
def seats(request, uid, ty):

    dateoj = request.GET.get('dateoj')

    now = datetime.now()
    deld = now
    if dateoj == "1":
        deld = datetime.now(timezone.utc)
    elif dateoj == "2":
        deld = now + timedelta(days=1)
    elif dateoj == "3":
        deld = now + timedelta(days=2)
    elif dateoj == "4":
        deld = now + timedelta(days=3)
    print(deld)
    modeofj = ""
    if ty == 1:
        modeofj = "normal"
    elif ty == 0:
        modeofj = "return"
    bus = BusI.objects.get(id=uid)
    filtf = []
    busesii = Bookings.objects.filter(bus=bus, type=modeofj)
    for item in busesii:
        print(item.book_date)
        if item.type == modeofj and item.book_date.date() == deld.date():

            filtf.append(item)
    print(filtf)
    print(busesii)
    filtd = []
    for itemd in filtf:
        filtd.append(itemd.seat_no)

    busesf = BusI.objects.filter(id=uid)
    for item in busesf:
        n = item.seat_count
        m = range(1, n+1)
    k = range(3, n+1, 5)
    gp = []
    for i in k:
        gp.append(i)
    print(gp)
    params = {'filtd': filtd, 'n': m, 'gp': gp, 'id': uid}
    return render(request, 'book/seatstatus.html', params)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def seatsch(request, froml, tol, uid, ty):
    modeoj = ""
    if ty == 1:
        modeoj = 'normal'
    elif ty == 0:
        modeoj = 'return'
    bus = BusI.objects.get(id=uid)
    fl = froml
    tl = tol
    params = {'id': uid, 'ty': ty, 'froml': froml, 'tol': tol}
    if request.method == 'POST':
        dateoj = request.POST.get('dateot')
        checkli = request.POST.getlist('seats')
        now = datetime.now()
        deld = now
        if dateoj == "1":
            deld = datetime.now()
        elif dateoj == "2":
            deld = now + timedelta(days=1)
        elif dateoj == "3":
            deld = now + timedelta(days=2)
        elif dateoj == "4":
            deld = now + timedelta(days=3)
        print(deld)
        print(checkli)
        user1 = request.user.customer
        print(checkli)
        if len(checkli) > 0:
            for i in checkli:
                inserta = Bookings(customer=user1, bus=bus, seat_no=i, type=modeoj, book_date=deld, froml=fl, tol=tl)
                inserta.save()

            messages.success(request, "Congrats your seats are booked successfully!!!!")
            return redirect('AboutBuses')
        else:
            messages.warning(request, "please select seats ")

    return render(request, 'book/seatcheck.html', params)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def seatssuc(request, uid):

    return render(request, 'book/seatsuc.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def bookings(request):
    user1 = request.user.customer
    listl = user1.bookings_set.order_by('book_id', 'bus')
    allct = []
    catprods = Bookings.objects.values('book_date')
    cats = {item['book_date'] for item in catprods}
    for cat in cats:
        prod = Bookings.objects.filter(book_date=cat, customer=user1)
        allct.append(prod)
    context = {'liste': allct}
    return render(request, 'book/bookings.html', context)

