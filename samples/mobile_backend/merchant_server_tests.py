from merchant_server import app
import paypal_client
import unittest
import json
from mock import patch, Mock


class TestMerchantServer(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a test client"""
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.response_dict = dict(
            create_time='2014-02-12T22:29:49Z',
            id='PAY-564191241M8701234KL57LXI',
            intent='sale',
            state='approved'
        )
        self.client_json = json.dumps(dict(
            response_type='payment',
            response=self.response_dict
        ))

    def test_empty_request(self):
        """Check that request without body raises 400"""
        rv = self.app.post('/client_responses')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('Invalid mobile client response', rv.data)

    def test_invalid_response_type(self):
        """Check invalid response type is handled properly"""
        json_data = json.dumps(dict(response_type='test', response='test'))
        rv = self.app.post(
            '/client_responses', data=json_data, content_type='application/json')
        self.assertEqual(rv.status_code, 400)
        self.assertIn('Invalid response type', rv.data)

    @patch('merchant_server.verify_payment')
    def test_verify_payment(self, mock):
        """verify correct response on successful paypal payment verification"""
        mock.return_value = True, None
        rv = self.app.post(
            '/client_responses', data=self.client_json, content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertIn('verified', rv.data)

    @patch('merchant_server.verify_payment')
    def test_verify_payment_twice_fails(self, mock):
        """Trying to verify an already verified payment is a bad request"""
        mock.return_value = True, None
        rv = self.app.post(
            '/client_responses', data=self.client_json, content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertIn('verified', rv.data)
        mock.return_value = False, 'Payment already been verified.'
        rv = self.app.post(
            '/client_responses', data=self.client_json, content_type='application/json')
        self.assertEqual(rv.status_code, 404)
        self.assertIn('Payment already been verified', rv.data)

    @patch('merchant_server.add_consent')
    def test_send_future_payment_consent(self, mock):
        """Test consent is received properly on merchant_server"""
        mock.return_value = None
        response_dict = dict(
            code='EBYhRW3ncivudQn8UopLp4A28xIlqPDpAoqd7bi'
        )
        client_dict = dict(
            environment='live',
            paypal_sdk_version='2.0.1',
            platform='iOS',
            product_name='PayPal iOS SDK'
        )
        json_data = json.dumps(dict(
            response_type='authorization_code',
            response=response_dict,
            customer_id='customer@gmail.com',
            client=client_dict
        ))
        rv = self.app.post(
            '/client_responses', data=json_data, content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertIn('Received consent', rv.data)


class TestPaypalClient(unittest.TestCase):

    def setUp(self):
        self.transaction = {
            "amount": {
                "total": "1.00",
                "currency": "USD"
            },
            "description": "This is the payment transaction description."
        }

    def test_get_stored_refresh_token(self):
        """Test that the correct refresh token is getting fetched for the customer"""
        paypal_client.save_refresh_token(
            'customer1@gmail.com', 'ref_token_sample')
        refresh_token = paypal_client.get_stored_refresh_token(
            'customer1@gmail.com')
        self.assertEqual(refresh_token, 'ref_token_sample')

    def test_remove_consent(self):
        """Test removing consent deletes stored refresh token"""
        paypal_client.save_refresh_token(
            'customer1@gmail.com', 'ref_token_sample')
        refresh_token = paypal_client.get_stored_refresh_token(
            'customer1@gmail.com')
        self.assertEqual(refresh_token, 'ref_token_sample')
        paypal_client.remove_consent('customer1@gmail.com')
        refresh_token = paypal_client.get_stored_refresh_token(
            'customer1@gmail.com')
        self.assertEqual(refresh_token, None)

    def test_charge_wallet_missing_consent(self):
        """Charging a new customer without consent will not work"""
        return_status, message = paypal_client.charge_wallet(
            self.transaction, 'new_customer@gmail.com', None, 'sale')
        self.assertEqual(return_status, False)
        self.assertIn("Customer has not granted consent", message)

    @patch('paypal_client.paypalrestsdk.Payment.create')
    @patch('paypal_client.get_stored_refresh_token')
    def test_charge_wallet_failure(self, mock_create, mock_token):
        """Test charge wallet fails with correct message"""
        mock_token.return_value = False
        mock_create.return_value = 'refresh_token'
        return_status, message = paypal_client.charge_wallet(
            self.transaction, 'customer1@gmail.com', 'correlation_id', 'sale')
        self.assertEqual(return_status, False)
        self.assertIn("Error while creating payment", message)

    @patch('paypal_client.paypalrestsdk.Payment.create')
    def test_charge_wallet_success(self, mock):
        mock.return_value = True
        paypal_client.save_refresh_token(
            'customer1@gmail.com', 'ref_token_sample')
        return_status, message = paypal_client.charge_wallet(
            self.transaction, 'customer1@gmail.com', 'correlation_id', 'sale')
        self.assertEqual(return_status, True)
        self.assertIn("Charged customer customer1@gmail.com " +
                      self.transaction["amount"]["total"], message)
