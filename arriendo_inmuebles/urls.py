"""
URL configuration for arriendo_inmuebles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from app.views import * 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('register/',registro_view, name='registro'),
    path('profile/', profile_view, name='profile'),
    path('crear_perfil/', create_profile_view, name='create_profile'),
    path('profile/updated/', profile_update_view, name='profile_update'),
    path('logout/', signout, name='logout'),
    path('adminstate/',adminState, name='adminstate'),
    path('estate/<int:inmueble_id>/update/', update_state, name='update_state'),
    path('estate/<int:inmueble_id>/', detail_state, name='estate_detail'),
    path('estate/',all_estates,name='allestates'),
    path('index/',main,name='index'),
    path('buscar_inmuebles/', buscar_inmuebles, name='buscar_inmuebles'),
    path('estate/<int:id>/delete/', eliminar_inmueble, name='eliminar'),
    path('contacto/',contacto, name='contacto'),
    path('enviar_contacto/',enviar_correo, name='enviar_contacto'),
    path('about/',render_about, name='about'),

]
