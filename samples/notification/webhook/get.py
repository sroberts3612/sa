from paypalrestsdk import Webhook
import logging
logging.basicConfig(level=logging.INFO)

try:
    webhook = Webhook.find("8TJ12214WP9291246")
    print("Got Details for Webhook[%s]" % (webhook.id))

except ResourceNotFound as error:
    print("Webhook Not Found")
