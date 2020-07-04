from paypalrestsdk import WebProfile
import logging
logging.basicConfig(level=logging.INFO)

try:
    web_profile = WebProfile.find("XP-3NWU-L5YK-X5EC-6KJM")
    print("Got Details for Web Profile[%s]" % (web_profile.id))

except ResourceNotFound as error:
    print("Web Profile Not Found")
