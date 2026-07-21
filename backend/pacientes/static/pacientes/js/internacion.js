document.addEventListener("DOMContentLoaded", function () {

    // ==========================================================
    // 1. SOPORTE RESPIRATORIO
    // ==========================================================
    const sinSoporte = document.getElementById("sin_soporte");

    const soportes = [
        document.getElementById("oxigeno"),
        document.getElementById("venturi"),
        document.getElementById("cnaf"),
        document.getElementById("vmni"),
        document.getElementById("arm"),
        document.getElementById("traqueostomia"),
    ];

    function actualizarSoportes() {
        if (!sinSoporte) return;

        if (sinSoporte.checked) {
            soportes.forEach(function (soporte) {
                if (soporte) {
                    soporte.checked = false;
                    soporte.disabled = true;
                }
            });
        } else {
            soportes.forEach(function (soporte) {
                if (soporte) soporte.disabled = false;
            });
        }
    }

    if (sinSoporte) {
        sinSoporte.addEventListener("change", actualizarSoportes);

        soportes.forEach(function (soporte) {
            if (soporte) {
                soporte.addEventListener("change", function () {
                    if (this.checked) {
                        sinSoporte.checked = false;
                    }
                    actualizarSoportes();
                });
            }
        });

        actualizarSoportes();
    }

    // ==========================================================
    // 2. TABAQUISMO Y CÁLCULO DE PACK-YEAR
    // ==========================================================
    const radiosTabaquismo = document.querySelectorAll('input[name="tabaquismo"]');
    const inputCig = document.getElementById("id_cigarrillos_por_dia");
    const inputAnos = document.getElementById("id_anos_fumando");
    const inputPack = document.getElementById("id_indice_paquetes_anio");

    // Función para calcular Pack-Year
    function calcularPackYear() {
        if (!inputCig || !inputAnos || !inputPack) return;

        const cig = parseFloat(inputCig.value) || 0;
        const anos = parseFloat(inputAnos.value) || 0;

        if (cig > 0 && anos > 0) {
            const packYear = (cig / 20) * anos;
            // Redondear a 1 decimal
            inputPack.value = packYear % 1 === 0 ? packYear : packYear.toFixed(1);
        } else {
            inputPack.value = '';
        }
    }

    // Función para actualizar estados según la condición seleccionada
    function actualizarTabaquismo() {
        const seleccionado = document.querySelector('input[name="tabaquismo"]:checked');
        
        if (!seleccionado) {
            if (inputCig) inputCig.disabled = true;
            if (inputAnos) inputAnos.disabled = true;
            if (inputPack) inputPack.disabled = true;
            return;
        }

        const label = document.querySelector(`label[for="${seleccionado.id}"]`);
        const texto = label ? label.textContent.trim().toLowerCase() : '';

        if (texto.includes('nunca')) {
            // Si elige 'Nunca fumó', limpiamos y deshabilitamos
            if (inputCig) { inputCig.value = ''; inputCig.disabled = true; }
            if (inputAnos) { inputAnos.value = ''; inputAnos.disabled = true; }
            if (inputPack) { inputPack.value = ''; inputPack.disabled = true; }
        } else {
            // Si elige 'Fumador activo' o 'Exfumador', habilitamos cig/día y años
            if (inputCig) inputCig.disabled = false;
            if (inputAnos) inputAnos.disabled = false;
            if (inputPack) inputPack.disabled = true; // Queda de solo lectura para el cálculo
            
            calcularPackYear();
        }
    }

    // Escuchar eventos de cambio de estado
    radiosTabaquismo.forEach(function (radio) {
        radio.addEventListener("change", actualizarTabaquismo);
    });

    // Escuchar tipeo en Cig/día y Años para recalcular en vivo
    if (inputCig) inputCig.addEventListener("input", calcularPackYear);
    if (inputAnos) inputAnos.addEventListener("input", calcularPackYear);

    actualizarTabaquismo();

});