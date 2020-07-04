from paypalrestsdk import WebProfile
import logging
logging.basicConfig(level=logging.INFO)

history = WebProfile.all()
print(history)

print("List WebProfile:")
for profile in history:
    print("  -> WebProfile[%s]" % (profile.name))
