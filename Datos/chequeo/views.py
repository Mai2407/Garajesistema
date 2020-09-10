from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import clientesForm
from chequeo.models import clientes
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import date
from datetime import datetime
from django.db.models import Q

now = datetime.now()

# Create your views here.

# -------------------------------------------------------------------
def inicio(request):

    return render(request, 'login.html')


# -------------------------------------------------------------------
@login_required
def index(request):

    return render(request, 'index.html')


# -------------------------------------------------------------------
@login_required
def registrar(request):

    return render(request, 'registrar.html')


# -------------------------------------------------------------------
# Para validar entrada de  usuarios y claves
def user_view(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request,
                        username=username,
                        password=password)

    if user is not None:

        login(request, user)

        return render(request,
                      'index.html')

    else:

        usuarioerror = 0

        context = {

            'usuarioerror': usuarioerror
        }

        return render(request,
                      'login.html',
                      context)

# -------------------------------------------------------------------
# Sacar a los usuarios cuando quiera salir.
@login_required
def out_page(request):

    logout(request)

    return render(request, 'login.html')

# --------------------------------------------------------------------------
# Permite mandar los datos de los formularios a la tabla de la base de datos
@login_required
def date_in(request):

    form = clientesForm(request.POST or None)

    if form.is_valid():

        ingresado = 0

        instance = form.save(commit=False)

        instance.user = request.user

        instance.save()

        form.clean()

        context = {

            'form': form,
            'ingresado': ingresado

        }

        return render(request, 'registrar.html', context)

    elif form.errors.as_data():

        ingresado = 1

        form.clean()

        context = {

            'ingresado': ingresado

        }

        return render(request, 'registrar.html', context)

    else:

        ingresado = 2

        context = {

            'ingresado': ingresado

        }

        return render(request, 'registrar.html', context)

# ------------------------------------------------------------------------
# Permite mostrar los datos de los formularios mandados la base de datos
@login_required
def registrados(request):

    queryset = clientes.objects.all()

    clients = []

    for client in queryset:
        
        if client.vigencia == True:

          dias = datetime.strptime(str(date.today()), '%Y-%m-%d') - datetime.strptime(client.diaentrada, '%Y-%m-%d')
          vehiculo = client.vahiculo
          
          dia = str(dias)

          comparar = dia

          if comparar == "10 days, 0:00:00" or "11 days, 0:00:00" or "12 days, 0:00:00" or "13 days, 0:00:00" or "14 days, 0:00:00" or "15 days, 0:00:00" or "16 days, 0:00:00" or "17 days, 0:00:00" or "18 days, 0:00:00" or "19 days, 0:00:00" or "20 days, 0:00:00" or "21 days, 0:00:00" or "22 days, 0:00:00" or "23 days, 0:00:00" or "24 days, 0:00:00" or "25 days, 0:00:00" or "26 days, 0:00:00" or "27 days, 0:00:00" or "28 days, 0:00:00" or "29 days, 0:00:00" or "30 days, 0:00:00" or "31 days, 0:00:00" or "32 days, 0:00:00" or "33 days, 0:00:00" or "34 days, 0:00:00" or "35 days, 0:00:00" or "36 days, 0:00:00" or "37 days, 0:00:00" : 

              diaFinal = int(dia[0:2])

          elif comparar == "0:00:00":

              diaFinal = 1

          else:

              diaFinal = int(dia[0:1])

          dias = diaFinal
          
          if vehiculo == "motor":

               if now.hour >= 12:

                  precio = diaFinal * 50

               else:

                  precio = diaFinal * 50 - 25


          elif vehiculo == "camion":

               if now.hour >= 12:

                  precio = diaFinal * 100 

               else:

                  precio = diaFinal * 100 - 25

          elif vehiculo == "automovil" or "camioneta":

               if now.hour >= 12:

                  precio = diaFinal * 75 


               else:

                  precio = diaFinal * 75 - 25


          else:
    
                if now.hour >= 12:

                  precio = diaFinal * 150


                else:

                  precio = diaFinal * 150 - 25


          deuda = precio


          temp_client_data = {
            'id': client.id,
            'nombre': client.nombre,
            'cedula': client.cedula,
            'telefono': client.telefono,  
            'marca': client.marca,
            'matricula': client.matricula,
            'diaentrada': client.diaentrada,
            'vahiculo': client.vahiculo,
            'dias': dias,
            'deuda':deuda,
            'vigencia': client.vigencia
          }
          clients.append(temp_client_data)

        else:
            
            dias = 0
            deuda = 0
            temp_client_data = {
            'id': client.id,
            'nombre': client.nombre,
            'cedula': client.cedula,
            'telefono': client.telefono,  
            'marca': client.marca,
            'matricula': client.matricula,
            'diaentrada': client.diaentrada,
            'vahiculo': client.vahiculo,
            'dias': dias,
            'deuda':deuda,
            'vigencia': client.vigencia
           }
            clients.append(temp_client_data)



    # Paginacion permite agrupar por cantida y por paginas los datos.
    paginator = Paginator(clients, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,
        'Paginator': paginator
    }

    return render(request, 'registrado.html', context)

