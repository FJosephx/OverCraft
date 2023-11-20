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

            'password': {
            required: true,
            // minlength: 8,
            },

        },
        messages: {
            'username': {
            required: 'Debe ingresar un nombre de usuario',
            },

            'password': {
            required: 'Debe ingresar una contraseña',
            // minlength: 'La contraseña debe tener al menos 8 caracteres',
            },

        },
        errorPlacement: function(error, element) {
            error.insertAfter(element); // Inserta el mensaje de error después del elemento
            error.addClass('div invalid-feedback fw-bolder'); // Aplica una clase al mensaje de error
            //element.after('<br>'); 
        },
    });


  });