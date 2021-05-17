from django.db import models
import re
from datetime import date

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        users = User.objects.all()
        if len(postData['first_name']) < 2:
            errors['firt_name'] = 'First name must be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'
        for user in users:
            if (postData ['email']) == user.email:
                errors['email'] = 'User already exists'
        if (postData ['pass_confirm']) != (postData ['password']):
            errors['pass_confirm'] = 'Passwords must match'
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = (postData ['email']))
        if not user:
            errors['email'] = 'Email not yet registered'
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        today = str(date.today())
        trips = Trip.objects.all()
        if len(postData ['city']) < 3:
            errors['city'] = 'City name must be at least 3 characters'
        if len(postData ['plan']) < 3:
            errors['plan'] = 'You need more plans'
        if (postData ['start_date']) <= today:
            errors['start_date'] = 'Trip can only begin after toaday'
        if (postData ['end_date']) <= (postData ['start_date']):
            errors['end_date'] = 'End date must come after the start date'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    pass_confirm = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    city = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='created_trips', on_delete=models.CASCADE, null=True)
    going = models.ManyToManyField(User, related_name='my_trips')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = TripManager()