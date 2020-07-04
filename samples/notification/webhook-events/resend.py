from paypalrestsdk import WebhookEvent
import logging
logging.basicConfig(level=logging.INFO)

webhook_event = WebhookEvent.find("8PT597110X687430LKGECATA")

if webhook_event.resend():  # return True or False
    print("webhook event[%s] resend successfully" % (webhook_event.id))
else:
    print(webhook_event.error)
