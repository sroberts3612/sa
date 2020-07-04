from paypalrestsdk import Invoice
import logging
import json
logging.basicConfig(level=logging.INFO)



# status should pass array with below enum values
# Allowed values: DRAFT, SENT, PAID, MARKED_AS_PAID, CANCELLED, REFUNDED, PARTIALLY_REFUNDED, MARKED_AS_REFUNDED.

options = {
    "start_invoice_date": "2016-01-01 PST",
    "end_invoice_date": "2030-03-26 PST",
    "status": ["SENT", "DRAFT", "PAID", "CANCELLED"]
}
invoices = Invoice.search(options)

if invoices.success():  # return True or False
    print(json.dumps(invoices.to_dict(), sort_keys=False, indent=4))
else:
    print(invoices.error)