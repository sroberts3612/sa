from paypalrestsdk import Authorization, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    authorization = Authorization.find("99M58264FG144833V")
    print(
        "Got Authorization details for Authorization[%s]" % (authorization.id))

except ResourceNotFound as error:
    print("Authorization Not Found")
