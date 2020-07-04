from paypalrestsdk import Invoice, ResourceNotFound
import logging
import json
logging.basicConfig(level=logging.INFO)

try:
    invoice = Invoice.find("INV2-9DRB-YTHU-2V9Q-7Q24")
    print(json.dumps(invoice.to_dict(), sort_keys=False, indent=4))

except ResourceNotFound as error:
    print("Invoice Not Found")
