"""Verify received webhook payload on merchant server.
Recommended first step before starting to parse the message e.g.
get_webhook_event_resource.py in the samples folder

Helpful link https://developer.paypal.com/docs/integration/direct/rest-webhooks-overview/
"""
from paypalrestsdk.notifications import WebhookEvent
import logging
logging.basicConfig(level=logging.INFO)

# The payload body sent in the webhook event
event_body = '{"id":"WH-0G2756385H040842W-5Y612302CV158622M","create_time":"2015-05-18T15:45:13Z","resource_type":"sale","event_type":"PAYMENT.SALE.COMPLETED","summary":"Payment completed for $ 20.0 USD","resource":{"id":"4EU7004268015634R","create_time":"2015-05-18T15:44:02Z","update_time":"2015-05-18T15:44:21Z","amount":{"total":"20.00","currency":"USD"},"payment_mode":"INSTANT_TRANSFER","state":"completed","protection_eligibility":"ELIGIBLE","protection_eligibility_type":"ITEM_NOT_RECEIVED_ELIGIBLE,UNAUTHORIZED_PAYMENT_ELIGIBLE","parent_payment":"PAY-86C81811X5228590KKVNARQQ","transaction_fee":{"value":"0.88","currency":"USD"},"links":[{"href":"https://api.sandbox.paypal.com/v1/payments/sale/4EU7004268015634R","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v1/payments/sale/4EU7004268015634R/refund","rel":"refund","method":"POST"},{"href":"https://api.sandbox.paypal.com/v1/payments/payment/PAY-86C81811X5228590KKVNARQQ","rel":"parent_payment","method":"GET"}]},"links":[{"href":"https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-0G2756385H040842W-5Y612302CV158622M","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-0G2756385H040842W-5Y612302CV158622M/resend","rel":"resend","method":"POST"}]}'
# Paypal-Transmission-Id in webhook payload header
transmission_id = "dfb3be50-fd74-11e4-8bf3-77339302725b"
# Paypal-Transmission-Time in webhook payload header
timestamp = "2015-05-18T15:45:13Z"
# Webhook id created
webhook_id = "4JH86294D6297924G"
# Paypal-Transmission-Sig in webhook payload header
actual_signature = "thy4/U002quzxFavHPwbfJGcc46E8rc5jzgyeafWm5mICTBdY/8rl7WJpn8JA0GKA+oDTPsSruqusw+XXg5RLAP7ip53Euh9Xu3UbUhQFX7UgwzE2FeYoY6lyRMiiiQLzy9BvHfIzNIVhPad4KnC339dr6y2l+mN8ALgI4GCdIh3/SoJO5wE64Bh/ueWtt8EVuvsvXfda2Le5a2TrOI9vLEzsm9GS79hAR/5oLexNz8UiZr045Mr5ObroH4w4oNfmkTaDk9Rj0G19uvISs5QzgmBpauKr7Nw++JI0pr/v5mFctQkoWJSGfBGzPRXawrvIIVHQ9Wer48GR2g9ZiApWg=="
# Paypal-Cert-Url in webhook payload header
cert_url = 'https://api.sandbox.paypal.com/v1/notifications/certs/CERT-360caa42-fca2a594-a5cafa77'
# PayPal-Auth-Algo in webhook payload header
auth_algo = 'sha256'

response = WebhookEvent.verify(
    transmission_id, timestamp, webhook_id, event_body, cert_url, actual_signature, auth_algo)
print(response)
