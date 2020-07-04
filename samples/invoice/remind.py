from paypalrestsdk import Invoice
import logging
logging.basicConfig(level=logging.INFO)

invoice = Invoice.find("INV2-9CAH-K5G7-2JPL-G4B4")
options = {
    "subject": "Past due",
    "note": "Please pay soon",
    "send_to_merchant": True
}

if invoice.remind(options):  # return True or False
    print("Invoice[%s] remind successfully" % (invoice.id))
else:
    print(invoice.error)
