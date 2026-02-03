async function cargarPedidos() {

    try {

        const res = await fetch("/api/pedidos");
        const pedidos = await res.json();

        const contenedor = document.getElementById("pedidos");
        if (!contenedor) return;

        contenedor.innerHTML = "";

        pedidos.forEach(pedido => {

            // SOLO PENDIENTES
            if (pedido.estado !== "pendiente") return;

            const card = document.createElement("div");
            card.className = "pedido";

            // NUMERO
            const titulo = document.createElement("h2");
            titulo.innerText = `#${pedido.id}`;
            card.appendChild(titulo);

            // HORA SOLO SI EXISTE
            if (pedido.hora) {
                const hora = document.createElement("div");
                hora.className = "hora";
                hora.innerText = `⏰ ${pedido.hora}`;
                card.appendChild(hora);
            }

            // PRODUCTOS
            const lista = document.createElement("ul");

            pedido.items.forEach(item => {

                const li = document.createElement("li");

                if (item.cantidad > 1) {
                    li.innerText = `${item.nombre} x${item.cantidad}`;
                } else {
                    li.innerText = item.nombre;
                }

                lista.appendChild(li);
            });

            card.appendChild(lista);

            // BOTON LISTO
            const boton = document.createElement("button");
            boton.innerText = "✅ MARCAR LISTO";
            boton.onclick = () => marcarListo(pedido.id);

            card.appendChild(boton);

            contenedor.appendChild(card);

        });

    } catch (e) {
        console.error("ERROR ZONA POLLOS:", e);
    }
}

// =======================
// MARCAR LISTO
// =======================

async function marcarListo(id) {

    try {

        const res = await fetch(`/api/pedidos/${id}/listo`, {
            method: "POST"
        });

        if (!res.ok) {
            alert("Error marcando pedido");
            return;
        }

        // REFRESH MANUAL
        cargarPedidos();

    } catch (e) {
        console.error("ERROR LISTO:", e);
    }
}

// =======================
// REFRESH COCINA
// =======================

setInterval(cargarPedidos, 3000);
cargarPedidos();
