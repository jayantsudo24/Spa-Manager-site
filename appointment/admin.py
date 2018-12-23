from django.contrib import admin

# Register your models here.

#from .models import Treatment,Employee,Appointment,Customer,Store

#admin.site.register(Treatment,Employee,Appointment,Customer,Store)

from .models import Treatment, Employee, Appointment, Customer, Store, Offer

admin.site.register(Store)
#admin.site.register(Treatment)
