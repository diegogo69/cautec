const campoChapaULA = document.querySelector('#cod-bienes');
const btnLimpiarForm = document.querySelector('#limpiar-form');

function formatearChapaULA(e) {
    let valorCampoChapaULA = e.target.value;

    // 1. Remover caracteres no numéricos del campo
    valorCampoChapaULA = valorCampoChapaULA.replace(/\D/g, ''); // \D matches any character that is not a digit (0-9)

    // 2. Aplicar el formato "x-xxxxx-xxxxx"
    let formatoChapaULA = '';
    if (valorCampoChapaULA.length > 0) {
        formatoChapaULA += valorCampoChapaULA.substring(0, 1); // Primer digito
    }
    if (valorCampoChapaULA.length > 1) {
        formatoChapaULA += '-' + valorCampoChapaULA.substring(1, 6); // Siguientes 5 digitos
    }
    if (valorCampoChapaULA.length > 6) {
        formatoChapaULA += '-' + valorCampoChapaULA.substring(6, 11); // Ultimos 5 digitos
    }

    // 3. Actualizar el valor del campo
    e.target.value = formatoChapaULA;
}

function limpiarForm(e) {
    const campoChapaULA = document.querySelector('#cod-bienes');

    console.log('Limpiando formulario...');
    campoChapaULA.value = '1';
    console.log(campoChapaULA.value);
}

campoChapaULA.addEventListener('input', formatearChapaULA);