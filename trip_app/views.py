from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import User, Trip
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST ['first_name'],
            last_name = request.POST ['last_name'],
            email = request.POST ['email'],
            password = pw_hash,
        )
        request.session['userid'] = new_user.id 
        return redirect('/dash')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:    
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id 
                return redirect('/dash')
            else:
                messages.error(request, 'Invalid password')
            return redirect('/')
        return redirect('/')

def dash(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    trips = Trip.objects.all()
    context = {
        'user': user,
        'user_trips': Trip.objects.filter(going=user),
        'other_trips': Trip.objects.all().exclude(creator=user).exclude(going=user),
    }
    return render(request, 'dash.html', context)

def new(request):
    user = User.objects.get(id=request.session['userid'])
    context = {
        'user': user,
    }
    return render(request, 'new.html', context)

def create(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        this_trip = Trip.objects.get(id=trip_id)
        context = {
            'trip': this_trip
        }
        return render(request, 'new.html', context)
    else:
        user = User.objects.get(id=request.session['userid'])
        trip = Trip.objects.create(
            city=request.POST['city'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            plan=request.POST['plan'],
        )
        user.my_trips.add(trip)
        return redirect('/dash')

def edit(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['userid'])
    context = {
        'trip': this_trip,
        'user': user
    }
    return render(request, 'edit.html', context)

def update(request, trip_id):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        this_trip = Trip.objects.get(id=trip_id)
        context = {
            'trip': this_trip
        }
        return render(request, 'edit.html', context)
    else:
        user = User.objects.get(id=request.session['userid'])
        this_trip = Trip.objects.get(id=trip_id)
        this_trip.city=request.POST['city']
        this_trip.start_date=request.POST['start_date']
        this_trip.end_date=request.POST['end_date']
        this_trip.plan=request.POST['plan']
        this_trip.save()
        return redirect('/dash')

def info(request, trip_id):
    user = User.objects.get(id=request.session['userid'])
    trip = Trip.objects.get(id=trip_id)
    context = {
        'trip': trip,
        'user': user
    }
    return render(request, 'trips.html', context)

def join(request, trip_id):
    user = User.objects.get(id=request.session['userid'])
    this_trip = Trip.objects.get(id=trip_id)
    user.my_trips.add(this_trip)
    return redirect('/dash')

def remove(request, trip_id):
    user = User.objects.get(id=request.session['userid'])
    this_trip = Trip.objects.get(id=trip_id)
    user.my_trips.remove(this_trip)
    return redirect('/dash')


def logout(request):
    request.session.clear()
    return redirect('/')