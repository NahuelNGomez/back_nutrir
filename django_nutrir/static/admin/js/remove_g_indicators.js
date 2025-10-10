// Script para eliminar indicadores de globalización (G) de los campos numéricos
document.addEventListener('DOMContentLoaded', function() {
    // Solo ejecutar en páginas de admin de Alimento, no en otras páginas
    if (!window.location.pathname.includes('/admin/alimento/alimento/')) {
        return;
    }
    // Buscar todos los campos de nutrientes
    const nutrientFields = document.querySelectorAll('.nutrient-field');
    
    nutrientFields.forEach(function(field) {
        // Eliminar cualquier indicador de globalización
        field.style.backgroundImage = 'none';
        field.style.backgroundPosition = 'right 8px center';
        field.style.backgroundRepeat = 'no-repeat';
        
        // Asegurar que el campo no tenga indicadores G
        if (field.type === 'number') {
            field.setAttribute('data-localization', 'false');
        }
    });
    
    // Observar cambios en el DOM para campos dinámicos
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                const addedNodes = Array.from(mutation.addedNodes);
                addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        const newFields = node.querySelectorAll ? node.querySelectorAll('.nutrient-field') : [];
                        newFields.forEach(function(field) {
                            field.style.backgroundImage = 'none';
                            field.setAttribute('data-localization', 'false');
                        });
                    }
                });
            }
        });
    });
    
    // Observar cambios en el formulario
    const form = document.querySelector('form');
    if (form) {
        observer.observe(form, { childList: true, subtree: true });
    }
});
