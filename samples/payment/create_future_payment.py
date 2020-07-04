# Create Future Payment Using PayPal Wallet
# https://developer.paypal.com/docs/integration/mobile/make-future-payment/
import paypalrestsdk

api = paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "CLIENT_ID",
    "client_secret": "CLIENT_SECRET"
})

# authorization code from mobile sdk
authorization_code = ''

# Exchange authorization_code for long living refresh token. You should store
# it in a database for later use
refresh_token = api.get_refresh_token(authorization_code)

# correlation id from mobile sdk
correlation_id = ''

# Initialize the payment object
payment = paypalrestsdk.Payment({
    "intent": "authorize",
    "payer": {
        "payment_method": "paypal"},
    "transactions": [{
        "amount": {
            "total": "0.17",
            "currency": "USD"},
        "description": "This is the payment transaction description."}]})

# Create the payment. Set intent to sale to charge immediately,
# else if authorize use the authorization id to capture
# payment later using samples/authorization/capture.py
if payment.create(refresh_token, correlation_id):
    print("Payment %s created successfully" % (payment.id))
    if payment['intent'] == "authorize":
        print(
            "Payment %s authorized. Authorization id is %s"
            % (payment.id, payment['transactions'][0]['related_resources'][0]['authorization']['id'])
        )
else:
    print("Error while creating payment:")
    print(payment.error)
