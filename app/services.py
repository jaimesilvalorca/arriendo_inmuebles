from .models import Inmuebles

def crear_inmueble(data):
    nuevo_inmueble = Inmuebles.objects.create(
        nombre_inmueble=data['nombre_inmueble'],
        descripcion=data['descripcion'],
        terreno_construido=data['terreno_construido'],
        terreno=data['terreno'],
        numero_estacionamientos=data['numero_estacionamientos'],
        numero_banos=data['numero_banos'],
        numero_habitaciones=data['numero_habitaciones'],
        direccion=data['direccion'],
        precio_mensual=data['precio_mensual'],
        estado=data['estado']
    )
    return nuevo_inmueble

def listar_inmuebles():
    return Inmuebles.objects.all()

def editar_inmueble(inmueble_id, data):
    inmueble = Inmuebles.objects.get(id=inmueble_id)
    for key, value in data.items():
        setattr(inmueble, key, value)
    inmueble.save()
    return inmueble

def borrar_inmueble(inmueble_id):
    inmueble = Inmuebles.objects.get(id=inmueble_id)
    inmueble.delete()
