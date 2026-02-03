let productos = [];
let pedidoActual = [];
let horaActivada = false;
let totalPedido = 0;

let productosDiv;
let pedidoActualDiv;
let btnConfirmar;
let btnLimpiar;

let checkHora;
let inputHora;

// ======================
// INIT
// ======================

document.addEventListener("DOMContentLoaded", () => {

    productosDiv = document.getElementById("productos");
    pedidoActualDiv = document.getElementById("pedido-actual");

    btnConfirmar = document.getElementById("confirmar-pedido");
    btnLimpiar = document.getElementById("limpiar-pedido");

    checkHora = document.getElementById("check-hora");
    inputHora = document.getElementById("hora-input");

    // BOTON HORA

    checkHora.addEventListener("click", () => {

        horaActivada = !horaActivada;

        if (horaActivada) {
            checkHora.classList.add("activo");
            inputHora.disabled = false;
        } else {
            checkHora.classList.remove("activo");
            inputHora.disabled = true;
            inputHora.value = "";
        }
    });

    btnConfirmar.addEventListener("click", confirmarPedido);
    btnLimpiar.addEventListener("click", limpiarPedido);

    cargarProductos();
    renderPedido();
});

// ======================
// CARGAR PRODUCTOS
// ======================

async function cargarProductos() {

    try {

        const res = await fetch("/api/productos");
        productos = await res.json();

        productosDiv.innerHTML = "";

        productos.forEach(prod => {

            const btn = document.createElement("button");

            btn.innerText = `${prod.nombre} (${prod.precio.toFixed(2)} €)`;

            btn.onclick = () => agregarProducto(prod);

            productosDiv.appendChild(btn);
        });

    } catch (e) {
        console.error("Error cargando productos", e);
    }
}

// ======================
// PEDIDO
// ======================

function agregarProducto(producto) {

    pedidoActual.push({
        nombre: producto.nombre,
        precio: Number(producto.precio)
    });

    totalPedido += Number(producto.precio);

    renderPedido();
}

// ======================
// RENDER PEDIDO
// ======================

function renderPedido() {

    pedidoActualDiv.innerHTML = "";

    if (pedidoActual.length === 0) {
        pedidoActualDiv.innerHTML = "<em>(vacío)</em>";
        actualizarTotal();
        return;
    }

    const mapa = {};

    pedidoActual.forEach(item => {

        if (!mapa[item.nombre]) {
            mapa[item.nombre] = {
                nombre: item.nombre,
                precio: item.precio,
                cantidad: 1
            };
        } else {
            mapa[item.nombre].cantidad++;
        }

    });

    const agrupados = Object.values(mapa);

    agrupados.forEach(item => {

        const fila = document.createElement("div");
        fila.className = "pedido-item";

        const texto = document.createElement("span");
        texto.innerText = `${item.nombre} x${item.cantidad} — ${(item.precio * item.cantidad).toFixed(2)} €`;

        const borrar = document.createElement("span");
        borrar.innerText = "❌";
        borrar.style.color = "red";
        borrar.style.cursor = "pointer";
        borrar.style.marginLeft = "10px";

        borrar.onclick = () => eliminarUnidad(item.nombre);

        fila.appendChild(texto);
        fila.appendChild(borrar);

        pedidoActualDiv.appendChild(fila);
    });

    actualizarTotal();
}

// ======================
// ELIMINAR 1 UNIDAD
// ======================

function eliminarUnidad(nombre) {

    const index = pedidoActual.findIndex(p => p.nombre === nombre);

    if (index !== -1) {

        totalPedido -= pedidoActual[index].precio;
        pedidoActual.splice(index, 1);

        renderPedido();
    }
}

// ======================
// TOTAL
// ======================

function actualizarTotal() {

    const totalDiv = document.getElementById("total");

    totalPedido = Math.round(totalPedido * 100) / 100;

    totalDiv.innerText = `TOTAL: ${totalPedido.toFixed(2)} €`;
}

// ======================
// CONFIRMAR PEDIDO
// ======================

async function confirmarPedido() {

    if (pedidoActual.length === 0) {
        alert("No hay productos");
        return;
    }

    const nombre = document.getElementById("nombre").value;
    const telefono = document.getElementById("telefono").value;

    // AGRUPAR PARA BACKEND

    const mapa = {};

    pedidoActual.forEach(item => {

        if (!mapa[item.nombre]) {

            mapa[item.nombre] = {
                nombre: item.nombre,
                precio: item.precio,
                cantidad: 1
            };

        } else {
            mapa[item.nombre].cantidad++;
        }

    });

    const itemsFinal = Object.values(mapa);

    // HORA

    let hora = null;

    if (horaActivada) {

        hora = inputHora.value;

        if (!hora) {
            alert("Selecciona hora");
            return;
        }
    }

    const payload = {
        items: itemsFinal,
        nombre,
        telefono
    };

    if (horaActivada) payload.hora = hora;

    console.log("ENVIANDO:", payload);

    try {

        const res = await fetch("/api/pedidos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.text();
            console.error("ERROR BACKEND:", err);
            alert("Error creando pedido (ver consola)");
            return;
        }

        // RESET

        pedidoActual = [];
        totalPedido = 0;

        horaActivada = false;
        checkHora.classList.remove("activo");
        inputHora.disabled = true;
        inputHora.value = "";

        renderPedido();

        alert("Pedido creado ✔");

    } catch (e) {

        console.error("ERROR FETCH:", e);
        alert("Error conexión");

    }
}

// ======================
// LIMPIAR
// ======================

function limpiarPedido() {

    pedidoActual = [];
    totalPedido = 0;

    renderPedido();
}
