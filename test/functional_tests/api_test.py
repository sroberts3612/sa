from test_helper import unittest, client_id, client_secret, paypal


class Api(unittest.TestCase):

    api = paypal.Api(
        client_id=client_id,
        client_secret=client_secret)

    def test_endpoint(self):

        new_api = paypal.Api(
            mode="live", client_id="dummy", client_secret="dummy")
        self.assertEqual(new_api.endpoint, "https://api.paypal.com")
        self.assertEqual(new_api.token_endpoint, "https://api.paypal.com")

        new_api = paypal.Api(
            mode="sandbox", client_id="dummy", client_secret="dummy")
        self.assertEqual(new_api.endpoint, "https://api.sandbox.paypal.com")
        self.assertEqual(
            new_api.token_endpoint, "https://api.sandbox.paypal.com")

        new_api = paypal.Api(
            endpoint="https://custom-endpoint.paypal.com", client_id="dummy", client_secret="dummy")
        self.assertEqual(
            new_api.endpoint, "https://custom-endpoint.paypal.com")
        self.assertEqual(
            new_api.token_endpoint, "https://custom-endpoint.paypal.com")

    def test_get(self):
        payment_history = self.api.get("/v1/payments/payment?count=1")
        self.assertEqual(payment_history['count'], 1)

    def test_post(self):
        credit_card = self.api.post("v1/vault/credit-cards", {
            "type": "visa",
            "number": "4417119669820331",
            "expire_month": "11",
            "expire_year": "2018",
            "cvv2": "874",
            "first_name": "Joe",
            "last_name": "Shopper"})
        self.assertEqual(credit_card.get('error'), None)
        self.assertNotEqual(credit_card.get('id'), None)

    def test_bad_request(self):
        credit_card = self.api.post("v1/vault/credit-cards", {})
        self.assertNotEqual(credit_card.get('error'), None)

    def test_expired_token(self):
        old_token = self.api.get_access_token()
        self.assertNotEqual(old_token, None)
        self.api.token_hash["access_token"] = "ExpiredToken"
        new_token = self.api.get_access_token()
        self.assertEqual(new_token, "ExpiredToken")
        payment_history = self.api.get("/v1/payments/payment?count=1")
        self.assertEqual(payment_history['count'], 1)

    def test_expired_time(self):
        self.api.token_hash["access_token"] = "ExpiredToken"
        self.api.token_hash["expires_in"] = 0
        new_token = self.api.get_access_token()
        self.assertNotEqual(new_token, "ExpiredToken")

    def test_not_found(self):
        self.assertRaises(
            paypal.ResourceNotFound, self.api.get, ("/v1/payments/payment/PAY-1234"))
