from paypalrestsdk import WebProfile
import logging
logging.basicConfig(level=logging.INFO)

web_profile_update_attributes = {
    "name": "YeowZa! T-Shirt Shop",
    "presentation": {
        "logo_image": "http://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Nature_photographer.jpg/1599px-Nature_photographer.jpg"
    },
    "input_fields": {
        "no_shipping": 1,
        "address_override": 1
    },
    "flow_config": {
        "landing_page_type": "billing",
        "bank_txn_pending_url": "http://www.yeowza.com"
    }
}

web_profile = WebProfile.find("XP-9R62-L4QJ-M8H6-UNV5")

if web_profile.update(web_profile_update_attributes):
    print("Web Profile[%s] updated successfully" % (web_profile.id))
else:
    print(web_profile.error)
