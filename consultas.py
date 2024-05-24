import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arriendo_inmuebles.settings')
django.setup()
from app.models import Inmuebles, Comuna, Region

def consultar_inmuebles_por_comunas():
    inmuebles_por_comunas = Inmuebles.objects.values('id_comuna__comuna', 'nombre_inmueble', 'descripcion')

    with open('log/inmuebles_por_comunas.txt', 'w') as file:
        for inmueble in inmuebles_por_comunas:
            file.write(f"Comuna: {inmueble['id_comuna__comuna']}\n")
            file.write(f"Nombre: {inmueble['nombre_inmueble']}\n")
            file.write(f"Descripción: {inmueble['descripcion']}\n")
            file.write("\n")

def consultar_inmuebles_por_regiones():
    inmuebles_por_regiones = Inmuebles.objects.values('id_region__region', 'nombre_inmueble', 'descripcion')

    with open('log/inmuebles_por_regiones.txt', 'w') as file:
        for inmueble in inmuebles_por_regiones:
            file.write(f"Región: {inmueble['id_region__region']}\n")
            file.write(f"Nombre: {inmueble['nombre_inmueble']}\n")
            file.write(f"Descripción: {inmueble['descripcion']}\n")
            file.write("\n")

consultar_inmuebles_por_comunas()
consultar_inmuebles_por_regiones()
