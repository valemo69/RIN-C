// ecocardiograma.js
document.addEventListener('DOMContentLoaded', function() {

    // ==========================================================
    // 1. FEVI -> Categoría automática
    // ==========================================================
    const feviInput = document.getElementById('id_fevi');
    const feviCategoriaDisplay = document.getElementById('fevi-categoria-display');

    function actualizarCategoriaFEVI() {
        if (!feviCategoriaDisplay) return;
        const valor = parseFloat(feviInput.value);
        let categoria = '---';
        let color = 'text-white-50';
        if (!isNaN(valor)) {
            if (valor >= 50) {
                categoria = 'Conservada ≥ 50%';
                color = 'text-success';
            } else if (valor >= 40) {
                categoria = 'Levemente reducida 40-49%';
                color = 'text-warning';
            } else if (valor >= 30) {
                categoria = 'Moderadamente reducida 30-39%';
                color = 'text-warning';
            } else if (valor > 0) {
                categoria = 'Severamente reducida < 30%';
                color = 'text-danger';
            }
        }
        feviCategoriaDisplay.textContent = categoria;
        feviCategoriaDisplay.className = color;
    }

    if (feviInput) {
        feviInput.addEventListener('input', actualizarCategoriaFEVI);
        actualizarCategoriaFEVI(); // inicializar
    }

    // ==========================================================
    // 2. Velocidad IT -> Gradiente automático (4v²)
    // ==========================================================
    const velocidadItInput = document.getElementById('id_velocidad_it');
    const gradienteItDisplay = document.getElementById('gradiente-it-display');

    function actualizarGradienteIT() {
        if (!gradienteItDisplay) return;
        const valor = parseFloat(velocidadItInput.value);
        if (!isNaN(valor) && valor > 0) {
            const gradiente = (4 * valor * valor).toFixed(1);
            gradienteItDisplay.textContent = gradiente + ' mmHg';
        } else {
            gradienteItDisplay.textContent = '---';
        }
    }

    if (velocidadItInput) {
        velocidadItInput.addEventListener('input', actualizarGradienteIT);
        actualizarGradienteIT(); // inicializar
    }

    // ==========================================================
    // 3. TAPSE / PAPs -> Índice TAPSE/PASP e interpretación
    // ==========================================================
    const tapseInput = document.getElementById('id_tapse');
    const papsInput = document.getElementById('id_paps');
    const ratioDisplay = document.getElementById('tapse-pasp-ratio-display');
    const interpretacionDisplay = document.getElementById('tapse-pasp-interpretacion-display');

    function actualizarTapsePasp() {
        if (!ratioDisplay || !interpretacionDisplay) return;
        const tapse = parseFloat(tapseInput.value);
        const paps = parseFloat(papsInput.value);
        
        if (!isNaN(tapse) && !isNaN(paps) && paps > 0) {
            const ratio = (tapse / paps).toFixed(2);
            ratioDisplay.textContent = ratio;
            
            let texto, color;
            if (ratio > 0.36) {
                texto = 'Acoplamiento conservado';
                color = 'success';
            } else if (ratio >= 0.30) {
                texto = 'Acoplamiento intermedio (borde)';
                color = 'warning';
            } else {
                texto = 'Acoplamiento alterado (disfunción VD)';
                color = 'danger';
            }
            interpretacionDisplay.textContent = texto;
            interpretacionDisplay.className = 'badge bg-' + color + ' ms-2';
        } else {
            ratioDisplay.textContent = '---';
            interpretacionDisplay.textContent = 'Ingrese TAPSE y PAPs';
            interpretacionDisplay.className = 'badge bg-secondary ms-2';
        }
    }

    if (tapseInput && papsInput) {
        tapseInput.addEventListener('input', actualizarTapsePasp);
        papsInput.addEventListener('input', actualizarTapsePasp);
        actualizarTapsePasp(); // inicializar
    }

    // ==========================================================
    // 4. Trombo -> habilitar/deshabilitar localización
    // ==========================================================
    const tromboCheckbox = document.getElementById('id_trombo_presente');
    const localizacionSelect = document.getElementById('id_trombo_localizacion');

    function actualizarTromboLocalizacion() {
        if (!localizacionSelect) return;
        if (tromboCheckbox.checked) {
            localizacionSelect.disabled = false;
        } else {
            localizacionSelect.disabled = true;
            localizacionSelect.value = '';
        }
    }

    if (tromboCheckbox && localizacionSelect) {
        tromboCheckbox.addEventListener('change', actualizarTromboLocalizacion);
        actualizarTromboLocalizacion(); // inicializar
    }

});