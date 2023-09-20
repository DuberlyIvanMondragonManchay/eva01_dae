from django.shortcuts import render
from .forms import UserForm 
from django.db import IntegrityError
from .models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def login_view(request):
    if request.method == 'GET':
        return render(request,'login.html',{'user_form': UserForm})
    
    if(request.POST):
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            if(user.password != password):
                return render(request, 'login.html',{'user_form':UserForm,'error': 'Error, Contraseña incorrecta'})
            else:
                return render(request, 'dashboard.html',{'user':user})
        except ObjectDoesNotExist:
            return render(request, 'login.html',{'user_form':UserForm,'error': 'Error, el usuario no existe.'})
 
    return render('login.html',{"error":"Ups ocurrio un error intente de nuevo"})



def register_view(request):
    error = ""
    if request.method == 'GET':
        return render(request, 'register.html', {'user_form': UserForm})
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            new_user = User(name=name, email=email, password=password)
            new_user.save()

            return render(request,'dashboard.html',{"user":new_user})
        except IntegrityError:
            error = "Ups ocurrió un error, inténtalo de nuevo"
            return render(request, 'register.html',{'user_form': UserForm ,'error': error})

def dashborad_view(request):
    if request.method == 'GET':
        return render(request,'dashboard.html')
    
    srt_num_horas = request.POST['num_horas']
    str_pago_horas =request.POST['pago_horas']

    data = calcular_pago_semanal(float(srt_num_horas), float(str_pago_horas))
    return render(request,'dashboard.html',{"data":data})



# Funcion para calcular el pago semanal
def calcular_pago_semanal(horas_trabajadas, pago_por_hora):
    # Horas extras
    if horas_trabajadas <= 48:
        pago_semanal = horas_trabajadas * pago_por_hora
    else:
        horas_normales = 48
        horas_extras = horas_trabajadas - 48
        pago_semanal = (horas_normales * pago_por_hora) + (horas_extras * (pago_por_hora * 2))

    #Bonificación de 50 soles
    pago_semanal += 50
    return pago_semanal





    