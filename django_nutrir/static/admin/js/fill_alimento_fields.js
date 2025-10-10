(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Solo ejecutar en páginas de admin de Alimento, no en otras páginas
        if (!window.location.pathname.includes('/admin/alimento/alimento/')) {
            return;
        }

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
                        
                        // Nutrientes básicos
                        if (data.agua !== undefined && data.agua !== null) {
                            $('#id_agua').val(data.agua).trigger('change');
                            console.log('Agua llenada:', data.agua);
                        }
                        if (data.energia !== undefined && data.energia !== null) {
                            $('#id_energia').val(data.energia).trigger('change');
                            console.log('Energía llenada:', data.energia);
                        }
                        if (data.proteinas !== undefined && data.proteinas !== null) {
                            $('#id_proteinas').val(data.proteinas).trigger('change');
                            console.log('Proteínas llenadas:', data.proteinas);
                        }
                        if (data.lipidos !== undefined && data.lipidos !== null) {
                            $('#id_lipidos').val(data.lipidos).trigger('change');
                            console.log('Lípidos llenados:', data.lipidos);
                        }
                        
                        // Ácidos grasos
                        if (data.acidos_grasos_saturados !== undefined && data.acidos_grasos_saturados !== null) {
                            $('#id_acidos_grasos_saturados').val(data.acidos_grasos_saturados).trigger('change');
                            console.log('Ácidos grasos saturados llenados:', data.acidos_grasos_saturados);
                        }
                        if (data.acidos_grasos_monoinsaturados !== undefined && data.acidos_grasos_monoinsaturados !== null) {
                            $('#id_acidos_grasos_monoinsaturados').val(data.acidos_grasos_monoinsaturados).trigger('change');
                            console.log('Ácidos grasos monoinsaturados llenados:', data.acidos_grasos_monoinsaturados);
                        }
                        if (data.acidos_grasos_poliinsaturados !== undefined && data.acidos_grasos_poliinsaturados !== null) {
                            $('#id_acidos_grasos_poliinsaturados').val(data.acidos_grasos_poliinsaturados).trigger('change');
                            console.log('Ácidos grasos poliinsaturados llenados:', data.acidos_grasos_poliinsaturados);
                        }
                        if (data.colesterol !== undefined && data.colesterol !== null) {
                            $('#id_colesterol').val(data.colesterol).trigger('change');
                            console.log('Colesterol llenado:', data.colesterol);
                        }
                        
                        // Carbohidratos y fibra
                        if (data.hidratos_carbono !== undefined && data.hidratos_carbono !== null) {
                            $('#id_hidratos_carbono').val(data.hidratos_carbono).trigger('change');
                            console.log('Hidratos llenados:', data.hidratos_carbono);
                        }
                        if (data.fibra !== undefined && data.fibra !== null) {
                            $('#id_fibra').val(data.fibra).trigger('change');
                            console.log('Fibra llenada:', data.fibra);
                        }
                        if (data.cenizas !== undefined && data.cenizas !== null) {
                            $('#id_cenizas').val(data.cenizas).trigger('change');
                            console.log('Cenizas llenadas:', data.cenizas);
                        }
                        
                        // Minerales
                        if (data.sodio !== undefined && data.sodio !== null) {
                            $('#id_sodio').val(data.sodio).trigger('change');
                            console.log('Sodio llenado:', data.sodio);
                        }
                        if (data.potasio !== undefined && data.potasio !== null) {
                            $('#id_potasio').val(data.potasio).trigger('change');
                            console.log('Potasio llenado:', data.potasio);
                        }
                        if (data.calcio !== undefined && data.calcio !== null) {
                            $('#id_calcio').val(data.calcio).trigger('change');
                            console.log('Calcio llenado:', data.calcio);
                        }
                        if (data.fosforo !== undefined && data.fosforo !== null) {
                            $('#id_fosforo').val(data.fosforo).trigger('change');
                            console.log('Fósforo llenado:', data.fosforo);
                        }
                        if (data.hierro !== undefined && data.hierro !== null) {
                            $('#id_hierro').val(data.hierro).trigger('change');
                            console.log('Hierro llenado:', data.hierro);
                        }
                        if (data.zinc !== undefined && data.zinc !== null) {
                            $('#id_zinc').val(data.zinc).trigger('change');
                            console.log('Zinc llenado:', data.zinc);
                        }
                        
                        // Vitaminas
                        if (data.niacina !== undefined && data.niacina !== null) {
                            $('#id_niacina').val(data.niacina).trigger('change');
                            console.log('Niacina llenada:', data.niacina);
                        }
                        if (data.folatos !== undefined && data.folatos !== null) {
                            $('#id_folatos').val(data.folatos).trigger('change');
                            console.log('Folatos llenados:', data.folatos);
                        }
                        if (data.vitamina_a !== undefined && data.vitamina_a !== null) {
                            $('#id_vitamina_a').val(data.vitamina_a).trigger('change');
                            console.log('Vitamina A llenada:', data.vitamina_a);
                        }
                        if (data.tiamina !== undefined && data.tiamina !== null) {
                            $('#id_tiamina').val(data.tiamina).trigger('change');
                            console.log('Tiamina llenada:', data.tiamina);
                        }
                        if (data.riboflavina !== undefined && data.riboflavina !== null) {
                            $('#id_riboflavina').val(data.riboflavina).trigger('change');
                            console.log('Riboflavina llenada:', data.riboflavina);
                        }
                        if (data.vitamina_b12 !== undefined && data.vitamina_b12 !== null) {
                            $('#id_vitamina_b12').val(data.vitamina_b12).trigger('change');
                            console.log('Vitamina B12 llenada:', data.vitamina_b12);
                        }
                        if (data.vitamina_c !== undefined && data.vitamina_c !== null) {
                            $('#id_vitamina_c').val(data.vitamina_c).trigger('change');
                            console.log('Vitamina C llenada:', data.vitamina_c);
                        }
                        if (data.vitamina_d !== undefined && data.vitamina_d !== null) {
                            $('#id_vitamina_d').val(data.vitamina_d).trigger('change');
                            console.log('Vitamina D llenada:', data.vitamina_d);
                        }
                        
                        // Campos legacy para compatibilidad
                        if (data.grasas !== undefined && data.grasas !== null) {
                            $('#id_grasas').val(data.grasas).trigger('change');
                            console.log('Grasas llenadas:', data.grasas);
                        }
                        if (data.grasas_totales !== undefined && data.grasas_totales !== null) {
                            $('#id_grasas_totales').val(data.grasas_totales).trigger('change');
                            console.log('Grasas totales llenadas:', data.grasas_totales);
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
        
    });
})(django.jQuery);