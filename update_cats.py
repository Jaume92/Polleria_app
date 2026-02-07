from polleria_app.database import db

def update_categories():
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    updates = [
        ("POLLOS", [1, 2]),           # Pollo entero, Medio pollo
        ("COMPLEMENTOS", [3, 4, 5, 7]), # Patatas, Croquetas, Sticks, Pan
        ("BEBIDAS", [6])              # Coca-Cola
    ]
    
    for cat, ids in updates:
        # Generate placeholders for the list of IDs
        placeholders = ','.join('?' * len(ids))
        query = f"UPDATE productos SET categoria = ? WHERE id IN ({placeholders})"
        # Combine category with ids for the parameters
        params = [cat] + ids
        cursor.execute(query, params)
        print(f"✅ Actualizados {len(ids)} productos a categoria '{cat}'")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_categories()
