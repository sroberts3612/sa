"""
An example to demonstrate getting the paypal resource sent via
the webhook event to the merchant server. It is recommended that
the payload is verified before this. Refer to verify_webhook_events.py
in the samples for more information regarding this.
"""
from paypalrestsdk import WebhookEvent
import logging
logging.basicConfig(level=logging.INFO)

webhook_event_json = {
    "id": "WH-8JH82006PH834764Y-9XE6617312678932V",
    "create_time": "2014-11-03T01:07:13Z",
    "resource_type": "authorization",
    "event_type": "PAYMENT.AUTHORIZATION.CREATED",
    "summary": "A successful payment authorization was created for $ 5.0 USD",
    "resource": {
        "id": "3WG12057BW522780J",
        "create_time": "2014-11-03T01:05:27Z",
        "update_time": "2014-11-03T01:07:08Z",
        "amount": {
            "total": "5.00",
            "currency": "USD",
            "details": {
                "subtotal": "5.00"
            }
        },
        "payment_mode": "INSTANT_TRANSFER",
        "state": "authorized",
        "protection_eligibility": "ELIGIBLE",
        "protection_eligibility_type": "ITEM_NOT_RECEIVED_ELIGIBLE,UNAUTHORIZED_PAYMENT_ELIGIBLE",
        "parent_payment": "PAY-3KA96482AM105222NKRLNJVY",
        "valid_until": "2014-12-02T01:05:27Z",
        "links": [
            {
                "href": "https://api.sandbox.paypal.com/v1/payments/authorization/3WG12057BW522780J",
                "rel": "self",
                "method": "GET"
            },
            {
                "href": "https://api.sandbox.paypal.com/v1/payments/authorization/3WG12057BW522780J/capture",
                "rel": "capture",
                "method": "POST"
            },
            {
                "href": "https://api.sandbox.paypal.com/v1/payments/authorization/3WG12057BW522780J/void",
                "rel": "void",
                "method": "POST"
            },
            {
                "href": "https://api.sandbox.paypal.com/v1/payments/authorization/3WG12057BW522780J/reauthorize",
                "rel": "reauthorize",
                "method": "POST"
            },
            {
                "href": "https://api.sandbox.paypal.com/v1/payments/payment/PAY-3KA96482AM105222NKRLNJVY",
                "rel": "parent_payment",
                "method": "GET"
            }
        ]
    },
    "links": [
        {
            "href": "https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-8JH82006PH834764Y-9XE6617312678932V",
            "rel": "self",
            "method": "GET"
        },
        {
            "href": "https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-8JH82006PH834764Y-9XE6617312678932V/resend",
            "rel": "resend",
            "method": "POST"
        }
    ]
}

webhook_event = WebhookEvent(webhook_event_json)
# event_resource is wrapped the corresponding paypalrestsdk class
# this is dynamically resolved by the sdk
event_resource = webhook_event.get_resource()
