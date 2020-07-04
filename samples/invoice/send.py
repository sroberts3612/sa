from paypalrestsdk import Invoice
import logging
logging.basicConfig(level=logging.INFO)

invoice = Invoice.find("INV2-9DRB-YTHU-2V9Q-7Q24")

if invoice.send():  # return True or False
    print("Invoice[%s] send successfully" % (invoice.id))
else:
    print(invoice.error)
