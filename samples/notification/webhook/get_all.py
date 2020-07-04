from paypalrestsdk import Webhook
import logging
logging.basicConfig(level=logging.INFO)

history = Webhook.all()
print(history)

print("List Webhook:")
for webhook in history:
    print("  -> Webhook[%s]" % (webhook.name))
