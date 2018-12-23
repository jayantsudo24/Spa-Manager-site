from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Store, Employee, Customer, Appointment, Treatment, Offer
from .forms import (
		AppointmentByTimeForm,
		CustomerForm,
		AppointmentForm,
		AppointmentForm1,
		AppointmentForm2,
		OfferForm,
		EmployeeForm,
		TreatForm,
		CustomSearch,
	)
import timedelta
import time
import math
import datetime

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.
store_id=0
Appointment_customer = 0
Appointment_schedule = '0'
Appointment_treatment = 0

def create_treat(request,id=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	form = TreatForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.store = Store.objects.filter(id=id)[0]
		instance.user = request.user
		instance.save()
		return HttpResponseRedirect('/appointment/'+str(id))


	context = {
		"form":form,
	    "store" : us[0],
		"form_name": "Treatment Form",
        }
	return render(request, "custom_form2.html", context)

def treat_list(request, id=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	queryset_list = Treatment.objects.filter(store__id=id)

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(name__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 8)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	if not query:
		queryset = Treatment.objects.filter(store__id=id)

	context = {
		"store_id":id,
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var,
		"store":us[0],
		}
	return render(request, "update_form3.html", context)

def treat_update(request, id=None, aid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Treatment, id=aid)
	form = TreatForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect('/appointment/'+str(id)+'/list_treat')

	context = {
		"store" : us[0],
		"form_name": "Offer Form",
        "form": form,
        }
	return render(request, "custom_form2.html", context)

def treat_delete(request, id=None, aid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Treatment, id=aid)
	instance.delete()
	return HttpResponseRedirect('/appointment/'+str(id)+'/list_treat')


def create_employee(request,id=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	form = EmployeeForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.store = Store.objects.filter(id=id)[0]
		instance.user = request.user
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect('/appointment/'+str(id))

	context = {
		"store" : us[0],
		"form_name": "Employee Form",
        "form": form,
        }
	return render(request, "custom_form2.html", context)

def employee_list(request, id=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	queryset_list = Employee.objects.filter(store__id=id)

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(name__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 8)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	if not query:
		queryset = Employee.objects.filter(store__id=id)

	context = {
		"store_id":id,
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var,
		"store":us[0],
		}
	return render(request, "update_form4.html", context)

def employee_update(request, id=None, aid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Employee, id=aid)
	form = EmployeeForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect('/appointment/'+str(id)+'/list_employee')

	context = {
		"store" : us[0],
		"form_name": "Offer Form",
        "form": form,
        }
	return render(request, "custom_form2.html", context)

def employee_delete(request, id=None, aid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Employee, id=aid)
	instance.delete()
	return HttpResponseRedirect('/appointment/'+str(id)+'/list_employee')

def create_offer(request,id=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	form = OfferForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.store = Store.objects.filter(id=id)[0]
		instance.user = request.user
		clean_data = form.cleaned_data
		treatment = Treatment.objects.in_bulk(clean_data['treatment'])
		del clean_data['treatment']
		instance.save()
		instance.treatment = treatment
		instance.save()
		return HttpResponseRedirect('/appointment/'+str(id))

	form.fields['treatment'].queryset = Treatment.objects.filter(store__id = id)
	context = {
		"store" : us[0],
		"form_name": "Offer Form",
        "form": form,
        }
	return render(request, "custom_form2.html", context)

def offer_list(request, id=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	queryset_list = Offer.objects.all().exclude(id=1).filter(store__id=id)

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(name__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 8)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	if not query:
		queryset = Offer.objects.all().exclude(id=1).filter(store__id=id)

	context = {
		"store_id":id,
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var,
		"store":us[0],
		}
	return render(request, "update_form2.html", context)

def offer_update(request, id=None, aid=None):
	if aid==1:
		return HttpResponseRedirect('/')
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Offer, id=aid)
	form = OfferForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect('/appointment/'+str(id)+'/list_offer')
	form.fields['treatment'].queryset = Treatment.objects.filter(store__id = id)
	context = {
		"store" : us[0],
		"form_name": "Offer Form",
        "form": form,
        }
	return render(request, "custom_form2.html", context)

def offer_delete(request, id=None, aid=None):
	if aid==1:
		return HttpResponseRedirect('/')
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Offer, id=aid)
	instance.delete()
	return HttpResponseRedirect('/appointment/'+str(id)+'/list_offer')


def custom_check(request, id=None):
	us = Store.objects.filter(id=id)
	if request.user.is_authenticated() or us[0].user==request.user:
		queryset_list = Customer.objects.all()
	else:
		context={
			"message":"Please Login, to view appointments"
		}
		return render(request, "login_marker.html", context)

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(name__icontains=query)|
				Q(contact__icontains=query)|
				Q(email__icontains=query)
				).distinct()

	paginator = Paginator(queryset_list, 9)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		"store" : us[0],
		"store_id":id,
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var,
	}
	return render(request, "custom_list.html", context)

def custom_create(request, id=None, contact=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	form = CustomerForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.contact = contact
		instance.user = request.user
		instance.save()
		return HttpResponseRedirect('/appointment/'+str(id)+'/create/'+str(instance.id))

	context = {
		"store": us[0],
		"form_name": "Customer Form",
        "form": form,
        }
	return render(request, "custom_form2.html", context)

def login(request):
	id = ""
	if request.user.is_authenticated():
		if request.user.is_superuser:
			return HttpResponseRedirect('/admin')
		queryset = Store.objects.filter(user=request.user)
		if queryset:
			id = queryset[0].id
	if id != "":
		request.session['username'] = id
		return HttpResponseRedirect('/appointment/'+str(id))
	else:
		return HttpResponseRedirect('/accounts/login')

def appointment_list(request, id=None):
	us = Store.objects.filter(id=id)
	if request.user.is_authenticated() or us[0].user==request.user:
		queryset_list = Customer.objects.all().order_by('schedule').reverse()
	else:
		context={
			"message":"Please Login, to view appointments"
		}
		return render(request, "login_marker.html", context)

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(name__icontains=query)|
			Q(contact__icontains=query)|
			Q(email__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 8)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	if not query:
		queryset = Appointment.objects.filter(Employee__store__id = id).filter(schedule__gt=datetime.datetime.now()).order_by('schedule')

	context = {
		"store_id":id,
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var,
		"store":us[0],
		}
	return render(request, "appoint_list.html", context)

def appointment_set(request, id=None, cid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	m=[]
	form2 = AppointmentForm2(request.POST or None, request.FILES or None)
	f = Treatment.objects.filter(id=request.session['Appointment_treatment'])
	obj = Appointment.objects.exclude(schedule__gt=datetime.datetime.strptime(request.session['Appointment_schedule'],'%Y-%m-%d %H:%M:%S')+f[0].duration).exclude(schedule_end__lt=datetime.datetime.strptime(request.session['Appointment_schedule'],'%Y-%m-%d %H:%M:%S')).filter(Employee__store__id = id)

	if form2.is_valid():
		instance = form2.save(commit=False)
		instance.customer_id = cid
		instance.user = request.user
		instance.treatment_id = request.session['Appointment_treatment']
		if instance.offer.offer is not 1:
			instance.profit = instance.treatment.selling_price * (1 - instance.offer.offer/100) - instance.treatment.cost_price
		else:
			instance.profit = instance.treatment.selling_price - instance.treatment.cost_price
		instance.schedule = datetime.datetime.strptime(request.session['Appointment_schedule'],'%Y-%m-%d %H:%M:%S')
		instance.schedule_end = (instance.schedule + instance.treatment.duration)
		instance.save()
		return HttpResponseRedirect('/appointment/'+str(id)+'/')

	for each in obj:
		if each.Employee.id not in m:
			m.append(each.Employee.id)
	if m:
		c = Employee.objects.filter(store__id = id).exclude(id__in = m)
	else:
		c = Employee.objects.filter(store__id = id)

	d = Offer.objects.filter(id = 1) | Offer.objects.filter(treatment__id = request.session['Appointment_treatment']).filter(end_date__gt = datetime.datetime.now())
	form2.fields['Employee'].queryset = c
	form2.fields['offer'].queryset = d

	context = {
			"form_name": "appointment",
			"form2": form2,
			"offers" : d.exclude(id=1),
			"store" : us[0],
		}
	return render(request, "custom_form1.html", context)


def appointment_create(request, id=None, cid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	m=[]
	msg = ''
	form1 = AppointmentForm1(request.POST or None, request.FILES or None)
	if form1.is_valid():
		instance = form1.cleaned_data
		instance1 = form1.save(commit=False)
		request.session['Appointment_treatment'] = instance1.treatment.id
		a = str(instance.get('date')).split('-')
		schedule = datetime.datetime(int(a[0]),int(a[1]),int(a[2]),int(instance.get('hour')),int(instance.get('minutes')),0)
		request.session['Appointment_schedule'] = str(schedule)[:19]
		f = Treatment.objects.filter(id=request.session['Appointment_treatment'])
		schedule_end = schedule+f[0].duration
		obj = Appointment.objects.exclude(schedule__gt=schedule_end).exclude(schedule_end__lt=schedule).filter(Employee__store__id = id)

		for each in obj:
			if each.Employee.id not in m:
				m.append(each.Employee.id)
		if m:
			c = Employee.objects.filter(store__id = id).exclude(id__in = m)
		else:
			c = Employee.objects.filter(store__id = id)
		if c:
			return HttpResponseRedirect('/appointment/'+str(id)+'/set/'+str(cid)+'/')
		else:
			msg = "No Employee is free"
	form1.fields['treatment'].queryset = Treatment.objects.filter(store__id = id)
	context = {
			"form_name": "appointment",
			"form1": form1,
			"msg" : msg,
			"store":us[0],
		}
	return render(request, "custom_form.html", context)

def appointment_store(request, id=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Store, id=id)
	prof = Appointment.objects.filter(schedule__gt = datetime.datetime.now().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0), schedule__lt = datetime.datetime.now(), Employee__store__id=id)
	profit = 0
	emp = Employee.objects.filter(store__id=id, active=True)
	empc = 0
	for each in emp:
		empc += 1
	for each in prof:
		profit += each.profit

	cs = CustomSearch(request.POST or None)
	if cs.is_valid():
		s = cs.cleaned_data['contact']
		customer = Customer.objects.filter(contact=s)
		if customer:
			return HttpResponseRedirect('/appointment/'+str(id)+'/create/'+str(customer[0].id)+'/')

		return HttpResponseRedirect('/appointment/'+str(id)+'/ccreate/'+s+'/')

	appoint = Appointment.objects.filter(Employee__store__id = id).filter(schedule__gt = datetime.datetime.now())[:5]
	context = {
				"store_id":id,
				"title": instance.address,
				"profit":profit,
				"appoint" : appoint,
				"empc":empc,
				"store":us[0],
				"csearch":cs
			}
	return render(request,"store_detail.html",context)

def appointment_update_others(request, id=None, cid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Appointment, id=cid)
	form = AppointmentForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		"title": "Update",
		"form":form,
		"store":us[0]
	}
	return render(request, "appoint_update_others.html", context)



def appointment_delete(request, id=None, cid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	instance = get_object_or_404(Appointment, id=cid)
	instance.delete()
	context={
		"message":"Appointment has been cancelled",
	}
	return HttpResponseRedirect('/appointment/'+str(id)+'/applist')

def monthly_appointment(request, id=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	form = AppointmentByTimeForm(request.POST or None)
	x = ""
	c = datetime.datetime.now().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
	d = datetime.datetime.now()
	if form.is_valid():
		cd = form.cleaned_data
		c = datetime.datetime.now().replace(month = int(cd.get('months'))).replace(year = int(cd.get('year'))).replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
		if cd.get('months')!="12":
			d = datetime.datetime.now().replace(month = int(cd.get('months'))+1).replace(year = int(cd.get('year'))).replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
		else:
			d = datetime.datetime.now().replace(month = 0).replace(year = int(cd.get('year'))+1).replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
	if c > datetime.datetime.now():
		c = datetime.datetime.now().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
		x = "Future Month : Invalid Input"
	if c.month >= datetime.datetime.now().month and c.year == datetime.datetime.now().year:
		d = datetime.datetime.now()
	prof = Appointment.objects.filter(schedule__gt = c, schedule__lt = d).filter(Employee__store__id = id)
	total = 0
	whours = datetime.timedelta(0,0,0)
	for a in prof:
		total = total + a.profit
		whours = whours + a.treatment.duration
	if whours == datetime.timedelta(0,0,0):
		whours = 'None'

	context = {
		"form":form,
		"object_list" : prof,
		"tocontrib": total,
		"whours":whours,
		"store":us[0],
		"x":x,
	}
	return render(request, "month_list.html", context)

def employee_details(request, id=None, eid=None):
	us = Store.objects.filter(id=id)
	if not request.user.is_authenticated() or us[0].user!=request.user:
		return HttpResponseRedirect('/')
	e = Employee.objects.filter(id=eid)
	emp = e[0]
	store = Store.objects.filter(id=id)
	form = AppointmentByTimeForm(request.POST or None)
	x = ""
	c = datetime.datetime.now().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
	d = datetime.datetime.now()
	if form.is_valid():
		cd = form.cleaned_data
		c = datetime.datetime.now().replace(month = int(cd.get('months'))).replace(year = int(cd.get('year'))).replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
		if cd.get('months')!="12":
			d = datetime.datetime.now().replace(month = int(cd.get('months'))+1).replace(year = int(cd.get('year'))).replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
		else:
			d = datetime.datetime.now().replace(month = 0).replace(year = int(cd.get('year'))+1).replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
	if c > datetime.datetime.now():
		c = datetime.datetime.now().replace(day=1).replace(hour=0).replace(minute=0).replace(second=0)
		x = "Future Month : Invalid Input"
	if c.month >= datetime.datetime.now().month and c.year == datetime.datetime.now().year:
		d = datetime.datetime.now()
	app = Appointment.objects.filter(schedule__gt = c, schedule__lt = d).filter(Employee__store__id = id).filter(Employee__id=eid)
	total = 0
	whours = datetime.timedelta(0,0,0)
	for a in app:
		total = total + a.profit
		whours = whours + a.treatment.duration
	if whours == datetime.timedelta(0,0,0):
		whours = 'None'

	context={
		"emp":emp,
		"store":store[0],
		"tocontrib": total,
		"whours":whours,
		"app":app,
		"filter":form,
		"x":x
	}
	return render(request, "empdet.html", context)
