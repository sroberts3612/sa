from paypalrestsdk import Invoice
import logging

invoice_id = "INV2-EM7V-GTSP-7UTG-Y2MK"

try:
    invoice = Invoice.find(invoice_id)
    height = "400"
    width = "400"

    rv = invoice.get_qr_code(height, width)
    print(rv)

except ResourceNotFound as error:
    print("Invoice Not Found")
