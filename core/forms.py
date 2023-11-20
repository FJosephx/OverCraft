from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, Categoria, Perfil, Bodega
from django.forms.widgets import ClearableFileInput

form_file = {'class': 'form-control-file form-control form-control-sm', 'title': 'Debe subir una imagen'}
form_select = {'class':'form-select form-control form-control-sm'}
form_text_area = {'class': 'form-control form-control-sm', 'rows': 2, 'placeholder':'Ingrese una descripcion'}
form_control = {'class': 'form-control form-control-sm', 'placeholder':'Ingrese el Nombre del Producto'}
form_precio = {'class':'form-control', 'placeholder':'Ingrese el precio'}
form_desc = {'class': 'form-control', 'placeholder':'3%'}
form_descOferta = {'class': 'form-control', 'placeholder':'5%'}
form_file_imagen = {'id':'id_imagen' ,'class': 'form-control-file form-control form-control-sm', 'title': 'Debe subir una imagen'}
form_select_bodega = {'class':'form-select form-control form-control-sm'}

form_text_area_registro = {'class': 'form-control form-control-sm', 'rows': 2, 'placeholder':'Ingrese una direccion'}

form_control_registro = {'class': 'form-control form-control-sm'}
form_control_inicio_sesion = {'class': 'form-control form-control-sm', 'placeholder':'Ingrese su Nombre de Usuario'}
form_control_inicio_sesion_password = {'class': 'form-control form-control-sm', 'placeholder':'Ingrese su Contraseña'}

form_hidden = {'class': 'd-none'}
form_check = {'class': 'form-check-input'}
form_password = {'class': 'form-control text-danger', 'value': '123'}

class ProductoForm(ModelForm):
    
    class Meta:
        model = Producto
        fields = [
                  'nombre', 
                  'descripcion', 
                  'precio', 
                  'descuento_subscriptor',
                  'descuento_oferta', 
                  'imagen', 
                  'categoria', 
                  ]

        widgets = {
            'nombre': forms.TextInput(attrs=form_control),
            'descripcion': forms.Textarea(attrs=form_text_area),
            'precio': forms.NumberInput(attrs=form_precio),
            'descuento_subscriptor': forms.NumberInput(attrs=form_desc),
            'descuento_oferta': forms.NumberInput(attrs=form_descOferta),
            'imagen' : forms.FileInput(attrs=form_file_imagen),
            'categoria' : forms.Select(attrs=form_select),
        } 



class IngresarForm(Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs=form_control_inicio_sesion), label="Cuenta")
    password = forms.CharField(widget=forms.PasswordInput(attrs=form_control_inicio_sesion_password), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

class BodegaForm(forms.Form):

    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Categoría'
    )
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.none(), 
        widget=forms.Select(attrs=form_select_bodega),
        label='Producto'
    )
    cantidad = forms.IntegerField(
        widget=forms.NumberInput(attrs=form_control),
        label='Cantidad'
    )

    class Meta:
        fields = '__all__'


class RegistroClienteForm(UserCreationForm):

    rut = forms.CharField(
        max_length=15, 
        required=True, 
        label='RUT',
        widget=forms.TextInput(attrs=form_control_registro),
    )
    direccion = forms.CharField(
        max_length=400, 
        required=True, 
        label='Dirección',
        widget=forms.Textarea(attrs=form_text_area_registro),
    )
    subscrito = forms.BooleanField(
        required=False,
        label='Subscrito',
        widget=forms.CheckboxInput(attrs=form_check),
    )
    imagen = forms.CharField(
        required=True,
        label='Imagen',
        widget=forms.FileInput(attrs=form_file_imagen),
    )
    
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'rut', 
            'direccion', 
            'subscrito', 
            'imagen', 
            'password1', 
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre Usuario'

        self.fields['username'].widget.attrs.update(form_control_registro)
        self.fields['first_name'].widget.attrs.update(form_control_registro)
        self.fields['first_name'].label = 'Nombre'

        self.fields['last_name'].label = 'Apellido'
        self.fields['email'].label = 'Correo Electronico'

        self.fields['last_name'].widget.attrs.update(form_control_registro)
        self.fields['email'].widget.attrs.update(form_control_registro)
        self.fields['password1'].widget.attrs.update(form_control_registro)
        self.fields['password2'].widget.attrs.update(form_control_registro)

        self.fields['password1'].label = 'Ingrese Contraseña'
        self.fields['password2'].label = 'Repita la Contraseña'
        
class PerfilUsuarioForm(Form):

    first_name = forms.CharField(max_length=150, required=True, label="Nombres",)
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    email = forms.CharField(max_length=254, required=True, label="Correo")
    rut = forms.CharField(max_length=80, required=False, label="Rut")
    direccion = forms.CharField(max_length=80, required=False, label="Dirección")

    class Meta:
        fields = '__all__'
