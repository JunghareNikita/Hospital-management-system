from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from hospital.forms import DoctorDetailForm, DoctorUserForm, PatientDetailForm, PatientUserForm, AppointmentForm, PatientAppointmentForm
from hospital.models import Doctor, Patient, Appointment, PatientDischargeDetail
from datetime import date, datetime

def home(request):
    return render(request, 'home.html')


# =================================== admin signup ====================================

def admin_signup(request):
    if request.method == "POST":
        fn = request.POST.get('first_name')
        ln = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User()
        user.first_name = fn
        user.last_name = ln
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()
        messages.success(request, "registration successful...!")
        group = Group.objects.get_or_create(name='Admin')
        group[0].user_set.add(user)
        return HttpResponseRedirect('adminlogin')
    return render(request, 'admin_signup.html')


# ========================================== doctor signup ========================================
def doctor_signup(request):
    doctorUser = DoctorUserForm()
    doctorDetail = DoctorDetailForm()

    if request.method == "POST":
        user_form = DoctorUserForm(request.POST)
        detail_form = DoctorDetailForm(request.POST, request.FILES)
        if user_form.is_valid() and detail_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = detail_form.save(commit=False)
            doctor.user = user
            doctor.assignedDoctorId = request.POST.get('assignedDoctorId')
            doctor.save()

            messages.success(request, "registration successful...!")
            group = Group.objects.get_or_create(name='Doctor')
            group[0].user_set.add(user)
            return redirect('doctorlogin')

    return render(request, 'doctor_signup.html', {'doctorUser': doctorUser, 'doctorDetail': doctorDetail})

# ========================================== Patient signup ========================================
def patient_signup(request):
    patientUser = PatientUserForm()
    patientDetail = PatientDetailForm()

    if request.method == "POST":
        user_form = PatientUserForm(request.POST)
        detail_form = PatientDetailForm(request.POST, request.FILES)
        if user_form.is_valid() and detail_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            patient = detail_form.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()

            messages.success(request, "registration successful...!")
            group = Group.objects.get_or_create(name='Patient')
            group[0].user_set.add(user)
            return redirect('patientlogin')

    return render(request, 'patient_Signup.html', {'patientUser': patientUser, 'patientDetail': patientDetail})


# =========================  for checking for is an admin or a doctor or a patient ==========================

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()

def is_patient(user):
    return user.groups.filter(name='Patient').exists()


# ========================================= after login views =========================================

