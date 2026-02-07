import sys
import os

print("CWD:", os.getcwd())
print("PYTHONPATH:", sys.path)

try:
    print("Intentando: from polleria_app.database import db")
    from polleria_app.database import db
    print("✅ Éxito absoluto")
except ImportError as e:
    print(f"❌ Fallo absoluto: {e}")

try:
    print("Intentando: from database import db")
    from database import db
    print("✅ Éxito relativo/local")
    
    try:
        prods = db.get_productos()
        print(f"✅ DB Leída. Productos: {len(prods)}")
    except Exception as e:
        print(f"❌ Fallo DB: {e}")

except ImportError as e:
    print(f"❌ Fallo relativo: {e}")
