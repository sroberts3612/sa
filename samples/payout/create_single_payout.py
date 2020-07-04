from paypalrestsdk import Payout, ResourceNotFound
import random
import string

sender_batch_id = ''.join(
    random.choice(string.ascii_uppercase) for i in range(12))

payout = Payout({
    "sender_batch_header": {
        "sender_batch_id": sender_batch_id,
        "email_subject": "You have a payment"
    },
    "items": [
        {
            "recipient_type": "EMAIL",
            "amount": {
                "value": 0.99,
                "currency": "USD"
            },
            "receiver": "shirt-supplier-one@mail.com",
            "note": "Thank you.",
            "sender_item_id": "item_1"
        }
    ]
})

if payout.create(sync_mode=True):
    print("payout[%s] created successfully" %
          (payout.batch_header.payout_batch_id))
else:
    print(payout.error)
