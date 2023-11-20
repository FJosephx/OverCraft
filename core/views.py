from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from typing import Awaitable
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Producto, Boleta, Carrito, DetalleBoleta, Bodega, Perfil
from .forms import ProductoForm,PerfilUsuarioForm, BodegaForm, RegistroClienteForm, IngresarForm
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.contrib import messages
from .tools import eliminar_registro, verificar_eliminar_registro
from core.templatetags.custom_filters import formatear_dinero, formatear_numero
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
            return redirect('password_cambiada')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {'form': form}
    return render(request, 'core/cambiar_password.html', context)


def home(request):
    
    buscar = ''
    if request.method == 'POST':
        buscar = request.POST.get('buscar')
        registros = Producto.objects.filter(nombre__icontains=buscar).order_by('nombre')
    else:
        registros = Producto.objects.all().order_by('nombre')

    productos = []
    
    for registro in registros:
        productos.append(obtener_info_producto(registro.id))

    data = { 
        'productos': productos,
        'titulo': 'Home | ServiExpress',
        'buscar': buscar 
        }
    
    return render(request, 'core/index.html', data)
     
def ropa(request):
    data = {'titulo': 'Concurso de Ropa'}
    return render(request, 'core/ropa.html', data)

def ficha(request, producto_id):

    context = obtener_info_producto(producto_id)


    return render(request, 'core/ficha.html', context)

def registro(request):
    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                user=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            return redirect(iniciar_sesion)
            
    return render(request, "core/registro.html", {'form': form})

def iniciar_sesion(request):
    comprar = request.GET.get('comprar', False)
    agregar_carrito = request.GET.get('agregar_carrito', False)


    mensaje = ""

    if request.method == "POST":
        form = IngresarForm(request.POST)
        if form.is_valid():
            username    = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)


            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(home)
            messages.error(request, 'La cuenta o la password no son correctos')

    if comprar:
        mensaje = 'Para comprar, inicia sesión'
    elif agregar_carrito:
        mensaje = "Para agregar al carrito, inicia sesión"
    else:
        mensaje = "Inicia sesión"
    
    return render(request, "core/iniciar_sesion.html", {
        'form':  IngresarForm(),
        'perfiles': Perfil.objects.all(),
        'mensaje':mensaje
    })


def administracion(request):
    data = {'titulo': 'Administracion'}
    return render(request, 'core/administracion.html',data)

def bodega(request):

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        producto = Producto.objects.get(id=producto_id)
        cantidad = int(request.POST.get('cantidad'))
        for cantidad in range(1, cantidad + 1):
            Bodega.objects.create(producto=producto)
        if cantidad == 1:
            messages.success(request, f'Se ha agregado 1 nuevo "{producto.nombre}" a la bodega')
        else:
            messages.success(request, f'Se han agregado {cantidad} productos de "{producto.nombre}" a la bodega')

    registros = Bodega.objects.all()
    lista = []
    for registro in registros:
        vendido = DetalleBoleta.objects.filter(bodega=registro).exists()
        item = {
            'bodega_id': registro.id,
            'nombre_categoria': registro.producto.categoria.nombre,
            'nombre_producto': registro.producto.nombre,
            'estado': 'Vendido' if vendido else 'En bodega',
            'imagen': registro.producto.imagen,
        }
        lista.append(item)

    return render(request, 'core/bodega.html', {
        'form': BodegaForm(),
        'productos': lista,
    })
    # data = {'titulo': 'Bodega'}
    # return render(request, 'core/bodega.html',data)

def boleta(request, nro_boleta):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    detalle_boleta = DetalleBoleta.objects.filter(boleta=boleta)
    datos = { 
        'boleta': boleta, 
        'detalle_boleta': detalle_boleta 
    }
    return render(request, 'core/boleta.html', datos)

def cambiar_estado_boleta(request, nro_boleta, estado):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    if estado == 'Anulado':
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    else:
        if estado == 'Vendido':
            boleta.fecha_venta = date.today()
            boleta.fecha_despacho = None
            boleta.fecha_entrega = None
        elif estado == 'Despachado':
            boleta.fecha_despacho = date.today()
            boleta.fecha_entrega = None
        elif estado == 'Entregado':
            if boleta.estado == 'Vendido':
                boleta.fecha_despacho = date.today()
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Despachado':
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Entregado':
                boleta.fecha_entrega = date.today()
    boleta.estado = estado
    boleta.save()
    return redirect(ventas)