def afterLogin_view(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')

    elif is_doctor(request.user):
        accountApproval = Doctor.objects.all().filter(user_id=request.user.id, status=True)
        if accountApproval:
            return redirect('doctor_dashboard')
        else:
            return render(request, 'doctor_wait_for_approval.html')

    elif is_patient(request.user):
        accountApproval = Patient.objects.all().filter(user_id=request.user.id, status=True)
        if accountApproval:
            return redirect('patient_dashboard')
        else:
            return render(request, 'patient_wait_for_approval.html')


# ======================================== admin add doctor and patient =================================================

def admin_add_doctor(request):
    doctorUser = DoctorUserForm()
    doctorDetail = DoctorDetailForm()

    if request.method == "POST":
        doctorUser = DoctorUserForm(request.POST)
        doctorDetail = DoctorDetailForm(request.POST, request.FILES)
        if doctorUser.is_valid() and doctorDetail.is_valid():
            user = doctorUser.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorDetail.save(commit=False)
            doctor.user = user
            doctor.assignedDoctorId = request.POST.get("assignedDoctorId")
            doctor.status = True
            doctor.save()

            group = Group.objects.get_or_create(name="Doctor")
            group[0].user_set.add(user)
            messages.success(request, "successful..!")
            return redirect("admin_add_doctor")
    return render(request, 'admin_add_doctor.html', {'doctorUser':doctorUser, 'doctorDetail':doctorDetail})

@login_required()
def admin_update_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    user = User.objects.get(id=doctor.user_id)

    doctorForm = DoctorUserForm(instance=user)
    doctorDetail = DoctorDetailForm(instance=doctor)

    if request.method == 'POST':
        doctorForm = DoctorUserForm(request.POST, instance=user)
        doctorDetail = DoctorDetailForm(request.POST, request.FILES, instance=doctor)
        if doctorForm.is_valid() and doctorDetail.is_valid():
            user = doctorForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorDetail.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect('admin_view_doctor')
    return render(request, 'admin_update_doctor.html', {'doctorUser':doctorForm, 'doctorDetail':doctorDetail})


@login_required()
def admin_delete_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    user = User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin_view_doctor')

def admin_add_patient(request):
    patientUser = PatientUserForm()
    patientDetail = PatientDetailForm()

    if request.method == "POST":
        patient_user = PatientUserForm(request.POST)
        patient_detail = PatientDetailForm(request.POST, request.FILES)
        if patient_user.is_valid() and patient_detail.is_valid():
            user = patient_user.save()
            user.set_password(user.password)
            user.save()

            patient = patient_detail.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.status = True
            patient.save()

            messages.success(request, "registration successful...!")
            group = Group.objects.get_or_create(name='Patient')
            group[0].user_set.add(user)

            return HttpResponseRedirect('admin_add_patient')
    return render(request, 'admin_add_patient.html', {'patientUser':patientUser, 'patientDetail':patientDetail})


@login_required()
def admin_update_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    user = User.objects.get(id=patient.user_id)

    patientUser = PatientUserForm(instance=user)
    patientDetail = PatientDetailForm(instance=patient)

    if request.method == "POST":
        patientUser = PatientUserForm(request.POST, instance=user)
        patientDetail = PatientDetailForm(request.POST, request.FILES, instance=patient)
        if patientDetail.is_valid() and patientUser.is_valid():
            user = patientUser.save()
            user.set_password(user.password)
            user.save()

            patient = patientDetail.save(commit=False)
            patient.status=True
            patient.save()
            return redirect('admin_view_patient')
    return render(request, 'admin_update_patient.html', {'patientUser':patientUser, 'patientDetail':patientDetail})

@login_required()
def admin_delete_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    user = User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin_view_patient')


# ================================================= admin dashboard =============================================

@login_required()
def admin_dashboard(request):
    doctor_data = Doctor.objects.all().order_by('-id')
    patient_data = Patient.objects.all().order_by('-id')

    totalDoctorCount = Doctor.objects.all().filter(status=True).count()
    pendingDoctorCount = Doctor.objects.all().filter(status=False).count()

    totalPatientCount = Patient.objects.all().filter(status=True).count()
    pendingPatientCount = Patient.objects.all().filter(status=False).count()

    totalAppointment = Appointment.objects.all().filter(status=True).count()
    pendingAppointment = Appointment.objects.all().filter(status=False).count()
    all_data={
        'doctor_data': doctor_data,
        'patient_data': patient_data,
        'totalDoctorCount':totalDoctorCount,
        'pendingDoctorCount':pendingDoctorCount,
        'totalPatientCount':totalPatientCount,
        'pendingPatientCount':pendingPatientCount,
        'totalAppointmentCount':totalAppointment,
        'pendingAppointmentCount':pendingAppointment,
    }
    return render(request, 'admin_dashboard.html', context=all_data)

# ======================================= Admin Doctor Related View Part ====================================

@login_required()
def admin_doctor(request):
    return render(request, 'admin_doctor.html')

@login_required()
def admin_view_doctor(request):
    doctor = Doctor.objects.all().filter(status=True)
    return render(request, 'admin_view_doctor.html', {'doctor': doctor})

@login_required()
def admin_approve_view(request):
    doctor = Doctor.objects.all().filter(status=False)
    return render(request, 'admin_approve_doctor_view.html', {'doctor': doctor})

@login_required()
def admin_approve_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    return redirect(reverse('admin_approve_view'))

@login_required()
def admin_reject_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    user = User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect(reverse('admin_approve_view'))

@login_required()
def admin_view_doctor_specialisation(request):
    doctor = Doctor.objects.all().filter(status=True)
    return render(request, 'admin_view_doctor_specialisation.html', {'doctor':doctor})

# ===================================== End Admin Doctor Related View Part ====================================
# ========================================= Admin Patient Related View ========================================

@login_required()
def admin_patient_view(request):
    return render(request, 'admin_patient.html')

@login_required()
def admin_view_patient(request):
    patient = Patient.objects.all().filter(status=True)
    return render(request, 'admin_view_patient.html', {'patient':patient})

@login_required()
def admin_approve_patient_view(request):
    patient = Patient.objects.all().filter(status=False)
    return render(request, 'admin_approve_patient_view.html', {'patient':patient})

@login_required()
def admin_approve_patient(request, pk):
    patient = Patient.objects.get(id = pk)
    patient.status = True
    patient.save()
    return redirect(reverse('admin_approve_patient_view'))

@login_required()
def admin_reject_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    user = User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect(reverse('admin_approve_patient_view'))


# ========================================= End Admin Patient Related View ========================================

# =================================================Admin Appointment View ====================================

@login_required()
def admin_appointment_view(request):
    return render(request, 'admin_appointment_view.html')

@login_required()
def admin_view_appointment_view(request):
    appointment = Appointment.objects.all().filter(status=True)
    return render(request, 'admin_view_appointment.html', {'appointment':appointment})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_book_appointment(request):
    appointmentForm = AppointmentForm()
    if request.method == "POST":
        appointmentForm = AppointmentForm(request.POST, request.FILES)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = User.objects.get(id=request.POST.get('doctorId'))
            appointment.patientName = User.objects.get(id=request.POST.get('patientId'))
            appointment.status = True
            appointment.save()
            return redirect('admin_book_appointment')
    return render(request, 'admin_book_appointment.html', {'appointment':appointmentForm})

@login_required()
def admin_approve_appointment_view(request):
    appointment = Appointment.objects.all().filter(status=False)
    return render(request, 'admin_approve_appointment_view.html', {'appointment': appointment})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment(request,pk):
    appointment = Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse('admin_approve_appointment_view'))

