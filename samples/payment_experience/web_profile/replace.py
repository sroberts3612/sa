from paypalrestsdk import WebProfile, ResourceNotFound
import logging

logging.basicConfig(level=logging.INFO)

try:
    web_profile = WebProfile.find("XP-3NWU-L5YK-X5EC-6KJM")
    print("Got Web Profile Details for Web Profile[%s]" % (web_profile.id))

    web_profile_update_attributes = [
        {
            "op": "replace",
            "path": "/presentation/brand_name",
            "value": "New Brand Name"
        }
    ]

    if web_profile.replace(web_profile_update_attributes):
        web_profile = WebProfile.find("XP-3NWU-L5YK-X5EC-6KJM")
        print("Web Profile [%s] name changed to [%s]" %
              (web_profile.id, web_profile.presentation.brand_name))
    else:
        print(web_profile.error)

except ResourceNotFound as error:
    print("Web Profile Not Found")