# -------------------------------------------------------------------------------------------
# Permite mostrar los datos de los formularios mandados la base de datos que no estan activos
@login_required
def no_activo(request):

    queryset = clientes.objects.all()

   # Paginacion permite agrupar por cantida y por paginas los datos.
    paginator = Paginator(queryset, 20)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,
        'Paginator': paginator,
    }

    return render(request, 'noactivo.html', context)

# ---------------------------------------------------------------------------------
# Permite eliminar los datos por id de los formularios buscados en la base de datos
@login_required
def delete(request, id):

    queryset = clientes.objects.all()

    clients = []

    for client in queryset:
        
        if client.vigencia == True:

          dias = datetime.strptime(str(date.today()), '%Y-%m-%d') - datetime.strptime(client.diaentrada, '%Y-%m-%d')
          vehiculo = client.vahiculo
          
          dia = str(dias)

          comparar = dia

          if comparar == "10 days, 0:00:00" or "11 days, 0:00:00" or "12 days, 0:00:00" or "13 days, 0:00:00" or "14 days, 0:00:00" or "15 days, 0:00:00" or "16 days, 0:00:00" or "17 days, 0:00:00" or "18 days, 0:00:00" or "19 days, 0:00:00" or "20 days, 0:00:00" or "21 days, 0:00:00" or "22 days, 0:00:00" or "23 days, 0:00:00" or "24 days, 0:00:00" or "25 days, 0:00:00" or "26 days, 0:00:00" or "27 days, 0:00:00" or "28 days, 0:00:00" or "29 days, 0:00:00" or "30 days, 0:00:00" or "31 days, 0:00:00" or "32 days, 0:00:00" or "33 days, 0:00:00" or "34 days, 0:00:00" or "35 days, 0:00:00" or "36 days, 0:00:00" or "37 days, 0:00:00" : 

              diaFinal = int(dia[0:2])

          elif comparar == "0:00:00":

              diaFinal = 1

          else:

              diaFinal = int(dia[0:1])

          dias = diaFinal
          
          if vehiculo == "motor":

               if now.hour >= 12:

                  precio = diaFinal * 50

               else:

                  precio = diaFinal * 50 - 25


          elif vehiculo == "camion":

               if now.hour >= 12:

                  precio = diaFinal * 100 

               else:

                  precio = diaFinal * 100 - 25

          elif vehiculo == "automovil" or "camioneta":

               if now.hour >= 12:

                  precio = diaFinal * 75 


               else:

                  precio = diaFinal * 75 - 25


          else:
    
                if now.hour >= 12:

                  precio = diaFinal * 150


                else:

                  precio = diaFinal * 150 - 25


          deuda = precio


          temp_client_data = {
            'id': client.id,
            'nombre': client.nombre,
            'cedula': client.cedula,
            'telefono': client.telefono,  
            'marca': client.marca,
            'matricula': client.matricula,
            'diaentrada': client.diaentrada,
            'vahiculo': client.vahiculo,
            'dias': dias,
            'deuda':deuda,
            'vigencia': client.vigencia
          }
          clients.append(temp_client_data)


   # Paginacion permite agrupar por cantida y por paginas los datos.
    paginator = Paginator(clients, 20)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    # ----------------------------

    Eliminado = 0

    context = {
               
               'Eliminado': Eliminado,
               'page_obj': page_obj,
               'Paginator': paginator,

              }

    cliente = get_object_or_404(clientes, id=id)

    request.method == 'POST'

    cliente.delete()

    return render(request, 'registrado.html', context)

