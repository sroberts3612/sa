from paypalrestsdk import Authorization
import logging
logging.basicConfig(level=logging.INFO)

authorization = Authorization.find("6CR34526N64144512")

if authorization.void():
    print("Void authorization successfully")
else:
    print(authorization.error)
