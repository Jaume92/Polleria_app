const TIEMPO_VISIBLE = 90000; // 1.5 minutos

let mostrados = new Map();

async function cargarPedidos() {

    try {

        const res = await fetch("/api/pedidos");
        const pedidos = await res.json();

        const contenedor = document.getElementById("pedidos");
        if (!contenedor) return;

        pedidos.forEach(pedido => {

            // SOLO LISTOS
            if (pedido.estado !== "listo") return;

            if (mostrados.has(pedido.id)) return;

            const card = document.createElement("div");
            card.className = "pedido animar";

            // NUMERO
            const titulo = document.createElement("h2");
            titulo.innerText = `#${pedido.id}`;
            card.appendChild(titulo);

            // HORA
            if (pedido.hora) {
                const hora = document.createElement("div");
                hora.className = "hora";
                hora.innerText = pedido.hora;
                card.appendChild(hora);
            }

            contenedor.appendChild(card);

            mostrados.set(pedido.id, true);

            // AUTOBORRADO
            setTimeout(() => {

                card.classList.add("fadeout");

                setTimeout(() => {
                    card.remove();
                    mostrados.delete(pedido.id);
                }, 800);

            }, TIEMPO_VISIBLE);

        });

    } catch (e) {
        console.error("ERROR TELE CLIENTE:", e);
    }
}

// LOOP
setInterval(cargarPedidos, 2000);
cargarPedidos();
