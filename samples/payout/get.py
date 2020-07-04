from paypalrestsdk import Payout, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    payout = Payout.find("R3LFR867ESVQY")
    print("Got Details for Payout[%s]" % (payout.batch_header.payout_batch_id))

except ResourceNotFound as error:
    print("Web Profile Not Found")
