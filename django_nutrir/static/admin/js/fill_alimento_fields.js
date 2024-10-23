document.addEventListener('DOMContentLoaded', function() {
    const alimentoSaraField = document.querySelector('#id_alimento_sara');
    if (alimentoSaraField) {
        alimentoSaraField.addEventListener('change', function() {
            const selectedAlimento = this.value;
            if (selectedAlimento) {
                fetch(`/alimento/get_alimento_sara/${selectedAlimento}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.nombre) {
                            document.querySelector('#id_nombre').value = data.nombre;
                            document.querySelector('#id_cantidad_porcion').value = data.cantidad_porcion;
                            document.querySelector('#id_hidratos_carbono').value = data.hidratos_carbono;
                            document.querySelector('#id_proteinas').value = data.proteinas;
                            document.querySelector('#id_grasas').value = data.grasas;
                            document.querySelector('#id_grasas_totales').value = data.grasas_totales;
                            document.querySelector('#id_energia').value = data.energia;
                            document.querySelector('#id_sodio').value = data.sodio;
                        }
                    });
            }
        });
    }
});