from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Comuna, Region, Inmuebles


class UserForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre')
    first_name.label = 'Nombre'
    last_name = forms.CharField(label='Apellido')
    last_name.label = 'Apellido'
    email = forms.EmailField(label='Correo')
    email.label = 'Correo'

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme contraseña', widget=forms.PasswordInput)
    username = forms.CharField(label='Nombre de usuario', max_length=150, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        labels = {'username': _("Nombre de usuario")}


class TipoForm(forms.Form):
    tipos = ((1, 'Arrendatario'), (2, 'Arrendador'),)
    tipo = forms.ChoiceField(label='Tipo', choices=tipos)
    rut = forms.CharField(label='Rut', max_length=100)
    direccion = forms.CharField(label='Dirección', max_length=100)
    telefono = forms.CharField(label='Teléfono', max_length=100)


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre')
    first_name.label = 'Nombre'
    last_name = forms.CharField(label='Apellido')
    last_name.label = 'Apellido'
    email = forms.EmailField(label='Correo')
    email.label = 'Correo'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class InmuebleForm(forms.Form):
    tipos = ((1, "Casa"), (2, "Departamento"), (3, "Estacionamiento"), (4, "Bodega"), (5, "Negocio"),(6, "Negocio"))
    id_tipo_inmueble = forms.ChoiceField(choices=tipos)
    comunas = [(x.id, x.comuna) for x in list(Comuna.objects.filter())]

    def nombre_comuna(e):
        return e[1]
    comunas.sort(key=nombre_comuna)

    id_comuna = forms.ChoiceField(choices=comunas)
    regiones = [(x.id,x.region) for x in list(Region.objects.filter())]
    id_region = forms.ChoiceField(choices=regiones)
    nombre_inmueble = forms.CharField(label='Nombre Inmueble', max_length=100)
    descripcion = forms.CharField(label='Descripción del inmueble', max_length=100)
    terreno_construido = forms.CharField(label='M2 construidos', max_length=100)
    terreno = forms.CharField(label='M2 de terreno', max_length=100)
    numero_estacionamientos = forms.CharField(label='Núm. de estacionamientos', max_length=100)
    numero_banos = forms.CharField(label='Número de baños', max_length=100)
    numero_habitaciones = forms.CharField(label='Número de habitaciones', max_length=100)
    direccion = forms.CharField(label='Dirección', max_length=100)
    imagen = forms.CharField(label="imagen",max_length=100)
    precio_mensual = forms.IntegerField(label='Precio')


class InmueblesUpdateForm(forms.ModelForm):
    class Meta:
        model = Inmuebles
        fields = ['nombre_inmueble', 'descripcion', 'terreno_construido', 'terreno', 'numero_estacionamientos', 'numero_banos', 'numero_habitaciones', 'direccion', 'precio_mensual','imagen']