def miscompras(request):

    user = User.objects.get(username='usuario_cliente')
    perfil = Perfil.objects.get(user=user)

    boletas = Boleta.objects.filter(cliente=perfil)
    historial =[]
    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)
    return render(request, 'core/miscompras.html', { 
        'historial': historial 
    })

def misdatos(request):
    data = {"mesg": "", "form": PerfilUsuarioForm}

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            perfil = Perfil.objects.get(user=user)
            perfil.rut = request.POST.get("rut")
            perfil.direccion = request.POST.get("direccion")
            perfil.save()
            data["mesg"] = "¡Sus datos fueron actualizados correctamente!"

    perfil = Perfil.objects.get(user=request.user)
    form = PerfilUsuarioForm()
    form.fields['first_name'].initial = request.user.first_name
    form.fields['last_name'].initial = request.user.last_name
    form.fields['email'].initial = request.user.email
    form.fields['rut'].initial = perfil.rut
    form.fields['direccion'].initial = perfil.direccion
    data["form"] = form
    return render(request, "core/misdatos.html", data)

def nosotros(request):
    data = {'titulo': 'Nosotros'}
    return render(request, 'core/nosotros.html',data)

def usuarios(request):
    usuarios = Perfil.objects.all()

    data = {
        # 'form': form,
        'usuarios': usuarios
    }
    return render(request, 'core/usuarios.html',data)

def obtener_productos(request):
    categoria_id = request.GET.get('categoria_id')
    productos = Producto.objects.filter(categoria_id=categoria_id)
    data = [
        {
            'id': producto.id, 
            'nombre': producto.nombre, 
            'imagen': producto.imagen.url
        } for producto in productos
    ]
    return JsonResponse(data, safe=False)


def ventas(request):
    boletas = Boleta.objects.all()
    historial =[]
    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'nom_cliente': f'{boleta.cliente.user.first_name} {boleta.cliente.user.last_name}',
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'subscrito': 'Sí' if boleta.cliente.subscrito else 'No',
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)
    return render(request, 'core/ventas.html', { 
        'historial': historial 
    })

def admin_productos(request,id, accion):
    

    if request.method == 'POST':
    
        if accion == 'crear':
            form = ProductoForm(request.POST, request.FILES)

        elif accion == 'actualizar':
            form = ProductoForm(request.POST, request.FILES, instance=Producto.objects.get(id=id))
        
        if form.is_valid():
            producto = form.save()
            form = ProductoForm(instance=producto)
            messages.success(request, f'El producto "{str(producto)}" se logró {accion} correctamente')
            return redirect(admin_productos, 'actualizar', producto.id)
        else:
            messages.error(request, f'No se pudo {accion} el Producto, pues el formulario no pasó las validaciones básicas')
            return redirect(admin_productos, 'actualizar', id)

    if request.method == 'GET':

        if accion == 'crear':
            form = ProductoForm()
        
        elif accion == 'actualizar':
            form = ProductoForm(instance=Producto.objects.get(id=id))

        elif accion == 'eliminar':
            messages.success(request, eliminar_registro(Producto, id))
            return redirect(admin_productos, 'crear', '0')
        else:
            form = None  # Agregar este caso predeterminado


    productos = Producto.objects.all()

    datos = {
        'form': form,
        'productos': productos
    }

    return render(request, 'core/productos.html',datos)


def obtener_info_producto(producto_id):

    producto = Producto.objects.get(id=producto_id)
    stock = Bodega.objects.filter(producto_id=producto_id).exclude(detalleboleta__isnull=False).count()
    
    # Preparar texto para mostrar estado: en oferta, sin oferta y agotado
    con_oferta = f'<span class="text-primary"> EN OFERTA {producto.descuento_oferta}% DE DESCUENTO </span>'
    sin_oferta = '<span class="text-success"> DISPONIBLE EN BODEGA </span>'
    agotado = '<span class="text-danger"> AGOTADO </span>'

    if stock == 0:
        estado = agotado
    else:
        estado = sin_oferta if producto.descuento_oferta == 0 else con_oferta

    # Preparar texto para indicar cantidad de productos en stock
    # en_stock = f'En stock: {formatear_numero(stock)} {"unidad" if stock == 1 else "unidades"}'
    en_stock = f'<div class="d-flex justify-content-between"><span>En stock: </span> <span> {formatear_numero(stock)} {"unidad" if stock == 1 else "unidades"} </span></div>'

    return {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'imagen': producto.imagen,
        'html_estado': estado,
        'html_precio': obtener_html_precios_producto(producto),
        'html_stock': en_stock,
    }