@login_required()
def admin_reject_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin_approve_appointment_view')

# ====================================== End Admin Appointment View ====================================
# ==================================== Admin Discharging Patient View ================================

@login_required()
def admin_discharge_patient_view(request):
    patient = Patient.objects.all().filter(status=True)
    return render(request, 'admin_discharge_patient_view.html', {'patient':patient})

@login_required()
def discharge_patient_view(request, pk):
    patient = Patient.objects.get(id=pk)
    days = (date.today() - patient.dataOfAdmit)
    assignedDoctor = User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days
    patientDict={
        'patientId': pk,
        'name': patient.get_name,
        'address': patient.address,
        'mobile': patient.mobile,
        'symptoms': patient.symptoms,
        'admitDate': patient.dataOfAdmit,
        'todayDate': date.today(),
        'day': d,
        'assignedDoctorName': assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict = {
            'roomCharge': int(request.POST['roomCharge']) * int(d),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': request.POST['medicineCost'],
            'otherCharges': request.POST['otherCharges'],
            'total': (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + int(
                request.POST['medicineCost']) + int(request.POST['otherCharges'])
        }
        patientDict.update(feeDict)
        PDD = PatientDischargeDetail()
        PDD.patientId = pk
        PDD.patientName = patient.get_name()
        PDD.assignDoctorName = assignedDoctor[0].first_name
        PDD.address = patient.address
        PDD.mobile = patient.mobile
        PDD.symptom = patient.symptoms
        PDD.admitDate = patient.dataOfAdmit
        PDD.releaseDate = date.today()
        PDD.DaySpend = int(d)
        PDD.medicineCost = int(request.POST['medicineCost'])
        PDD.roomCharge = int(request.POST['roomCharge']) * int(d)
        PDD.doctorFee = int(request.POST['doctorFee'])
        PDD.otherCharges = int(request.POST['otherCharges'])
        PDD.total = (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + int(
            request.POST['medicineCost']) + int(request.POST['otherCharges'])
        PDD.save()
        return render(request, 'patient_final_bill.html', {'patientDict':patientDict})
    return render(request, 'generate_patient_bill.html', {'patientDict': patientDict})

# ============================== End Admin Discharging Patient View ================================

# ====================================== End Admin Dashboard ====================================

# ========================================= Doctor Dashboard ==================================

@login_required()
def doctor_dashboard(request):
    patientCount = Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).count()
    appointmentCount = Appointment.objects.all().filter(status=True, doctorId=request.user.id).count()
    dischargePatientCount = PatientDischargeDetail.objects.all().filter(assignDoctorName=request.user).count()
    return render(request, 'doctor_dashboard.html', {'patientCount':patientCount, 'appointmentCount':appointmentCount, 'dischargePatientCount':dischargePatientCount})

@login_required()
def doctor_patient_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    return render(request, 'doctor_patient.html', {'doctor':doctor})

@login_required()
def doctor_view_patient(request):
    patient = Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id)
    doctor = Doctor.objects.get(user_id=request.user.id)
    return render(request, 'doctor_view_patient.html', {'patient': patient, 'doctor':doctor})

@login_required()
def doctor_appointment_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    return render(request, 'doctor_appointment.html', {'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointment = Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointment:
        patientid.append(a.patientId)
    patients = Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointment, patients)
    return render(request, 'doctor_view_appointment.html', {'appointments': appointments, 'doctor': doctor})

@login_required()
def doctor_delete_appointment_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    appointments = Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})

