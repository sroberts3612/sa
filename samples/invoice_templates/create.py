from paypalrestsdk import InvoiceTemplate
from util import sample_invoice_template
import logging
logging.basicConfig(level=logging.INFO)

invoice_template = sample_invoice_template()
if invoice_template.create():
    print("Invoice Template[%s] created successfully" % (invoice_template.template_id))
else:
    print(invoice_template.error)

