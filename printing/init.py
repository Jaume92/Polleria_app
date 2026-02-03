from escpos.printer import Usb

p = Usb(0x0456, 0x0808, timeout=0, in_ep=0x82, out_ep=0x01)

p.text("TEST IMPRESORA\n")
p.cut()
p.close()
