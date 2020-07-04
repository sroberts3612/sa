from paypalrestsdk import Webhook
import logging
logging.basicConfig(level=logging.INFO)

webhook = Webhook.find("8TJ12214WP9291246")

if webhook.delete():
    print("Webhook deleted")
else:
    print(webhook.error)
