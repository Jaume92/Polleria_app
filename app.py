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
app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}
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

app = FastAPI(title="Pollería App", version="2.0")

# Asegurar que la BD existe al arrancar
@app.on_event("startup")
def on_startup():
    db.init_db()

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# CORS
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
    id: int # ID del producto
    cantidad: int

class PedidoCreate(BaseModel):
    items: List[ItemPedido]
    nombre: str = ""
    telefono: str = ""
    hora: Optional[str] = None


# =========================
# VISTAS (FRONTEND)
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

from polleria_app.database import db

@app.get("/api/productos")
def listar_productos():
    return db.get_productos()


# =========================
# API PEDIDOS
# =========================

@app.get("/api/pedidos")
def listar_pedidos():
    return db.get_pedidos()

@app.post("/api/pedidos")
def crear_pedido(payload: PedidoCreate, background_tasks: BackgroundTasks):
    
    # 1. Validar y preparar items con precio real de BD (SEGURIDAD)
    items_para_guardar = []
    
    for item in payload.items:
        prod = db.get_producto_by_id(item.id)
        if not prod:
            raise HTTPException(status_code=400, detail=f"Producto ID {item.id} no existe")
            
        items_para_guardar.append((
            prod["id"],           # ID Producto
            item.cantidad,        # Cantidad
            prod["precio"],       # Precio Real (Snapshot)
            prod["nombre"]        # Nombre Real (Snapshot)
        ))
    
    if not items_para_guardar:
        raise HTTPException(status_code=400, detail="El pedido no tiene items validos")

    # 2. Guardar en BD (Transaccional)
    try:
        nuevo_pedido = db.create_pedido(
            nombre=payload.nombre,
            telefono=payload.telefono,
            hora=payload.hora,
            items=items_para_guardar
        )
    except Exception as e:
        print("❌ Error guardando pedido:", e)
        raise HTTPException(status_code=500, detail="Error interno guardando pedido")

    # 3. IMPRESIÓN (Background)
    try:
        # Convertimos al formato que espera imprimir_pedido (lista de dicts)
        items_impresion = [
            {"nombre": i[3], "cantidad": i[1]} for i in items_para_guardar
        ]
        
        background_tasks.add_task(
            imprimir_pedido,
            pedido_id=nuevo_pedido["id"],
            items=items_impresion,
            hora=nuevo_pedido["hora_recogida"], # Ojo: en BD es hora_recogida
            nombre=nuevo_pedido["nombre_cliente"], # Ojo: en BD es nombre_cliente
            telefono=nuevo_pedido["telefono"]
        )
    except Exception as e:
        print("❌ Error lanzando impresión:", e)

    return nuevo_pedido


@app.get("/api/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: int):
    p = db.get_pedido_completo(pedido_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return p


@app.post("/api/pedidos/{pedido_id}/listo")
def marcar_listo(pedido_id: int):
    if not db.get_pedido_completo(pedido_id):
         raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.update_pedido_estado(pedido_id, "listo")
    return {"ok": True}


@app.post("/api/pedidos/{pedido_id}/entregado")
def marcar_entregado(pedido_id: int):
    if not db.get_pedido_completo(pedido_id):
         raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.update_pedido_estado(pedido_id, "entregado")
    return {"ok": True}


# =========================
# RESET (SOLO LIMPIA, YA NO REINICIA MEMORIA)
# =========================

@app.post("/api/reset")
def reset_demo():
    # TODO: Implementar borrado de tabla pedidos si se desea
    # Por seguridad, ahora no borramos nada
    return {"ok": True, "message": "Reset desactivado por seguridad"}

