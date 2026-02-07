// TPV 70/30 - LOGICA SIMPLIFICADA
let productosDB = [];
let pedidoActual = [];

// DOM Elements
let productosDiv, ticketDiv, totalSpan;
let inputCliente, inputTelefono, btnCobrar, divReloj;

document.addEventListener("DOMContentLoaded", () => {
    // Referencias DOM
    productosDiv = document.getElementById("productos-grid");
    ticketDiv = document.getElementById("ticket-list");
    totalSpan = document.getElementById("total");
    inputCliente = document.getElementById("cliente");
    inputTelefono = document.getElementById("telefono");
    btnCobrar = document.getElementById("btn-cobrar");
    divReloj = document.getElementById("reloj");

    // Listeners
    btnCobrar.addEventListener("click", cobrarPedido);

    // Iniciar
    iniciarReloj();
    cargarDatos();
});

// =========================================
// RELOJ
// =========================================
function iniciarReloj() {
    setInterval(() => {
        const now = new Date();
        divReloj.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }, 1000);
}

// =========================================
// DATOS & RENDER
// =========================================
async function cargarDatos() {
    try {
        const res = await fetch("/api/productos");
        if (res.ok) {
            productosDB = await res.json();
            renderProductos();
        } else {
            productosDiv.innerHTML = "Error cargando productos";
        }
    } catch (e) {
        console.error(e);
        productosDiv.innerHTML = "Error de conexión";
    }
}

function renderProductos() {
    productosDiv.innerHTML = "";
    // Renderizar TODOS los productos (sin categorias)
    productosDB.forEach(prod => {
        const btn = document.createElement("button");
        btn.className = "producto-btn";
        btn.innerHTML = `
            <div>${prod.nombre}</div>
            <small>${Number(prod.precio).toFixed(2)}€</small>
        `;
        btn.onclick = () => agregarAlTicket(prod);
        productosDiv.appendChild(btn);
    });
}

// =========================================
// TICKET
// =========================================
function agregarAlTicket(prod) {
    const existe = pedidoActual.find(p => p.id === prod.id);
    if (existe) {
        existe.cantidad++;
    } else {
        pedidoActual.push({ ...prod, cantidad: 1, precio: Number(prod.precio) });
    }
    renderTicket();
}

function renderTicket() {
    ticketDiv.innerHTML = "";
    let total = 0;

    pedidoActual.forEach(item => {
        const subtotal = item.cantidad * item.precio;
        total += subtotal;

        const row = document.createElement("div");
        row.className = "ticket-item";
        row.innerHTML = `
            <div>${item.nombre} <small>x${item.cantidad}</small></div>
            <div style="display:flex; gap:10px; align-items:center">
                <span>${subtotal.toFixed(2)}</span>
                <span style="color:red; cursor:pointer" onclick="borrarItem(${item.id})">✖</span>
            </div>
        `;
        ticketDiv.appendChild(row);
    });

    totalSpan.innerText = total.toFixed(2) + " €";
    ticketDiv.scrollTop = ticketDiv.scrollHeight;
}

window.borrarItem = function (id) {
    pedidoActual = pedidoActual.filter(p => p.id !== id);
    renderTicket();
}

// =========================================
// COBRAR
// =========================================
async function cobrarPedido() {
    if (pedidoActual.length === 0) return alert("Ticket vacío");

    const payload = {
        items: pedidoActual.map(p => ({ id: p.id, cantidad: p.cantidad })),
        nombre: inputCliente.value || "Cliente TPV",
        telefono: inputTelefono.value || ""
    };

    try {
        const res = await fetch("/api/pedidos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            alert("✓ Cobrado correctamente");
            pedidoActual = [];
            inputCliente.value = "";
            inputTelefono.value = "";
            renderTicket();
        } else {
            alert("Error al guardar pedido");
        }
    } catch (e) {
        alert("Error de conexión");
        console.error(e); // Added error logging
    }
}
