from django.urls import path
from .views import agregar_producto_al_carrito,eliminar_producto_en_carrito, cambiar_estado_boleta, poblar,obtener_productos,eliminar_producto_en_bodega,salir,admin_productos,ventas, usuarios,home, ropa, ficha, misdatos, nosotros, registro, iniciar_sesion, administracion, bodega, boleta, miscompras, carrito
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from core.views import change_password

urlpatterns = [
    
    path('', home, name='home'),
    path('ropa', ropa, name='ropa'),
    path('ficha/<producto_id>', ficha, name='ficha'),
    path('registro', registro, name='registro'),
    path('iniciar_sesion', iniciar_sesion, name='iniciar_sesion'),
    path('administracion', administracion, name='administracion'),
    path('bodega', bodega, name="bodega"),
    path('boleta', boleta, name='boleta'),
    path('carrito', carrito, name="carrito"),
    path('miscompras', miscompras, name="miscompras"),
    # path('misdatos', misdatos, name="misdatos"),
    path('misdatos', misdatos, name="misdatos"),
    path('nosotros', nosotros, name="nosotros"),
    path('usuarios', usuarios, name="usuarios"),
    # path('productos', productos, name="productos"),
    path('admin_productos/<accion>/<id>', admin_productos, name="admin_productos"),

    path('ventas', ventas, name="ventas"),
    path('poblar', poblar, name='poblar'),
    path('salir', salir, name='salir'),
    path('obtener_productos', obtener_productos, name='obtener_productos'),
    path('boleta/<nro_boleta>', boleta, name='boleta'),
    path('cambiar_estado_boleta/<nro_boleta>/<estado>', cambiar_estado_boleta, name='cambiar_estado_boleta'),
    path('eliminar_producto_en_bodega/<bodega_id>', eliminar_producto_en_bodega, name='eliminar_producto_en_bodega'),
    
    path('password_cambiada/', TemplateView.as_view(template_name='core/password_cambiada.html'), name='password_cambiada'),
    # path('cambiar_password/', auth_views.PasswordChangeView.as_view(template_name='core/cambiar_password.html', success_url='/password_cambiada'), name='cambiar_password'),
    path('cambiar_password/', change_password, name='cambiar_password'),
    path('agregar_producto_al_carrito/<producto_id>', agregar_producto_al_carrito, name='agregar_producto_al_carrito'),

    path('eliminar_producto_en_carrito/<carrito_id>', eliminar_producto_en_carrito, name='eliminar_producto_en_carrito'),

]
