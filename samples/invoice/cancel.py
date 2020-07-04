from paypalrestsdk import Invoice
import logging
import json
logging.basicConfig(level=logging.INFO)

invoice = Invoice.find("INV2-V2QW-LCUV-RNRL-AQUE")
options = {
    "subject": "Past due",
    "note": "Canceling invoice",
    "send_to_merchant": True,
    "send_to_payer": True
}

if invoice.cancel(options):  # return True or False
    print(json.dumps(invoice.to_dict(), sort_keys=False, indent=4))
else:
    print(invoice.error)
