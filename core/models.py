from django.core.validators import MinValueValidator, MaxValueValidator
import locale
from django.db import models
from django.contrib.auth.models import User
from core.templatetags.custom_filters import formatear_dinero
from django.db.models import Min
from django.db import connection


# Create your models here
class Categoria(models.Model):
    nombre = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre de la categoría")

    class Meta:
        db_table = 'Categoria'
        verbose_name = "Categoría de producto"
        verbose_name_plural = "Categorías de productos"
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre}'

    def acciones(self):
        return {
            'accion_eliminar': 'eliminar la Categoría',
            'accion_actualizar': 'actualizar la Categoría'
        }


#Modelo para Productos
class Producto(models.Model):
    nombre = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre Producto")
    descripcion = models.CharField(max_length=400, null=True, blank=True, verbose_name="Descripcion Producto")
    precio = models.IntegerField(verbose_name="Precio Producto", blank=False, null=False, )

    descuento_oferta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Descuento Oferta",
        blank=False,
        null=False,
    )

    imagen = models.ImageField(upload_to="images/", null=False, blank=False, verbose_name="Imagen Producto")

    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name="Categoria Producto")

    def __str__(self):
        return f'{self.nombre} (ID {self.id})'

    # class Meta:
    #     db_table = 'Producto'
    #     verbose_name = "Producto"
    #     verbose_name_plural = "Productos"
    #     ordering = ['categoriaProducto', 'nombreProducto']

    def acciones(self):
        return {
            'accion_eliminar': 'eliminar el Producto',
            'accion_actualizar': 'actualizar el Producto'
        }


class Perfil(models.Model):
    USUARIO_CHOICES = [
        ('Cliente', 'Cliente'),
        ('Administrador', 'Administrador'),
        ('Superusuario', 'Superusuario'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        choices=USUARIO_CHOICES,
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Tipo de usuario'
    )
    imagen = models.ImageField(upload_to='perfiles/', blank=False, null=False, verbose_name='Imagen')

    class Meta:
        db_table = 'Perfil'
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"
        ordering = ['tipo_usuario']


class Carrito(models.Model):
    cliente = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    descuento_oferta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto oferta'
    )
    descuento_total = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto total'
    )
    descuentos = models.IntegerField(blank=False, null=False, verbose_name='Descuentos')
    precio_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Precio a pagar')

    class Meta:
        db_table = 'Carrito'
        verbose_name = "Carrito de compras"
        verbose_name_plural = "Carritos de compras"
        ordering = ['cliente', 'producto']

    def __str__(self):
        return f'{self.id} Carrito de {self.cliente.user.first_name} {self.cliente.user.last_name} (Producto {self.producto.categoria.nombre} - {self.producto.nombre} - {formatear_dinero(self.precio)})'

    def acciones(self):
        return {
            'accion_eliminar': 'eliminar el Carrito',
            'accion_actualizar': 'actualizar el Carrito'
        }


class Boleta(models.Model):
    ESTADO_CHOICES = [
        ('Anulado', 'Anulado'),
        ('Vendido', 'Vendido'),
        ('Despachado', 'Despachado'),
        ('Entregado', 'Entregado'),
    ]
    nro_boleta = models.IntegerField(primary_key=True, blank=False, null=False, verbose_name='Nro boleta')
    cliente = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    monto_sin_iva = models.IntegerField(blank=False, null=False, verbose_name='Monto sin IVA')
    iva = models.IntegerField(blank=False, null=False, verbose_name='IVA')
    total_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Total a pagar')
    fecha_venta = models.DateField(blank=False, null=False, verbose_name='Fecha de venta')
    fecha_despacho = models.DateField(blank=True, null=True, verbose_name='Fecha de despacho')
    fecha_entrega = models.DateField(blank=True, null=True, verbose_name='Fecha de entrega')
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=50, blank=False, null=False, verbose_name='Estado')

    class Meta:
        db_table = 'Boleta'
        verbose_name = "Boleta"
        verbose_name_plural = "Boletas"

    def __str__(self):
        return f'Boleta {self.nro_boleta} de {self.cliente.user.first_name} {self.cliente.user.last_name} por {formatear_dinero(self.total_a_pagar)}'

    def acciones(self):
        return {
            'accion_eliminar': 'eliminar la Boleta',
            'accion_actualizar': 'actualizar la Boleta'
        }


class Bodega(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, verbose_name='Producto')

    class Meta:
        db_table = 'Bodega'
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"

    def __str__(self):
        consulta_sql = f'SELECT boleta_id FROM DetalleBoleta WHERE bodega_id={self.id}'
        with connection.cursor() as cursor:
            cursor.execute(consulta_sql)
            resultado = cursor.fetchone()
        info = f'Vendido (Boleta {resultado[0]})' if resultado else 'En bodega'
        return f'{self.producto.nombre} (ID {self.id}) - {info}'

    def acciones(self):
        return {
            'accion_eliminar': 'eliminar el producto de la Bodega',
            'accion_actualizar': 'actualizar el producto de la Bodega'
        }


class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.DO_NOTHING)
    bodega = models.ForeignKey(Bodega, on_delete=models.DO_NOTHING)
    precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
    descuento_oferta = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto oferta'
    )
    descuento_total = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=False,
        null=False,
        verbose_name='Descto total'
    )
    descuentos = models.IntegerField(blank=False, null=False, verbose_name='Descuentos')
    precio_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Precio a pagar')

    class Meta:
        db_table = 'DetalleBoleta'
        verbose_name = "Detalle de boleta"
        verbose_name_plural = "Detalles de boletas"

    def __str__(self):
        minimo_id = DetalleBoleta.objects.filter(boleta_id=self.boleta.nro_boleta).aggregate(minimo_id=Min('id'))[
            'minimo_id']
        nro_item = self.id - minimo_id + 1
        return f'Boleta {self.boleta.nro_boleta} Item {nro_item} {self.bodega.producto.nombre} - {formatear_dinero(self.precio_a_pagar)}'

    def acciones(self):
        return {
            'accion_eliminar': 'eliminar el Detalle de la Boleta',
            'accion_actualizar': 'actualizar el Detalle de la Boleta'
        }
