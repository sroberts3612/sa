from paypalrestsdk import Webhook
import logging

logging.basicConfig(level=logging.INFO)

webhook = Webhook({
    "url": "https://www.yeowza.com/paypal_webhook",
    "event_types": [
        {
            "name": "PAYMENT.AUTHORIZATION.CREATED"
        },
        {
            "name": "PAYMENT.AUTHORIZATION.VOIDED"
        }
    ]
})

if webhook.create():
    print("Webhook[%s] created successfully" % (webhook.id))
else:
    print(webhook.error)
