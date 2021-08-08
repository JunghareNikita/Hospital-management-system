from django.db import models
from django.contrib.auth.models import User

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    mobile = models.IntegerField()
    department = models.CharField(max_length=50, choices=departments, default='Cardiologist')
    status = models.BooleanField()

    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    def user_id(self):
        return self.user_id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    mobile = models.IntegerField()
    symptoms = models.CharField(max_length=50)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    status = models.BooleanField()
    dataOfAdmit = models.DateField()

    def get_name(self):
        return self.user.first_name +" "+ self.user.last_name

    def user_id(self):
        return self.user_id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.symptoms)


class Appointment(models.Model):
    doctorId = models.PositiveIntegerField(null=True)
    patientId = models.PositiveIntegerField(null=True)
    doctorName = models.CharField(max_length=40, null=True)
    patientName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

class PatientDischargeDetail(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40)
    assignDoctorName = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    symptom = models.CharField(max_length=100, null=True)

    admitDate = models.DateField(null=True)
    releaseDate = models.DateField(null=True)
    DaySpend = models.PositiveIntegerField(null=True)

    roomCharge = models.PositiveIntegerField(null=True)
    medicineCost = models.PositiveIntegerField(null=True)
    doctorFee = models.PositiveIntegerField(null=True)
    otherCharges = models.PositiveIntegerField(null=True)
    total = models.PositiveIntegerField(null=True)