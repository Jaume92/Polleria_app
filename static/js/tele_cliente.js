const TIEMPO_VISIBLE = 60000; // 1 minuto exacto (CAMBIO SOLICITADO)

let mostrados = new Map();

async function cargarPedidos() {

    try {
        // Cache Buster para evitar que el navegador guarde datos viejos
        const res = await fetch("/api/pedidos?t=" + Date.now());
        const pedidos = await res.json();

        const contenedor = document.getElementById("pedidos");
        if (!contenedor) return;

        pedidos.forEach(pedido => {

            // SOLO LISTOS
            if (pedido.estado !== "listo") return;

            // Si ya está mostrado, ignorar
            if (mostrados.has(pedido.id)) return;

            const card = document.createElement("div");
            card.className = "pedido animar";
            card.id = `pedido-${pedido.id}`;

            // NUMERO ESTILIZADO (HASHTAG PEQUEÑO)
            const titulo = document.createElement("h2");
            titulo.innerHTML = `<span class="hashtag">#</span>${pedido.id}`;
            card.appendChild(titulo);

            // HORA
            if (pedido.hora && String(pedido.hora).trim() !== "") {
                const hora = document.createElement("div");
                hora.className = "hora";
                hora.innerText = pedido.hora;
                card.appendChild(hora);
            }

            contenedor.appendChild(card);

            // INTELIGENCIA: Guardamos TIMESTAMP para saber cuándo borrarlo
            // Usamos un timeout simple porque es lo que pidió: "irse al minuto"
            mostrados.set(pedido.id, true);

            setTimeout(() => {
                if (document.body.contains(card)) {
                    card.classList.add("fadeout");
                    setTimeout(() => {
                        card.remove();
                        // Nota: NO borramos de 'mostrados' para que no vuelva a salir 
                        // si sigue listo en BD. Se queda en 'mostrados' para siempre 
                        // hasta recarga de página.
                    }, 800);
                }
            }, TIEMPO_VISIBLE);
        });

    } catch (e) {
        console.error("ERROR TELE CLIENTE:", e);
    }
}

// LOOP
setInterval(cargarPedidos, 2000);
cargarPedidos();
