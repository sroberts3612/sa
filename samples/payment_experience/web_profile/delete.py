from paypalrestsdk import WebProfile
import logging
logging.basicConfig(level=logging.INFO)

web_profile = WebProfile.find("XP-9R62-L4QJ-M8H6-UNV5")

if web_profile.delete():
    print("WebProfile deleted")
else:
    print(web_profile.error)
