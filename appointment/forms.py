from django import forms
from .models import Customer, Appointment, Offer, Treatment, Employee
import timedelta
import datetime

class TreatForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = [
            "name",
            "cost_price",
            "selling_price",
            "description",
        ]
    hours = forms.ChoiceField(choices=[(x, x) for x in range(0, 5)])
    minutes = forms.ChoiceField(choices=[(x, x) for x in range(0, 60, 5)])
    def save(self, commit=True):
        hours = self.cleaned_data.get('hours', None)
        minutes = self.cleaned_data.get('minutes', None)
        seconds = int(minutes)*60+int(hours)*3600
        if seconds!=0:
            self.instance.duration = seconds
        return super(TreatForm, self).save(commit=commit)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "name",
            "address",
            "email",
            "contact",
            "active",
        ]

class CustomSearch(forms.Form):
    contact = forms.CharField(label="",min_length=10,max_length=11,widget=forms.TextInput(attrs={'placeholder': 'Search Contact'}))

class OfferForm(forms.ModelForm):
    treatment = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=Treatment.objects.all(), required = True)
    class Meta:
        model = Offer
        fields = [
            "name",
            "offer",
            "treatment",
            "end_date",
        ]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "address",
            "email",
        ]

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['treatment', 'Employee', 'offer']

class AppointmentForm1(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['treatment']
    date = forms.DateField(label="",widget=forms.DateInput(attrs={'id':'datepicker', 'placeholder':'date'}), initial = datetime.datetime.now())
    hour = forms.ChoiceField(choices=[(x, x) for x in range(6, 21)],initial = datetime.datetime.now().hour)
    minutes = forms.ChoiceField(choices=[(x, x) for x in range(0,60,5)],initial = (datetime.datetime.now().minute/5)*5)

class AppointmentForm2(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['Employee','offer']

class AppointmentByTimeForm(forms.Form):
    t = datetime.datetime.now().year
    months = forms.ChoiceField(choices=[(x, x) for x in range(1, 13)],initial = datetime.datetime.now().month)
    year = forms.ChoiceField(choices=[(x, x) for x in range(t,t-5,-1)],initial = datetime.datetime.now().year)