def calcular_precios_producto(producto):
    precio_normal = producto.precio
    precio_oferta = producto.precio * (100 - producto.descuento_oferta) / 100
    precio_subscr = producto.precio * (100 - (producto.descuento_oferta + producto.descuento_subscriptor)) / 100
    hay_desc_oferta = producto.descuento_oferta > 0
    hay_desc_subscr = producto.descuento_subscriptor > 0
    return precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr

def obtener_html_precios_producto(producto):

    
    
    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(producto)
    
    normal = f'<div class="d-flex justify-content-between"><span>Normal:</span> <span>{formatear_dinero(precio_normal)}</span></div>'
    tachar = f'<div class="d-flex justify-content-between"><span>Normal:</span> <span class="text-decoration-line-through"> {formatear_dinero(precio_normal)} </span></div>'
    oferta = f'<div class="d-flex justify-content-between"><span>Oferta:</span> <span class="text-success fw-bold"> {formatear_dinero(precio_oferta)} </span></div>'
    subscr = f'<div class="d-flex justify-content-between"><span>Subscrito:</span> <span class="text-danger fw-bold"> {formatear_dinero(precio_subscr)} </span></div>'

    if hay_desc_oferta > 0:
        texto_precio = f'{tachar}{oferta}'
    else:
        texto_precio = normal

    if hay_desc_subscr > 0:
        texto_precio += f'{subscr}'

    return texto_precio

def salir(request):
    logout(request)
    return redirect(home)

def eliminar_producto_en_bodega(request, bodega_id):
    
    nombre_producto = Bodega.objects.get(id=bodega_id).producto.nombre
    eliminado, error = verificar_eliminar_registro(Bodega, bodega_id, True)
    
    if eliminado:
        messages.success(request, f'Se ha eliminado el ID {bodega_id} ({nombre_producto}) de la bodega')
    else:
        messages.error(request, error)

    return redirect(bodega)


def poblar(request):
    poblar_bd()
    return redirect(home)

def carrito(request):

    detalle_carrito = Carrito.objects.filter(cliente=request.user.perfil)

    total_a_pagar = 0
    for item in detalle_carrito:
        total_a_pagar += item.precio_a_pagar
    monto_sin_iva = int(round(total_a_pagar / 1.19))
    iva = total_a_pagar - monto_sin_iva

    return render(request, 'core/carrito.html', {
        'detalle_carrito': detalle_carrito,
        'monto_sin_iva': monto_sin_iva,
        'iva': iva,
        'total_a_pagar': total_a_pagar,
    })


def eliminar_producto_en_carrito(request, carrito_id):

    Carrito.objects.get(id=carrito_id).delete()

    return redirect(carrito)


def agregar_producto_al_carrito(request, producto_id):

    perfil = request.user.perfil
    producto = Producto.objects.get(id=producto_id)

    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(producto)

    precio = producto.precio
    descuento_subscriptor = producto.descuento_subscriptor if perfil.subscrito else 0
    descuento_total=producto.descuento_subscriptor + producto.descuento_oferta if perfil.subscrito else producto.descuento_oferta
    precio_a_pagar = precio_subscr if perfil.subscrito else precio_oferta
    descuentos = precio - precio_subscr if perfil.subscrito else precio - precio_oferta

    Carrito.objects.create(
        cliente=perfil,
        producto=producto,
        precio=precio,
        descuento_subscriptor=descuento_subscriptor,
        descuento_oferta=producto.descuento_oferta,
        descuento_total=descuento_total,
        descuentos=descuentos,
        precio_a_pagar=precio_a_pagar
    )

    return redirect(ficha, producto_id)