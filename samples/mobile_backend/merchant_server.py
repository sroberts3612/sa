# Flask application for a developer/merchant verifying payments and executing
# payments on behalf of customer who has consented to future payments

from flask import Flask, request, jsonify
from paypal_client import verify_payment, add_consent, charge_wallet

app = Flask(__name__)


@app.route('/client_responses', methods=['POST'])
def parse_response():
    """Check validity of a mobile payment made via credit card or PayPal,
    or save customer consented to future payments
    """
    if not request.json or not 'response' or 'response_type' not in request.json:
        raise InvalidUsage('Invalid mobile client response ')

    if request.json['response_type'] == 'payment':
        result, message = verify_payment(request.json)
        if result:
            return jsonify({"status": "verified"}), 200
        else:
            raise InvalidUsage(message, status_code=404)

    elif request.json['response_type'] == 'authorization_code':
        add_consent(request.json['customer_id'],
                    request.json['response']['code'])
        return jsonify({"status": "Received consent"}), 200

    else:
        raise InvalidUsage('Invalid response type')


@app.route('/correlations', methods=['POST'])
def correlations():
    """Send correlation id, customer id (e.g email) and transactions details for
    purchase made by customer who formerly consented to future payments.
    Can be used for immediate payments or authorize a payment for later execution

    https://developer.paypal.com/docs/integration/direct/capture-payment/
    """
    result, message = charge_wallet(
        transaction=request.json['transactions'][
            0], customer_id=request.json['customer_id'],
        correlation_id=request.json[
            'correlation_id'], intent=request.json['intent']
    )
    if result:
        return jsonify({"status": message}), 200
    else:
        raise InvalidUsage(message)


class InvalidUsage(Exception):

    """Errorhandler class to enable custom error message propagation
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
