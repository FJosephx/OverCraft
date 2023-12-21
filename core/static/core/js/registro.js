$(document).ready(function(){



    $.validator.setDefaults({
        messages: {
            required: 'Este campo es obligatorio',
        },
    });

    $('#form').validate({ 
        rules: {
            'username': {
            required: true,
            },
            'first_name': {
            required: true,
            },
            'first_name': {
            required: true,
            },
            'last_name': {
            required: true,
            },
            'email': {
            required: true,
            email: true,
            },
            'password1': {
            required: true,
            minlength: 8,
            },
            'password2': {
            required: true,
            equalTo: '#id_password1'
            }
        },
        messages: {
            'username': {
            required: 'Debe ingresar un nombre de usuario',
            },
            'first_name': {
            required: 'Debe ingresar su nombre',
            },
            'last_name': {
            required: 'Debe ingresar sus apellidos',
            },
            'email': {
            required: 'Debe ingresar su correo',
            email: 'El formato del correo no es válido',
            },
            'password1': {
            required: 'Debe ingresar una contraseña',
            minlength: 'La contraseña debe tener al menos 8 caracteres',
            },
            'password2': {
            required: 'Debe ingresar una contraseña',
            equalTo: 'Debe repetir la contraseña anterior'
            }
        },
        errorPlacement: function(error, element) {
            error.insertAfter(element); // Inserta el mensaje de error después del elemento
            error.addClass('div invalid-feedback fw-bolder'); // Aplica una clase al mensaje de error
            //element.after('<br>'); 
        },
    });

    $('#id_imagen').change(function() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#admin-usuario-imagen').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(input.files[0]);
        }
    });
  
  });