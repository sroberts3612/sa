from paypalrestsdk import InvoiceTemplate
from util import sample_invoice_template
import random
import string
import logging
logging.basicConfig(level=logging.INFO)

invoice_template = sample_invoice_template()

if invoice_template.create():
    invoice_template.template_data.items[0].quantity = 2
    if invoice_template.update():
        print("Invoice Template[%s] updated sucessfully" % invoice_template.template_id)
    else:
        print("Failed to update Invoice Template" + str(invoice_template.error))
else:
    print("Failed to create Invoice Template")

