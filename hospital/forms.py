from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment
from . import models

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
        help_texts = {
            'username':None
        }

class DoctorDetailForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address', 'mobile', 'department', 'status']

class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password':forms.PasswordInput()
        }
        help_texts = {
            'username':None
        }

class PatientDetailForm(forms.ModelForm):
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model = Patient
        fields = ['address', 'mobile', 'symptoms', 'status', 'dataOfAdmit']

        widgets = {
            'dataOfAdmit':forms.DateTimeInput(format=('%d-%m-%Y'), attrs={'class':'mtyDateClass', 'id':'datetimepicker1','type':'Date', 'data-target':'#datetimepicker1', 'placeholder':'selete a Date'})
        }

class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model = Appointment
        fields = ['description', 'status']

class PatientAppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model = Appointment
        fields = ['description', 'status']