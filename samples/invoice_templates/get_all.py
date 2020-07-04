from paypalrestsdk import InvoiceTemplate
from util import sample_invoice_template
import logging
logging.basicConfig(level=logging.INFO)

for i in range(2):
    invoice_template = sample_invoice_template()
    invoice_template.create()

history = InvoiceTemplate.all()

print("List Invoice Templates:")
for invoice_template in history.templates:
    print("  -> Invoice Template[%s]" % (invoice_template.template_id))
