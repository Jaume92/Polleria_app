from escpos.printer import Usb
from datetime import datetime
from polleria_app.config import (
    PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID, 
    PRINTER_TIMEOUT, PRINTER_IN_EP, PRINTER_OUT_EP
)

def imprimir_pedido(pedido_id, items, hora=None, nombre="", telefono=""):

    try:
        printer = Usb(
            PRINTER_VENDOR_ID, 
            PRINTER_PRODUCT_ID, 
            timeout=PRINTER_TIMEOUT, 
            in_ep=PRINTER_IN_EP, 
            out_ep=PRINTER_OUT_EP
        )


        printer.set(align="center", bold=True, width=2, height=2)
        printer.text("POLLeria\n")
        printer.text("----------------\n")

        printer.set(align="center", bold=True)
        printer.text(f"PEDIDO #{pedido_id}\n")

        printer.set(align="center", bold=False)
        printer.text(datetime.now().strftime("%d/%m/%Y %H:%M") + "\n")

        if hora:
            printer.text(f"RECOGER: {hora}\n")

        printer.text("----------------\n")

        printer.set(align="left")

        for item in items:

            nombre_prod = item["nombre"]
            cantidad = item["cantidad"]

            if cantidad > 1:
                linea = f"{nombre_prod} x{cantidad}\n"
            else:
                linea = f"{nombre_prod}\n"

            printer.text(linea)

        printer.text("----------------\n")

        if nombre:
            printer.text(f"Cliente: {nombre}\n")

        if telefono:
            printer.text(f"Tel: {telefono}\n")

        printer.text("\n")

        printer.set(align="center", bold=True)
        printer.text("GRACIAS\n")

        printer.text("\n\n")

        printer.cut()

        printer.close()

        print("✅ Ticket impreso correctamente")

    except Exception as e:
        print("❌ ERROR IMPRESION:", e)
