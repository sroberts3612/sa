from paypalrestsdk import PayoutItem, ResourceNotFound

try:
    payout_item = PayoutItem.find("YKV9JPD7C2PCY")
    print("Got Details for PayoutItem[%s]" % (payout_item.payout_item_id))

    if payout_item.cancel():
        print("Payout Item[%s] cancelled successfully" % (payout_item.payout_item_id))
    else:
        print(payout_item.error)

except ResourceNotFound as error:
    print("Payout Item Not Found")
