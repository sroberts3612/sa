from paypalrestsdk import WebhookEventType
import logging
logging.basicConfig(level=logging.INFO)

history = WebhookEventType.all()
print(history)
