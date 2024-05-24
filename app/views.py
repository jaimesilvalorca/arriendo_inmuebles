from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from .forms import UserForm,UserUpdateForm,TipoForm,InmuebleForm, InmueblesUpdateForm
from .models import Profile,TipoUser,Inmuebles,Comuna, Region
from django.http import HttpResponseNotAllowed, HttpResponse


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_profile')
    else:
        form = AuthenticationForm(request)
    return render(request, 'auth/login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    tipo_user = profile.id_tipo_user.tipo_user if profile.id_tipo_user else None
    return render(request, 'profile.html', {'user': user, 'profile': profile, 'tipo_user': tipo_user})

@login_required
def create_profile_view(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    return redirect('profile')


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            user = request.user
            print(user.email)
            profile, created = Profile.objects.get_or_create(user=user)
            
            tipo_user_id = int(form.cleaned_data['tipo'])
            tipo_user_instance = TipoUser.objects.get(id=tipo_user_id)
            
            profile.id_tipo_user = tipo_user_instance
            profile.rut = form.cleaned_data['rut']
            profile.direccion = form.cleaned_data['direccion']
            profile.telefono = form.cleaned_data['telefono']
            profile.correo = user.email
            profile.save()
            return redirect('profile') 
    else:
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        form = TipoForm(initial={
            'tipo': profile.id_tipo_user.id if profile.id_tipo_user else None,
            'rut': profile.rut,
            'direccion': profile.direccion,
            'telefono': profile.telefono,
        })
    return render(request, 'profile_update.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect("login")



@login_required
def adminState(request):
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    if profile.id_tipo_user.id == 1:
        if request.method == 'POST':
            form = InmuebleForm(request.POST)
            if form.is_valid():
                comuna_id = int(form.cleaned_data['id_comuna'])
                region_id = int(form.cleaned_data['id_region'])
                comuna = Comuna.objects.get(id=comuna_id)
                region = Region.objects.get(id=region_id)            
                inmueble = Inmuebles(
                    id_tipo_inmueble_id=int(form.cleaned_data['id_tipo_inmueble']),
                    id_comuna=comuna,
                    id_region=region,
                    id_user_id=user_id,
                    nombre_inmueble=form.cleaned_data['nombre_inmueble'],
                    descripcion=form.cleaned_data['descripcion'],
                    terreno_construido=form.cleaned_data['terreno_construido'],
                    terreno=form.cleaned_data['terreno'],
                    numero_estacionamientos=form.cleaned_data['numero_estacionamientos'],
                    numero_banos=form.cleaned_data['numero_banos'],
                    numero_habitaciones=form.cleaned_data['numero_habitaciones'],
                    direccion=form.cleaned_data['direccion'],
                    imagen=form.cleaned_data['imagen'],
                    precio_mensual=form.cleaned_data['precio_mensual'],
                )
                inmueble.save()
                return redirect('estate/<int:inmueble_id>/')
        else:
            form = InmuebleForm()
        return render(request, 'estate/administrator.html', {'profile': profile, 'form': form})  
    else:
        print("Arrendatario", profile.id_tipo_user)
        return render(request, 'estate/administrator.html', {'profile': profile})

@login_required
def update_state(request, inmueble_id):
    inmueble = Inmuebles.objects.get(pk=inmueble_id)
    if request.method == 'POST':
        form = InmueblesUpdateForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            return redirect('estate_detail', inmueble_id=inmueble.id)

    else:
        form = InmueblesUpdateForm(instance=inmueble)
    return render(request, 'estate/update.html', {'form': form})    

@login_required
def detail_state(request, inmueble_id):
    inmueble = Inmuebles.objects.get(pk=inmueble_id)
    return render(request, 'estate/detail.html', {'inmueble': inmueble})

@login_required
def all_estates(request):
    user_id = request.user.id

    inmuebles = Inmuebles.objects.filter(id_user_id=user_id)
    
    for inmueble in inmuebles:
        inmueble.comuna = inmueble.id_comuna.comuna


    for inmueble in inmuebles:
        inmueble.region = inmueble.id_region.region 

    return render(request, 'estate/allestates.html', {'inmuebles': inmuebles})

@login_required

def main(request):
    comunas = Comuna.objects.all()
    regiones = Region.objects.all()
    
    context = {
        'comunas': comunas,
        'regiones': regiones,
    }
    return render(request,'main.html',context)



@login_required
def buscar_inmuebles(request):
    if request.method == 'GET':
        comuna_id = request.GET.get('comuna')
        region_id = request.GET.get('region')
        if comuna_id and region_id:
            inmuebles = Inmuebles.objects.filter(id_comuna=comuna_id, id_region=region_id)
        elif comuna_id:
            inmuebles = Inmuebles.objects.filter(id_comuna=comuna_id)
        elif region_id:
            inmuebles = Inmuebles.objects.filter(id_region=region_id)
        else:
            inmuebles = Inmuebles.objects.all()

        data = [{
                 'id': inmueble.id,
                 'nombre_inmueble': inmueble.nombre_inmueble,
                 'descripcion': inmueble.descripcion,
                 'direccion': inmueble.direccion,
                 'region': inmueble.id_region.region,
                 'comuna': inmueble.id_comuna.comuna,
                 'imagen': inmueble.imagen} for inmueble in inmuebles]

        return JsonResponse({'inmuebles': data})
    else:
        return JsonResponse({'error': 'Método no permitido'})


@login_required
def eliminar_inmueble(request, id):
    if request.method == 'POST':
        try:
            inmueble = Inmuebles.objects.get(id=id)
            inmueble.delete()
            return redirect('allestates')
        except Inmuebles.DoesNotExist:
            return HttpResponse('Inmueble no encontrado', status=404)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def contacto(request):
    return render(request, 'contact.html')
@login_required
def enviar_correo(request):
    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')


        subject = 'Mensaje de contacto desde el sitio web'
        message = f'Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}'
        from_email = 'jaimesilvalorca@gmail.com'
        to_email = ['jaimesilvalorca@gmail.com']


        try:
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            return redirect('index')
        except Exception as e:
            return HttpResponse("Error al enviar el correo electrónico. Por favor, inténtalo de nuevo más tarde.")
    else:
        return HttpResponse("Método no permitido")
    
def render_about(request):
    return render(request,'about.html')
