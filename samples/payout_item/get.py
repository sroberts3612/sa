from paypalrestsdk import PayoutItem, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    payout_item = PayoutItem.find("YKV9JPD7C2PCY")
    print("Got Details for PayoutItem[%s]" % (payout_item.payout_item_id))

except ResourceNotFound as error:
    print("Payout Item Not Found")
