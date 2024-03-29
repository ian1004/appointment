from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone

# Create your views here.

def homepage(request):
	return render(request,'index.html')

def aboutpage(request):
	return render(request,'about.html')

def login_admin(request):
	error = ""
	if request.method == 'POST':
		u = request.POST['username']
		p = request.POST['password']
		user = authenticate(username=u,password=p)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminlogin.html',d)

def loginpage(request):
	error = ""
	page = ""
	if request.method == 'POST':
		u = request.POST['email']
		p = request.POST['password']
		user = authenticate(request,username=u,password=p)
		try:
			if user is not None:
				login(request,user)
				error = "no"
				g = request.user.groups.all()[0].name
				if g == 'Doctor':
					page = 'doctor'
					d = {'error': error, 'page':page}
					return render(request,'doctorhome.html',d)
				elif g == 'Receptionist':
					page = 'reception'
					d = {'error': error, 'page':page}
					return render(request,'receptionhome.html',d)
				elif g == 'Patient':
					page = 'patient'
					d = {'error': error, 'page':page}
					return render(request,'patienthome.html',d)
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
			#print(e)
			#raise e
	return render(request,'login.html')

def createaccountpage(request):
	error = ""
	user="none"
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword = request.POST['repeatpassword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['dateofbirth']
		bloodgroup = request.POST['bloodgroup']
		try:
			if password == repeatpassword:
				Patient.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
				user = User.objects.create_user(name=name,email=email,password=password,username=email)
				pat_group = Group.objects.get(name='Patient')
				pat_group.user.set.add(user)
				#print(pat_group)
				user.save()
				#print(user)
				error = "no"
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
			print("Erorr:",e)
	d = {'error' : error}
	#print(error)
	return render(request,'createaccount.html',d)
	#return render(request,'createaccount.html')

def adminaddDoctor(request):
	error = ""
	user ="none"
	if not request.user.is_staff:
		return redirect('login_admin')

	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword = request.GET.get('repeatpassword')
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.GET.get('birthdate')
		bloodgroup = request.POST['bloodgroup']
		specialization = request.POST['specialization']

		try:
			if password == repeatpassword:
				Doctor.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup, specialization=specialization)
				user = User.objects.create_user(firt_name=name,email=email,password=password,username=email)
				doc_group = Group.objects.get(name='Doctor')
				doc_group.user.set.add(user)
				user.save()
				error = "no"
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminadddoctor.html',d)
	
