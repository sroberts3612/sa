from paypalrestsdk import Invoice
import logging
logging.basicConfig(level=logging.INFO)

invoice = Invoice.find("<INVOICE_ID>")
refund_attr = {
    "date": "2014-07-06 03:30:00 PST",
    "note": "Refund provided by cash."
}

if invoice.record_refund(refund_attr):  # return True or False
    print("Payment record on Invoice[%s] successfully" % (invoice.id))
else:
    print(invoice.error)
