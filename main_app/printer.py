from zebra import Zebra
import zpl

def print_barcode(vehicleID):
    z = Zebra()
    z.setqueue('ZSB-DP12')
    l = zpl.Label(100, 60)
    height = 8
    l.origin(7,height)
    l.write_barcode(height = 200, barcode_type='C', check_digit='Y', orientation='R')
    l.write_text(str(vehicleID))
    l.endorigin()
    print(l.dumpZPL())
    z.output(l.dumpZPL())