@login_required()
def delete_appointment_view(request, pk):
    appointment = Appointment.objects.get(id=pk)
    appointment.delete()
    doctor = Doctor.objects.get(user_id = request.user.id)
    appointments = Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientId = []
    for a in appointments:
        patientId.append(a.patientId)
    patients = Patient.objects.all().filter(status=True, user_id=patientId)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_delete_appointment.html', {'doctor':doctor, 'appointments':appointments})

@login_required()
def doctor_discharge_patient_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    dischargePatient = PatientDischargeDetail.objects.all().distinct().filter(assignDoctorName=request.user.first_name)
    return render(request, 'doctor_discharge_patient_view.html', {'dischargePatient':dischargePatient, 'doctor':doctor})

# ============================================= End Doctor Dashboard ==================================================
# =============================================== Patient Dashboard ===============================================

@login_required()
def patient_dashboard(request):
    patient = Patient.objects.get(user_id=request.user.id)
    doctor = Doctor.objects.get(user_id= patient.assignedDoctorId)
    context = {'patient':patient, 'doctor':doctor}
    return render(request, 'patient_dashboard.html', context)

def patient_appointment(request):
    patientAppoinmentForm = PatientAppointmentForm()
    patient = Patient.objects.get(user_id=request.user.id)
    message = None
    context = {'appointmentForm': patientAppoinmentForm, 'patient': patient, 'message': message}

    if request.method == "POST":
        patientAppoinmentForm = PatientAppointmentForm(request.POST)
        if patientAppoinmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc = request.POST.get('description')

            doctor = Doctor.objects.get(user_id=request.POST.get('doctorId'))

            if doctor.department == 'Cardiologist':
                if 'heart' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'patient_book_appointment.html', {'appointmentForm': patientAppoinmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Dermatologists':
                if 'skin' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'patient_book_appointment.html', {'appointmentForm': patientAppoinmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Emergency Medicine Specialists':
                if 'fever' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'patient_book_appointment.html', {'appointmentForm': patientAppoinmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Allergists/Immunologists':
                if 'allergy' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'patient_book_appointment.html', {'appointmentForm':patientAppoinmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Anesthesiologists':
                if 'surgery' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'patient_book_appointment.html', {'appointmentForm': patientAppoinmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Colon and Rectal Surgeons':
                if 'cancer' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'patient_book_appointment.html', {'appointmentForm': patientAppoinmentForm, 'patient': patient, 'message': message})

            appointment = patientAppoinmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.user.id
            appointment.doctorName = User.objects.get(id= request.POST.get('doctorId')).first_name
            appointment.patientName = request.user.first_name
            appointment.status = False
            appointment.save()
        return redirect('patient_appointment')

    return render(request, 'patient_book_appointment.html', context)

login_required()
def patient_discharge_view(request):
    patient = Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails = PatientDischargeDetail.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.dataOfAdmit,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].DaySpend,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'otherCharges':dischargeDetails[0].otherCharges,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged': False,
            'patient': patient,
            'patientId': request.user.id,
        }

    return render(request, 'patient_discharge.html', context=patientDict)
# ================================================ End Patient Dashboard ==============================================

