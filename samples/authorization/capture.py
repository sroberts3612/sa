from paypalrestsdk import Authorization
import logging
logging.basicConfig(level=logging.INFO)

authorization = Authorization.find("5RA45624N3531924N")
capture = authorization.capture({
    "amount": {
        "currency": "USD",
        "total": "4.54"},
    "is_final_capture": True})

if capture.success():
    print("Capture[%s] successfully" % (capture.id))
else:
    print(capture.error)
