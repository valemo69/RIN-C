document.addEventListener('DOMContentLoaded', function() {
    // Buscar todos los formularios de resultados MTB
    document.querySelectorAll('.mtb-resultados-form').forEach(function(form) {
        const mtbSelect = form.querySelector('select[name="genexpert_mtb"]');
        const rifDiv = form.querySelector('.genexpert-rif-wrapper');
        const rifCheckbox = rifDiv ? rifDiv.querySelector('input[name="genexpert_rif"]') : null;

        if (!mtbSelect || !rifDiv || !rifCheckbox) return;

        function actualizarRifampicina() {
            const valor = mtbSelect.value;
            if (valor === 'D') { // 'D' = Detectado
                rifDiv.style.display = 'block';
                rifCheckbox.disabled = false;
            } else {
                rifDiv.style.display = 'none';
                rifCheckbox.checked = false;
                rifCheckbox.disabled = true;
            }
        }

        // Escuchar cambios en el select de MTB
        mtbSelect.addEventListener('change', actualizarRifampicina);
        // Ejecutar al cargar la página
        actualizarRifampicina();
    });
});