def adminviewDoctor(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	doc = Doctor.objects.all()
	d = { 'doc' : doc }
	return render(request,'adminviewDoctors.html',d)

def admin_delete_doctor(request,pid,email):
	if not request.user.is_staff:
		return redirect('login_admin')
	doctor = Doctor.objects.get(id=pid)
	doctor.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('adminviewDoctor')

def patient_delete_appointment(request,pid):
	if not request.user.is_active:
		return redirect('loginpage')
	appointment = Appointment.objects.get(id=pid)
	appointment.delete()
	return redirect('viewappointments')

def adminaddReceptionist(request):
	error = ""
	user = "none"
	if not request.user.is_staff:
		return redirect('login_admin')
	
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword = request.POST['repeatpassword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['birthdate']
		bloodgroup = request.POST['bloodgroup']

		try:
			if password == repeatpassword:
				Receptionist.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
				user = User.objects.create_user(firt_name=name,email=email,password=password,username=email)
				rec_group = Group.objects.get(name='Receptionist')
				rec_group.user.set.add(user)
				#print(pat_group)
				user.save()
				#print(user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	
	d = {'error' : error}
	return render(request,'adminaddreceptionist.html',d)

def adminviewReceptionist(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	rec = Receptionist.objects.all()
	r = { 'rec' : rec }
	return render(request,'adminviewreceptionists.html',r)

def admin_delete_receptionist(request,pid,email):
	if not request.user.is_staff:
		return redirect('login_admin')
	reception = Receptionist.objects.get(id=pid)
	reception.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('adminviewReceptionist')

def adminviewAppointment(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	upcoming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
	#print("Upcoming Appointment",upcoming_appointments)
	previous_appointments = Appointment.objects.filter(appointmentdate__lte=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')
	#print("Previous Appointment",previous_appointments)
	d = { "upcoming_appointments" : upcoming_appointments, "previous_appointments" : previous_appointments }
	return render(request,'adminviewappointments.html',d)


def Logout(request):
	if not request.user.is_active:
		return redirect('loginpage')
	logout(request)
	return redirect('loginpage')

def Logout_admin(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	logout(request)
	return redirect('login_admin')

def AdminHome(request):
	#after login user comes to this page
	if not request.user.is_staff:
		return redirect('login_admin')
	return render(request,'adminhome.html')

def Home(request):
	if not request.user.is_active:
		return redirect('loginpage')

	g = request.user.groups.all()[0].name
	if g == 'Doctor':
		return render(request,'doctorhome.html')
	elif g == ' Receptionist':
		return render(request,'receptionhome.html')
	elif g == 'Patient':
		return render(request,'patienthome.html')

def profile(request):
	if not request.user.is_active:
		return redirect('loginpage')

	g = request.user.groups.all()[0].name
	if g == 'Patient':
		patient_details = Patient.objects.all().filter(email=request.user)
		d = { 'patient_details' : patient_details }
		return render(request,'patientprofile.html',d)
	elif g == 'Doctor':
		doctor_details = Doctor.objects.all().filter(email=request.user)
		d = { 'doctor_details' : doctor_details }
		return render(request,'doctorprofile.html',d)
	elif g == 'Receptionist':
		reception_details = Receptionist.objects.all().filter(email=request.user)
		d = { 'reception_details' : reception_details }
		return render(request,'receptionprofile.html',d)

def MakeAppointments(request):
	error = ""
	if not request.user.is_active:
		return redirect('loginpage')
	alldoctors = Doctor.objects.all()
	d = { 'alldoctors' : alldoctors }
	g = request.user.groups.all()[0].name
	if g == 'Patient':
		if request.method == 'POST':
			doctoremail == request.POST['doctoremail']
			doctorname == request.POST['doctorname']
			patientname == request.POST['patientname']
			patientemail == request.POST['patientemail']
			appointmentdate == request.POST['appointmentdate']
			appointmenttime == request.POST['appointmenttime']
			symptoms == request.POST['symptoms']
			try:
				Appointment.objects.create(doctorname=doctorname,doctoremail=doctoremail,patientname=patientname,patientemail=patientemail,appointmentdate=appointmentdate,appointmenttime=appointmenttime,symptoms=symptoms,status=True, prescription="")
				error = "no"
			except:
				error = "yes"
			e = {"error":error}
			return render(request,'patientmakeappointments.html',e)
		elif request.method == 'GET':
			return render(request,'patientmakeappointments.html',d)

def viewappointments(request):
	if not request.user.is_active:
		return redirect('loginpage')
	#print(request.user)
	g = request.user.groups.all()[0].name
	if g == 'Patient':
		upcoming_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
		#print("Upcoming Appointment",upcoming_appointments)
		previous_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__lte=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(patientemail=request.user,status=False).order_by('-appointmentdate')
		#print("Previous Appointment",previous_appointments)
		d = { "upcoming_appointments" : upcoming_appointments, "previous_appointments" : previous_appointments }
		return render(request,'patientviewappointments.html',d)
	elif g == 'Doctor':
		if request.method == 'POST':
			prescriptiondata = request.POST['prescription']
			idvalue = request.POST['idofappointment']
			Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata,status=False)
			#print(idvalue)
			#print(pname)
			#p = {"idvalue":idvalue","pname":pname}
			#return render(request,'doctoraddprescription.html',p)
		upcoming_appointments = Appointment.objects.filter(doctoremail=request.user,appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
		#print("Upcoming Appointment",upcoming_appointments)
		previous_appointments = Appointment.objects.filter(doctoremail=request.user,appointmentdate__lte=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(doctoremail=request.user,status=False).order_by('-appointmentdate')
		#print("Previous Appointment",previous_appointments)
		d = { "upcoming_appointments" : upcoming_appointments, "previous_appointments" : previous_appointments }
		return render(request,'doctorviewappointment.html',d)
	elif g == 'Receptionist':
		upcoming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
		#print("Upcoming Appointment",upcoming_appointments)
		previous_appointments = Appointment.objects.filter(appointmentdate__lte=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')
		#print("Previous Appointment",previous_appointments)
		d = { "upcoming_appointments" : upcoming_appointments, "previous_appointments" : previous_appointments }
		return render(request,'receptionviewappointments.html',d)
