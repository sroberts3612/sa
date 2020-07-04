from paypalrestsdk import Webhook
import logging
logging.basicConfig(level=logging.INFO)

try:
    webhook = Webhook.find("70Y03947RF112050J")
    webhook_event_types = webhook.get_event_types()
    print(webhook_event_types)

except ResourceNotFound as error:
    print("Webhook Not Found")
