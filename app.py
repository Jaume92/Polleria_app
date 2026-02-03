from __future__ import annotations

from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 🧾 IMPRESIÓN
from polleria_app.printing.tickets import imprimir_pedido

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# =========================
# APP
# =========================

app = FastAPI(title="Pollería App", version="1.0")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# CORS (por si mañana metes tablets, móviles, wifi local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELOS
# =========================

class ItemPedido(BaseModel):
    nombre: str
    precio: float
    cantidad: int


class PedidoCreate(BaseModel):
    items: List[ItemPedido]
    nombre: str = ""
    telefono: str = ""
    hora: Optional[str] = None


# =========================
# "BD" EN MEMORIA
# =========================

pedidos: List[dict] = []
_next_id = 1


def _find_pedido(pedido_id: int) -> dict:
    for p in pedidos:
        if p["id"] == pedido_id:
            return p
    raise HTTPException(status_code=404, detail="Pedido no encontrado")


# =========================
# VISTAS
# =========================

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/mostrador")


@app.get("/mostrador", response_class=HTMLResponse, include_in_schema=False)
def vista_mostrador(request: Request):
    return templates.TemplateResponse("mostrador.html", {"request": request})


@app.get("/pollos", response_class=HTMLResponse, include_in_schema=False)
def vista_pollos(request: Request):
    return templates.TemplateResponse("zona_pollos.html", {"request": request})


@app.get("/tele_cliente", response_class=HTMLResponse, include_in_schema=False)
def vista_tele_cliente(request: Request):
    return templates.TemplateResponse("tele_cliente.html", {"request": request})


# =========================
# API PRODUCTOS
# =========================

@app.get("/api/productos")
def listar_productos():
    return [
        {"id": 1, "nombre": "Pollo entero", "precio": 12.00},
        {"id": 2, "nombre": "Medio pollo", "precio": 6.50},
        {"id": 3, "nombre": "Patatas grandes", "precio": 3.50},
        {"id": 4, "nombre": "Croquetas de toro", "precio": 4.00},
        {"id": 5, "nombre": "Sticks de queso", "precio": 3.80},
        {"id": 6, "nombre": "Coca-Cola", "precio": 2.00},
        {"id": 7, "nombre": "Barra de pan", "precio": 1.00},
    ]


# =========================
# API PEDIDOS
# =========================

@app.get("/api/pedidos")
def listar_pedidos():
    return pedidos


@app.post("/api/pedidos")
def crear_pedido(payload: PedidoCreate, background_tasks: BackgroundTasks):
    global _next_id

    nuevo = {
        "id": _next_id,
        "items": [item.dict() for item in payload.items],
        "estado": "pendiente",
        "nombre": payload.nombre,
        "telefono": payload.telefono,
        "hora": payload.hora,
        "canal": "MOSTRADOR",
        "fecha": datetime.now().isoformat(timespec="minutes")
    }

    pedidos.append(nuevo)
    _next_id += 1

    # 🧾 IMPRESIÓN (NO BLOQUEA API)
    try:
        background_tasks.add_task(
            imprimir_pedido,
            nuevo["id"],
            nuevo["items"],
            nuevo["hora"],
            nuevo["nombre"],
            nuevo["telefono"]
        )
    except Exception as e:
        print("❌ Error lanzando impresión:", e)

    return nuevo


@app.get("/api/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: int):
    return _find_pedido(pedido_id)


@app.post("/api/pedidos/{pedido_id}/listo")
def marcar_listo(pedido_id: int):
    p = _find_pedido(pedido_id)
    p["estado"] = "listo"
    return {"ok": True}


@app.post("/api/pedidos/{pedido_id}/entregado")
def marcar_entregado(pedido_id: int):
    p = _find_pedido(pedido_id)
    p["estado"] = "entregado"
    return {"ok": True}


# =========================
# RESET DEMO
# =========================

@app.post("/api/reset")
def reset_demo():
    global pedidos, _next_id
    pedidos = []
    _next_id = 1
    return {"ok": True}
