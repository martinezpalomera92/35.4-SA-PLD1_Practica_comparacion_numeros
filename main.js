// 1. Solicitar los números y convertir a enteros
let num1 = parseInt(prompt("Ingresa el primer número:"));
let num2 = parseInt(prompt("Ingresa el segundo número:"));
let num3 = parseInt(prompt("Ingresa el tercer número:"));

// 2. Obtener referencias a los elementos del DOM
const mensaje = document.getElementById('mensaje');
const ordenMayorAMenor = document.getElementById('ordenMayorAMenor');
const ordenMenorAMayor = document.getElementById('ordenMenorAMayor');

// Función para mostrar el resultado en el DOM
function mostrarResultados(mayor, medio, menor) {
    ordenMayorAMenor.textContent = `Orden de mayor a menor: ${mayor}, ${medio}, ${menor}`;
    ordenMenorAMayor.textContent = `Orden de menor a mayor: ${menor}, ${medio}, ${mayor}`;
}

// 3. Validar que las entradas sean números válidos
if (isNaN(num1) || isNaN(num2) || isNaN(num3)) {
    mensaje.textContent = "Error: Por favor, ingresa números válidos.";
} else {
    // 4. Verificar si los números son iguales
    if (num1 === num2 && num2 === num3) {
        mensaje.textContent = "Los números son iguales.";
    } else {
        // 5. Lógica de ordenamiento y visualización
        if (num1 >= num2 && num1 >= num3) {
            if (num2 >= num3) {
                mostrarResultados(num1, num2, num3);
            } else {
                mostrarResultados(num1, num3, num2);
            }
        } else if (num2 >= num1 && num2 >= num3) {
            if (num1 >= num3) {
                mostrarResultados(num2, num1, num3);
            } else {
                mostrarResultados(num2, num3, num1);
            }
        } else {
            if (num1 >= num2) {
                mostrarResultados(num3, num1, num2);
            } else {
                mostrarResultados(num3, num2, num1);
            }
        }
    }
}


/* let num1 = parseInt(prompt("Enter first number:"));
let num2 = parseInt(prompt("Enter second number:"));
let num3 = parseInt(prompt("Enter third number:"));

if (isNaN(num1) || isNaN(num2) || isNaN(num3)) {
    console.log("Please enter valid numbers.");
} else {

    // Verifica si los tres números son iguales
    if (num1 === num2 && num2 === num3) {
        console.log("Los números son iguales.");
    } else
        if (num1 >= num2 && num1 >= num3) {
            if (num2 >= num3) {
                console.log(`Orden de mayor a menor: ${num1}, ${num2}, ${num3}`);
                console.log(`Orden de menor a mayor: ${num3}, ${num2}, ${num1}`);
            } else {
                console.log(`Orden de mayor a menor: ${num1}, ${num3}, ${num2}`);
                console.log(`Orden de menor a mayor: ${num2}, ${num3}, ${num1}`);
            }
        } else if (num2 >= num1 && num2 >= num3) {
            if (num1 >= num3) {
                console.log(`Orden de mayor a menor: ${num2}, ${num1}, ${num3}`);
                console.log(`Orden de menor a mayor: ${num3}, ${num1}, ${num2}`);
            } else {
                console.log(`Orden de mayor a menor: ${num2}, ${num3}, ${num1}`);
                console.log(`Orden de menor a mayor: ${num1}, ${num3}, ${num2}`);
            }
        } else {
            if (num1 >= num2) {
                console.log(`Orden de mayor a menor: ${num3}, ${num1}, ${num2}`);
                console.log(`Orden de menor a mayor: ${num2}, ${num1}, ${num3}`);
            } else {
                console.log(`Orden de mayor a menor: ${num3}, ${num2}, ${num1}`);
                console.log(`Orden de menor a mayor: ${num1}, ${num2}, ${num3}`);
            }
        }
}
        */