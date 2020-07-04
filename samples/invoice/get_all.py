from paypalrestsdk import Invoice
import logging
logging.basicConfig(level=logging.INFO)

history = Invoice.all({"page_size": 2})

print("List Invoice:")
for invoice in history.invoices:
    print("  -> Invoice[%s]" % (invoice.id))
