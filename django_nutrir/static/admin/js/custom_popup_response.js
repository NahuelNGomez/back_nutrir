(function() {
    'use strict';

    // Función para manejar la respuesta del popup de manera más robusta
    function handlePopupResponse() {
        var windowRef = window;
        var windowRefProxy;
        var windowName, widgetName;
        var openerRef = windowRef.opener;
        
        if (!openerRef) {
            // related modal is active
            openerRef = windowRef.parent;
            windowName = windowRef.name;
            widgetName = windowName.replace(/^(change|add|delete|lookup)_/, '');
            if (typeof(openerRef.id_to_windowname) === 'function') {
                // django < 3.1 compatibility
                widgetName = openerRef.id_to_windowname(widgetName);
            }
            windowRefProxy = {
                name: widgetName,
                location: windowRef.location,
                close: function() {
                    if (typeof(openerRef.dismissRelatedObjectModal) === 'function') {
                        openerRef.dismissRelatedObjectModal();
                    }
                }
            };
            windowRef = windowRefProxy;
        }

        // Obtener los datos de respuesta del popup
        var constantsElement = document.getElementById('django-admin-popup-response-constants');
        if (!constantsElement) {
            console.error('No se encontró el elemento django-admin-popup-response-constants');
            return;
        }

        var initData;
        try {
            initData = JSON.parse(constantsElement.dataset.popupResponse);
        } catch (e) {
            console.error('Error al parsear los datos de respuesta del popup:', e);
            return;
        }

        // Manejar la respuesta según el tipo de acción
        switch (initData.action) {
            case 'change':
                if (typeof(openerRef.dismissChangeRelatedObjectPopup) === 'function') {
                    openerRef.dismissChangeRelatedObjectPopup(windowRef, initData.value, initData.obj, initData.new_value);
                } else if (typeof(openerRef.dismissRelatedObjectModal) === 'function') {
                    openerRef.dismissRelatedObjectModal();
                }
                break;
            case 'delete':
                if (typeof(openerRef.dismissDeleteRelatedObjectPopup) === 'function') {
                    openerRef.dismissDeleteRelatedObjectPopup(windowRef, initData.value);
                } else if (typeof(openerRef.dismissRelatedObjectModal) === 'function') {
                    openerRef.dismissRelatedObjectModal();
                }
                break;
            default:
                // Para acciones de 'add' (crear nuevo objeto)
                if (typeof(openerRef.dismissAddRelatedObjectPopup) === 'function') {
                    openerRef.dismissAddRelatedObjectPopup(windowRef, initData.value, initData.obj);
                } else if (typeof(openerRef.dismissAddAnotherPopup) === 'function') {
                    // django 1.7 compatibility
                    openerRef.dismissAddAnotherPopup(windowRef, initData.value, initData.obj);
                } else if (typeof(openerRef.dismissRelatedObjectModal) === 'function') {
                    // Fallback para admin_interface
                    openerRef.dismissRelatedObjectModal();
                } else {
                    console.error('No se encontró función de cierre de popup disponible');
                    // Intentar cerrar la ventana como último recurso
                    if (windowRef.close) {
                        windowRef.close();
                    }
                }
                break;
        }
    }

    // Ejecutar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', handlePopupResponse);
    } else {
        handlePopupResponse();
    }
})();
