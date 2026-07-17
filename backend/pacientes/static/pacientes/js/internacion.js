document.addEventListener("DOMContentLoaded", function () {

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

        if (sinSoporte.checked) {

            soportes.forEach(function (soporte) {
                soporte.checked = false;
                soporte.disabled = true;
            });

        } else {

            soportes.forEach(function (soporte) {
                soporte.disabled = false;
            });

        }
    }

    sinSoporte.addEventListener("change", actualizarSoportes);

    soportes.forEach(function (soporte) {

        soporte.addEventListener("change", function () {

            if (this.checked) {
                sinSoporte.checked = false;
            }

            actualizarSoportes();

        });

    });

    actualizarSoportes();

});