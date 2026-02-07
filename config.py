import os
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "polleria.db"

# Impresora (Valores por defecto, se pueden cambiar aquí)
PRINTER_VENDOR_ID = 0x0456
PRINTER_PRODUCT_ID = 0x0808
PRINTER_TIMEOUT = 0
PRINTER_IN_EP = 0x82
PRINTER_OUT_EP = 0x01
