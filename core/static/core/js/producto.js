$(document).ready(function(){



    $.validator.setDefaults({
        messages: {
          required: "Este campo es obligatorio",
        },
    });

    $('#form').validate({ 
        rules: {

            



            'nombre': {
                required: true,
                minlength: 2,
            },
            'descripcion': {
                required: true,
                minlength: 2,
            },
            'precio': {
                required: true,
                digits: true,
                number: true,
            },
            'imagen': {
                required: true,
                // extension: "jpg|jpeg|png"
            },
            'categoria': {
                required: true,
            },

            'descuento_subscriptor': {
                required: true,
                digits: true,
                number: true,
                range: [0, 100],

             },
            'descuento_oferta': {
                required: true,
                digits: true,
                number: true,
                range: [0, 100],

             },

        },
        messages: {

            'nombre': {
                required: 'Debe ingresar el Nombre del Producto',
                minlength: 'Debe ingresar mas de 2 letras'
            },
            'descripcion': {
                required: 'Debe ingresar la descripcion del Producto',
                minlength: 'Debe ingresar mas de 2 letras'
            },
            'precio': {
                required: 'Debe ingresar el precio del producto',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
            },
            'imagen': {
                required: 'Debe ingresar la imagen del producto',
                // extension: "Seleccione una imagen en formato JPG, JPEG, PNG"
            },
            'categoria': {
                required: 'Debe ingresar una categoria',
            },

            'descuento_subscriptor': {
                required: 'Debe Ingresar el Desc. Subscriptor',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
                
                range: 'El descuento debe ser un número entre 0 y 100',


            },
            
            'descuento_oferta': {
                required: 'Debe ingresar un Desc. en Oferta',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
                
                range: 'El descuento debe ser un número entre 0 y 100',


            },


        },
        

        errorPlacement: function(error, element) {
            
            error.insertAfter(element); // Inserta el mensaje de error después del elemento
            // element.addClass('is-invalid');
            error.addClass('div invalid-feedback fw-bolder'); // Aplica una clase al mensaje de error


        },
        


    });

    $('#id_imagen').change(function() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#admin-producto-imagen').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(input.files[0]);
        }
    });
  
  });