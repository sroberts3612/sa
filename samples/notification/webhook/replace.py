from paypalrestsdk import Webhook, ResourceNotFound
import logging

logging.basicConfig(level=logging.INFO)

try:
    webhook = Webhook.find("70Y03947RF112050J")
    print("Got Webhook Details for Webhook[%s]" % (webhook.id))

    webhook_replace_attributes = [
        {
            "op": "replace",
            "path": "/url",
            "value": "https://www.yeowza.com/paypal_webhook_url"
        },
        {
            "op": "replace",
            "path": "/event_types",
            "value": [
                {
                    "name": "PAYMENT.SALE.REFUNDED"
                }
            ]
        }
    ]

    if webhook.replace(webhook_replace_attributes):
        webhook = Webhook.find("70Y03947RF112050J")
        print("Webhook [%s] url changed to [%s]" % (webhook.id, webhook.url))
    else:
        print(webhook.error)

except ResourceNotFound as error:
    print("Webhook Not Found")
