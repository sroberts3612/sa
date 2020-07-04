from paypalrestsdk import Invoice
import logging
from paypalrestsdk.openid_connect import Tokeninfo

logging.basicConfig(level=logging.INFO)

# Using Log In with PayPal, third party merchants can authorize your application to create and submit invoices on their behalf.
# See https://developer.paypal.com/docs/integration/direct/identity/log-in-with-paypal/ for more details about Log In with PayPal.


# Step 1. Generate a Log In with PayPal authorization URL. The third party merchant will need to visit this URL and authorize your request. You should use the `openid`, `https://uri.paypal.com/services/invoicing`, and `email` scopes at the minimum.
# paypalrestsdk.configure({'openid_client_id': 'CLIENT_ID', 'openid_client_secret': 'CLIENT_SECRET', 'openid_redirect_uri': 'http://example.com'})
# login_url = Tokeninfo.authorize_url({'scope': 'openid profile'})

# For example, the URL to redirect the third party merchant may be like:
# https://www.sandbox.paypal.com/webapps/auth/protocol/openidconnect/v1/authorize?client_id=AYSq3RDGsmBLJE-otTkBtM-jBRd1TCQwFf9RGfwddNXWz0uFU9ztymylOhRS&scope=openid%20https%3A%2F%2Furi.paypal.com%2Fservices%2Finvoicing%20email&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%2Fpaypal%2FPayPal-PHP-SDK%2Fsample%2Flipp%2FUserConsentRedirect.php%3Fsuccess%3Dtrue

# Step 2. After the third party merchant authorizes your request, Log In with PayPal will redirect the browser to your configured openid_redirect_uri with an authorization code query parameter value.

# For example, after the merchant successfully authorizes your request, they will be redirected to the merchant's website configured via `openid_redirect_uri` like:
# http://localhost/paypal/PayPal-Python-SDK/sample/UserConsentRedirect.php?success=true&scope=https%3A%2F%2Furi.paypal.com%2Fservices%2Finvoicing+openid+email&code=q6DV3YTMUDquwMQ88I7VyE_Ou1ksKcKVo1b_a8zqUQ7fGCxLoLajHIBROQ5yxcM0dNWVWPQaovH35dJmdmunNYrNKao8UlpY5LVMuTgnxZ6ce6UL3XuEd3JXuuPtdg-4feXyMA25oh2aM5o5HTtSeSG1Ag596q9tk90dfJQ8gxhFTw1bV

# Step 3. Your web app should parse the query parameters for the authorization `code` value. You should use the `code` value to get a refresh token and securely save it for later use.
#begin
#  authorization_code = "q6DV3YTMUDquwMQ88I7VyE_Ou1ksKcKVo1b_a8zqUQ7fGCxLoLajHIBROQ5yxcM0dNWVWPQaovH35dJmdmunNYrNKao8UlpY5LVMuTgnxZ6ce6UL3XuEd3JXuuPtdg-4feXyMA25oh2aM5o5HTtSeSG1Ag596q9tk90dfJQ8gxhFTw1bV"
#  tokeninfo = Tokeninfo.create(code)
#  print(tokeninfo)
#  # Response 200
#  tokeninfo = {
#    token_type: 'Bearer',
#    expires_in: '28800',
#    refresh_token: 'J5yFACP3Y5dqdWCdN3o9lNYz0XyR01IHNMQn-E4r6Ss38rqbQ1C4rC6PSBhJvB_tte4WZsWe8ealMl-U_GMSz30dIkKaovgN41Xf8Sz0EGU55da6tST5I6sg3Rw',
#    id_token: '<some value>',
#    access_token: '<some value>'
#  }
#end

# Step 4. You can use the refresh token to get the third party merchant's email address to use in the invoice, and then you can create an invoice on behalf of the third party merchant.
refresh_token = "J5yFACP3Y5dqdWCdN3o9lNYz0XyR01IHNMQn-E4r6Ss38rqbQ1C4rC6PSBhJvB_tte4WZsWe8ealMl-U_GMSz30dIkKaovgN41Xf8Sz0EGU55da6tST5I6sg3Rw"

token_info = Tokeninfo.create_with_refresh_token(refresh_token)

print(token_info)

user_info = token_info.userinfo()

print(user_info)

invoice = Invoice({
    "merchant_info": {
        # The email address used here would be of a third party.
        "email": user_info.email,
        "first_name": "Dennis",
        "last_name": "Doctor",
        "business_name": "Medical Professionals, LLC",
        "phone": {
            "country_code": "001",
            "national_number": "5032141716"
        },
        "address": {
            "line1": "1234 Main St.",
            "city": "Portland",
            "state": "OR",
            "postal_code": "97217",
            "country_code": "US"
        }
    },
    "billing_info": [{"email": "example@example.com"}],
    "items": [
        {
            "name": "Sutures",
            "quantity": 50,
            "unit_price": {
                "currency": "USD",
                "value": 5
            }
        }
    ],
    "note": "Medical Invoice 16 Jul, 2013 PST",
    "payment_term": {
        "term_type": "NET_45"
    },
    "shipping_info": {
        "first_name": "Sally",
        "last_name": "Patient",
        "business_name": "Not applicable",
        "phone": {
            "country_code": "001",
            "national_number": "5039871234"
        },
        "address": {
            "line1": "1234 Broad St.",
            "city": "Portland",
            "state": "OR",
            "postal_code": "97216",
            "country_code": "US"
        }
    }
})

if invoice.create(refresh_token):
    print("Third Party Invoice[%s] created successfully" % (invoice.id))

    # Fetch the resource similarly as shown below:
    result = Invoice.find(invoice.id, refresh_token=refresh_token)
    print("Invoice Detail: %s" % result)
else:
    print(invoice.error)
