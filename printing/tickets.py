from escpos.printer import Usb
from datetime import datetime

# TU IMPRESORA
VENDOR_ID = 0x0456
PRODUCT_ID = 0x0808


def imprimir_pedido(pedido_id, items, hora=None, nombre="", telefono=""):

    try:
        printer = Usb(VENDOR_ID, PRODUCT_ID, timeout=0, in_ep=0x82, out_ep=0x01)


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
