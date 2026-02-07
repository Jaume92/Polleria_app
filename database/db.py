import sqlite3
import os
from typing import List, Optional, Dict, Any
from polleria_app.config import DATABASE_PATH, DATABASE_DIR

def get_db_connection():
    """Crea una conexión a la base de datos."""
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row # Para acceder a columnas por nombre
    return conn

def init_db():
    """Inicializa la base de datos con el esquema."""
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        
    conn = get_db_connection()
    conn.executescript(schema_sql)
    conn.close()
    print(f"✅ Base de datos inicializada en: {DATABASE_PATH}")

# --- PRODUCTOS ---

def get_productos() -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE activo = 1")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_producto_by_id(prod_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (prod_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# --- PEDIDOS ---

def create_pedido(nombre: str, telefono: str, hora: str, items: List[tuple]) -> dict:
    """
    Crea un pedido y sus items en una transacción.
    items: Lista de tuplas (producto_id, cantidad, precio_unitario, nombre_producto)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Crear Pedido
        cursor.execute("""
            INSERT INTO pedidos (nombre_cliente, telefono, hora_recogida)
            VALUES (?, ?, ?)
        """, (nombre, telefono, hora))
        pedido_id = cursor.lastrowid
        
        # 2. Insertar Items
        for prod_id, cantidad, precio, nombre_prod in items:
            cursor.execute("""
                INSERT INTO items_pedido (pedido_id, producto_id, nombre_snapshot, precio_snapshot, cantidad)
                VALUES (?, ?, ?, ?, ?)
            """, (pedido_id, prod_id, nombre_prod, precio, cantidad))
            
        conn.commit()
        
        # 3. Devolver el pedido completo recien creado
        return get_pedido_completo(pedido_id)
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_pedidos() -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    # Obtenemos los pedidos
    cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
    rows = cursor.fetchall()
    pedidos = [dict(row) for row in rows]
    
    # Para cada pedido, obtenemos sus items (podría optimizarse con JOIN, pero así es simple)
    for p in pedidos:
        cursor.execute("""
            SELECT nombre_snapshot as nombre, precio_snapshot as precio, cantidad 
            FROM items_pedido WHERE pedido_id = ?
        """, (p["id"],))
        p["items"] = [dict(item) for item in cursor.fetchall()]
        
    conn.close()
    return pedidos

def get_pedido_completo(pedido_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
        
    pedido = dict(row)
    
    cursor.execute("""
        SELECT nombre_snapshot as nombre, precio_snapshot as precio, cantidad 
        FROM items_pedido WHERE pedido_id = ?
    """, (pedido_id,))
    pedido["items"] = [dict(item) for item in cursor.fetchall()]
    
    conn.close()
    return pedido

def update_pedido_estado(pedido_id: int, nuevo_estado: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET estado = ? WHERE id = ?", (nuevo_estado, pedido_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
