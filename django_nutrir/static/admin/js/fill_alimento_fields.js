(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Función para llenar los campos con los datos del alimento SARA seleccionado
        function fillAlimentoFields(alimentoSaraId) {
            if (!alimentoSaraId) return;
            
            // Mostrar indicador de carga
            var loadingMsg = $('<div class="loading-message" style="color: #007cba; font-style: italic;">Cargando datos del alimento SARA...</div>');
            $('#id_alimento_sara').after(loadingMsg);
            
            // Hacer una petición AJAX para obtener los datos del alimento SARA
            $.ajax({
                url: '/alimento/get_alimento_sara/' + alimentoSaraId + '/',
                type: 'GET',
                success: function(data) {
                    try {
                        console.log('Datos recibidos:', data);
                        
                        // Llenar los campos con los datos recibidos (incluyendo valores 0)
                        if (data.nombre !== undefined && data.nombre !== null) {
                            $('#id_nombre').val(data.nombre).trigger('change');
                            console.log('Nombre llenado:', data.nombre);
                        }
                        if (data.cantidad_porcion !== undefined && data.cantidad_porcion !== null) {
                            $('#id_cantidad_porcion').val(data.cantidad_porcion).trigger('change');
                            console.log('Cantidad porción llenada:', data.cantidad_porcion);
                        }
                        if (data.hidratos_carbono !== undefined && data.hidratos_carbono !== null) {
                            $('#id_hidratos_carbono').val(data.hidratos_carbono).trigger('change');
                            console.log('Hidratos llenados:', data.hidratos_carbono);
                        }
                        if (data.proteinas !== undefined && data.proteinas !== null) {
                            $('#id_proteinas').val(data.proteinas).trigger('change');
                            console.log('Proteínas llenadas:', data.proteinas);
                        }
                        if (data.grasas !== undefined && data.grasas !== null) {
                            $('#id_grasas').val(data.grasas).trigger('change');
                            console.log('Grasas llenadas:', data.grasas);
                        }
                        if (data.grasas_totales !== undefined && data.grasas_totales !== null) {
                            $('#id_grasas_totales').val(data.grasas_totales).trigger('change');
                            console.log('Grasas totales llenadas:', data.grasas_totales);
                        }
                        if (data.energia !== undefined && data.energia !== null) {
                            $('#id_energia').val(data.energia).trigger('change');
                            console.log('Energía llenada:', data.energia);
                        }
                        if (data.sodio !== undefined && data.sodio !== null) {
                            $('#id_sodio').val(data.sodio).trigger('change');
                            console.log('Sodio llenado:', data.sodio);
                        }
                        
                        // Mostrar mensaje de éxito
                        loadingMsg.html('<span style="color: #46b450;">✓ Datos cargados exitosamente</span>');
                        setTimeout(function() {
                            loadingMsg.fadeOut();
                        }, 2000);
                        
                        console.log('Campos llenados automáticamente con los datos del alimento SARA');
                    } catch (error) {
                        loadingMsg.html('<span style="color: #dc3232;">✗ Error al procesar los datos</span>');
                        console.log('Error al procesar los datos del alimento SARA:', error);
                    }
                },
                error: function(xhr, status, error) {
                    loadingMsg.html('<span style="color: #dc3232;">✗ Error al cargar los datos</span>');
                    console.log('Error al cargar los datos del alimento SARA:', error);
                }
            });
        }
        
        // Configurar Select2 para el campo alimento_sara
        $('#id_alimento_sara').select2({
            placeholder: 'Buscar alimento de tabla SARA...',
            allowClear: true,
            width: '100%',
            minimumInputLength: 0,
            language: {
                noResults: function() {
                    return "No se encontraron resultados";
                },
                searching: function() {
                    return "Buscando...";
                },
                inputTooShort: function() {
                    return "Escriba al menos un carácter para buscar";
                }
            }
        });
        
        // Manejar el cambio de selección
        $('#id_alimento_sara').on('change', function() {
            var alimentoSaraId = $(this).val();
            if (alimentoSaraId) {
                fillAlimentoFields(alimentoSaraId);
            }
        });
        
        // Agregar "G" a la derecha de los campos nutricionales (excepto kilocalorías)
        function addGIndicators() {
            var nutrientFields = [
                '#id_hidratos_carbono',
                '#id_proteinas', 
                '#id_grasas',
                '#id_grasas_totales',
                '#id_sodio'
            ];
            
            nutrientFields.forEach(function(fieldId) {
                var $field = $(fieldId);
                if ($field.length && !$field.siblings('.g-indicator').length) {
                    $field.after('<span class="g-indicator" style="color: #666; font-weight: bold; font-size: 12px; margin-left: 5px;">G</span>');
                }
            });
        }
        
        // Ejecutar al cargar la página
        addGIndicators();
        
        // Ejecutar cuando se cargan nuevos elementos (por si hay inlines)
        $(document).on('DOMNodeInserted', function() {
            setTimeout(addGIndicators, 100);
        });
    });
})(django.jQuery);
