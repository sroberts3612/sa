from paypalrestsdk import InvoiceTemplate
from create import sample_invoice_template
import logging
logging.basicConfig(level=logging.INFO)

invoice_template = sample_invoice_template()
if invoice_template.create():
    found_invoice_template = InvoiceTemplate.find(invoice_template.template_id)
    print("Found Invoice Template[%s]" % found_invoice_template.template_id)
else:
    print(invoice_template.error)
