from paypalrestsdk import Invoice, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    number = Invoice.next_invoice_number();
    print("Got next invoice number[%s]" % (number))

except ResourceNotFound as error:
    print("Something went wrong")
