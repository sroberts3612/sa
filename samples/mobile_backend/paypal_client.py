import paypalrestsdk
import paypal_config
import logging

logging.basicConfig(level=logging.DEBUG)

api = paypalrestsdk.configure({
    "mode": paypal_config.MODE,
    "client_id": paypal_config.CLIENT_ID,
    "client_secret": paypal_config.CLIENT_SECRET
})

# map from user email to refresh_token
CUSTOMER_TOKEN_MAP = "customer_token_map.txt"

# store ids of verified payments
# use a database instead of files in production
VERIFIED_PAYMENTS = "paypal_verified_payments.txt"


def verify_payment(payment_client):
    """Verify credit card of paypal payment made using rest apis
    https://developer.paypal.com/docs/integration/mobile/verify-mobile-payment/
    """
    payment_id = payment_client['response']['id']

    try:
        payment_server = paypalrestsdk.Payment.find(payment_id)

        if payment_server.state != 'approved':
            return False, 'Payment has not been approved yet. Status is ' + payment_server.state + '.'

        amount_client = payment_client['payment']['amount']
        currency_client = payment_client['payment']['currency_code']

        # Get most recent transaction
        transaction = payment_server.transactions[0]
        amount_server = transaction.amount.total
        currency_server = transaction.amount.currency
        sale_state = transaction.related_resources[0].sale.state

        if (amount_server != amount_client):
            return False, 'Payment amount does not match order.'
        elif (currency_client != currency_server):
            return False, 'Payment currency does not match order.'
        elif sale_state != 'completed':
            return False, 'Sale not completed.'
        elif used_payment(payment_id):
            return False, 'Payment already been verified.'
        else:
            return True, None

    except paypalrestsdk.ResourceNotFound:
        return False, 'Payment Not Found'


def used_payment(payment_id):
    """Make sure same payment does not get reused
    """
    pp_verified_payments = set([line.strip()
                                for line in open(VERIFIED_PAYMENTS, "rw")])
    if payment_id in pp_verified_payments:
        return True
    else:
        with open(VERIFIED_PAYMENTS, "a") as f:
            f.write(payment_id + "\n")
            return False


def add_consent(customer_id=None, auth_code=None):
    """Send authorization code after obtaining customer
    consent. Exchange for long living refresh token for
    creating payments in future
    """
    refresh_token = api.get_refresh_token(auth_code)
    save_refresh_token(customer_id, refresh_token)


def remove_consent(customer_id):
    """Remove previously granted consent by customer
    """
    customer_token_map = dict([line.strip().split(",")
                               for line in open(CUSTOMER_TOKEN_MAP)])
    customer_token_map.pop(customer_id, None)
    with open(CUSTOMER_TOKEN_MAP, "w") as f:
        for customer, token in customer_token_map:
            f.write(customer + "," + token + "\n")


def save_refresh_token(customer_id=None, refresh_token=None):
    """Store refresh token, likely in a database for app in production
    """
    with open(CUSTOMER_TOKEN_MAP, "a") as f:
        f.write(customer_id + "," + refresh_token + "\n")


def get_stored_refresh_token(customer_id=None):
    """If customer has already consented, return cached refresh token
    """
    try:
        customer_token_map = dict(
            [line.strip().split(",") for line in open(CUSTOMER_TOKEN_MAP)])
        return customer_token_map.get(customer_id)
    except (OSError, IOError):
        return None


def charge_wallet(transaction, customer_id=None, correlation_id=None, intent="authorize"):
    """Charge a customer who formerly consented to future payments
    from paypal wallet.
    """
    payment = paypalrestsdk.Payment({
        "intent": intent,
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": transaction["amount"]["total"],
                "currency": transaction["amount"]["currency"]
            },
            "description": transaction["description"]
        }]})

    refresh_token = get_stored_refresh_token(customer_id)

    if not refresh_token:
        return False, "Customer has not granted consent as no refresh token has been found for customer. Authorization code needed to get new refresh token."

    if payment.create(refresh_token, correlation_id):
        print("Payment %s created successfully" % (payment.id))
        if payment['intent'] == "authorize":
            authorization_id = payment['transactions'][0][
                'related_resources'][0]['authorization']['id']
            print(
                "Payment %s authorized. Authorization id is %s" % (
                    payment.id, authorization_id
                )
            )
        return True, "Charged customer " + customer_id + " " + transaction["amount"]["total"]
    else:
        return False, "Error while creating payment:" + str(payment.error)
