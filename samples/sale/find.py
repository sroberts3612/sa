# Get Details of a Sale Transaction Sample
# This sample code demonstrates how you can retrieve
# details of completed Sale Transaction.
# API used: /v1/payments/sale/{sale-id}
from paypalrestsdk import Sale, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    # Get Sale object by passing sale id
    sale = Sale.find("7DY409201T7922549")
    print("Got Sale details for Sale[%s]" % (sale.id))

except ResourceNotFound as error:
    print("Sale Not Found")
