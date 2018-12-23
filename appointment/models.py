from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import timedelta
import math
# Create your models here.

class Treatment(models.Model):
    name = models.CharField(max_length=30, unique=True)
    cost_price = models.IntegerField(blank=False, null=False)
    selling_price = models.IntegerField(blank = False, null = False)
    description = models.TextField(blank=False, null=False, default=' ')
    duration = timedelta.fields.TimedeltaField()
    store = models.ForeignKey('Store', on_delete=models.DO_NOTHING)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Employee(models.Model):
    class Meta:
        unique_together = (('name', 'store', 'address', 'email'),)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=11)
    active = models.BooleanField(default=True)
    store = models.ForeignKey('Store', on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Appointment(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    Employee = models.ForeignKey('Employee', on_delete=models.DO_NOTHING)
    treatment = models.ForeignKey('Treatment', on_delete=models.DO_NOTHING, default=None)
    offer = models.ForeignKey('Offer', default = 1)
    schedule = models.DateTimeField(default=datetime.now,blank=True)
    schedule_end = models.DateTimeField(default=datetime.now,blank=True)
    profit = models.FloatField()
    def __unicode__(self):
        return str(self.schedule)

    def __str__(self):
        return str(self.schedule)



class Customer(models.Model):
    class Meta:
        unique_together = (('name', 'contact'),)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=11)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("appointcreate", kwargs={"cid":self.id})

class Store(models.Model):
    class Meta:
        unique_together = (('name', 'address'),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    def __unicode__(self):
        return self.address

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("store", kwargs={"id":self.id})

class Offer(models.Model):
    name = models.CharField(max_length = 100, null = False, blank = False)
    offer = models.FloatField(null = False, blank = False)
    treatment = models.ManyToManyField('Treatment', blank = True)
    end_date = models.DateTimeField(default = datetime.now, blank = True)
    store = models.ForeignKey('Store', on_delete=models.DO_NOTHING)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
