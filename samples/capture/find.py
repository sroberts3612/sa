from paypalrestsdk import Capture, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    capture = Capture.find("8F148933LY9388354")
    print("Got Capture details for Capture[%s]" % (capture.id))

except ResourceNotFound as error:
    print("Capture Not Found")