# -------------------------------------------------------------------------
# Permite mostrar los datos de los formularios buscados en la base de datos
@login_required
def Looking_For_Person(request):

    if request.GET['prs']:

        cliente = request.GET['prs']

        obj = clientes.objects.filter(
               Q(id__icontains=cliente) |
               Q(nombre__icontains=cliente) |
               Q(cedula__icontains=cliente) |
               Q(matricula__icontains=cliente) |
               Q(telefono__icontains=cliente) |
               Q(marca__icontains=cliente)
              )

        clients = []

        for client in obj:

          if client.vigencia == True:

            dias = datetime.strptime(str(date.today()), '%Y-%m-%d') - datetime.strptime(client.diaentrada, '%Y-%m-%d')
            vehiculo = client.vahiculo
          
            dia = str(dias)

            comparar = dia

            if comparar == "10 days, 0:00:00" or "11 days, 0:00:00" or "12 days, 0:00:00" or "13 days, 0:00:00" or "14 days, 0:00:00" or "15 days, 0:00:00" or "16 days, 0:00:00" or "17 days, 0:00:00" or "18 days, 0:00:00" or "19 days, 0:00:00" or "20 days, 0:00:00" or "21 days, 0:00:00" or "22 days, 0:00:00" or "23 days, 0:00:00" or "24 days, 0:00:00" or "25 days, 0:00:00" or "26 days, 0:00:00" or "27 days, 0:00:00" or "28 days, 0:00:00" or "29 days, 0:00:00" or "30 days, 0:00:00" or "31 days, 0:00:00" or "32 days, 0:00:00" or "33 days, 0:00:00" or "34 days, 0:00:00" or "35 days, 0:00:00" or "36 days, 0:00:00" or "37 days, 0:00:00" : 

              diaFinal = int(dia[0:2])

            elif comparar == "1 days, 0:00:00" or "2 days, 0:00:00" or "3 days, 0:00:00" or "4 days, 0:00:00" or "5 days, 0:00:00" or "6 days, 0:00:00" or "7 days, 0:00:00" or "8 days, 0:00:00" or "9 days, 0:00:00": 
              
              diaFinal = int(dia[0:1])

            else:

              diaFinal = int(dia[0:2])

            dias = diaFinal
          
            if vehiculo == "camion":

               if now.hour >= 11:

                  precio = diaFinal * 150


               else:

                  precio = diaFinal * 150 - 50



            elif vehiculo == "automovil" or "camioneta":

               if now.hour >= 11:

                  precio = diaFinal * 75 


               else:

                  precio = diaFinal * 75 - 25


            elif vehiculo == "motor":

                if now.hour >= 11:

                  precio = diaFinal * 50


                else:

                  precio = diaFinal * 50 - 25


            else:
    
                if now.hour >= 11:

                  precio = diaFinal * 75


                else:

                  precio = diaFinal * 75 - 25

 
            deuda = precio


            temp_client_data = {
              'id': client.id,
              'nombre': client.nombre,
              'cedula': client.cedula,
              'telefono': client.telefono,  
              'marca': client.marca,
              'matricula': client.matricula,
              'diaentrada': client.diaentrada,
              'vahiculo': client.vahiculo,
              'dias': dias,
              'deuda': deuda,
              'vigencia': client.vigencia
            }
            clients.append(temp_client_data)

          else:
            
            dias = 0
            deuda = 0
            temp_client_data = {
              'id': client.id,
              'nombre': client.nombre,
              'cedula': client.cedula,
              'telefono': client.telefono,  
              'marca': client.marca,
              'matricula': client.matricula,
              'diaentrada': client.diaentrada,
              'vahiculo': client.vahiculo,
              'dias': dias,
              'deuda': deuda,
              'vigencia': client.vigencia
            }
            clients.append(temp_client_data)


        context = {
            'buscado': clients,
            'query': cliente,
        }

        return render(request, 'registrado.html', context)

    else:

        return HttpResponseRedirect('/registrados/')

# -------------------------------------------------------------------------------------------
# Permite actulizar los datos por id de los formularios buscados en la base de datos
@login_required
def update(request, id):

    obj = get_object_or_404(clientes, id=id)

    form = clientesForm(request.POST or None, instance=obj)

    context = {
        
        'form': form,
    }

    if form.is_valid():

        obj = form.save(commit=False)

        obj.user = request.user

        obj.save()

        form.clean()

        return HttpResponseRedirect('/registrados/')

    return render(request, 'actulizar.html', context)

# ----------------------------------------------------------
# Permite activar o desactivar los datos
@login_required
def activo_or_not(request, id):

    obj = get_object_or_404(clientes, id=id)

    form = clientesForm(request.POST or None, instance=obj)

    context = {

        'form': form,
        
    }

    if form.is_valid():

        obj = form.save(commit=False)

        obj.user = request.user

        obj.save()

        form.clean()

        return HttpResponseRedirect('/registrados/')

    return render(request, 'actulizar.html', context)

# -------------------------------------------------------------------------------------------