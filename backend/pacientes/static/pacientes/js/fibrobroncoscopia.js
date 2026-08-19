document.addEventListener('DOMContentLoaded', function() {
    const balCheck = document.getElementById('id_bal_realizado');
    const balResult = document.getElementById('id_bal_resultado');
    const biopsiaCheck = document.getElementById('id_biopsia_realizada');
    const biopsiaResult = document.getElementById('id_biopsia_resultado');

    function toggleFields() {
        if (balCheck) {
            balResult.disabled = !balCheck.checked;
        }
        if (biopsiaCheck) {
            biopsiaResult.disabled = !biopsiaCheck.checked;
        }
    }

    if (balCheck) balCheck.addEventListener('change', toggleFields);
    if (biopsiaCheck) biopsiaCheck.addEventListener('change', toggleFields);
    toggleFields(); // estado inicial
});