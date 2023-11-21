# ServiExpress
prototipo arquitectura

Manual para ejecutar proyecto:
1. Ejecutar los siguientes comandos en una consola (cmd)

python -m pip install --upgrade pip
pip install --upgrade virtualenv
python -m venv "C:\ProyectosDjango\Arquitectura_venv"
call cd /D "C:\ProyectosDjango"
call Arquitectura_venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install django
pip install pillow
pip install djangorestframework
pip install transbank-sdk
call django-admin startproject Arquitectura
call cd Arquitectura
python manage.py startapp core
python manage.py startapp apirest
pip freeze > requirements.txt
call code "C:\ProyectosDjango\Arquitectura" 

2. Una vez se abra el visual studio code con la consola
 Ejecutar el comando "s" sin comillas y presionar enter para que se inicie el prototipo en el navegador.
 En caso de arrojar error ejecutar "m" sin comillas y presionar enter para que generar el modelo.

3. Datos para entrar al sistema
   
   Administrador:
   user= admin
   password= 123
   
   Usuario:
   user= fr.unda
   password= fr123456
