from test_helper import paypal, unittest
from mock import patch


class TestCreditCard(unittest.TestCase):

    def setUp(self):
        self.credit_card_attributes = {
            "type": "visa",
            "number": "4417119669820331",
            "expire_month": "11",
            "expire_year": "2018",
            "cvv2": "874",
            "first_name": "Joe",
            "last_name": "Shopper"}
        self.credit_card = paypal.CreditCard(self.credit_card_attributes)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        '''
        Check that a request id has been created and the mock post method
        has been called with the instance of api object, correct route and
        api credentials
        '''

        response = self.credit_card.create()
        self.assertNotEqual(self.credit_card.request_id, None)
        mock.assert_called_once_with(self.credit_card.api, 'v1/vault/credit-cards',
                                     self.credit_card_attributes, {'PayPal-Request-Id': self.credit_card.request_id}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        '''
        Check correct endpoint requested for finding a credit_card
        and the response of credit card type
        '''

        self.credit_card.id = 'CARD-6KP075290X361673LKLKB24A'
        card = paypal.CreditCard.find(self.credit_card.id)
        # python 2.6 compatible
        mock.assert_called_once_with(
            self.credit_card.api, 'v1/vault/credit-cards/' + self.credit_card.id, refresh_token=None)
        self.assertTrue(isinstance(card, paypal.CreditCard))

    @patch('test_helper.paypal.Api.delete', autospec=True)
    def test_delete(self, mock):
        '''
        Check correct endpoint requested for deleting a card
        from vault
        '''

        self.credit_card.id = 'CARD-6KP075290X361673LKLKB24A'
        response = self.credit_card.delete()
        mock.assert_called_once_with(
            self.credit_card.api, 'v1/vault/credit-cards/' + self.credit_card.id)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_duplicate_request_id(self, mock):
        '''
        Test that credit card with identical attributes and request id
        returns the credit card already created. Request id must be the
        same for idempotency
        '''

        response = self.credit_card.create()
        mock.assert_called_once_with(self.credit_card.api, 'v1/vault/credit-cards',
                                     self.credit_card_attributes, {'PayPal-Request-Id': self.credit_card.request_id}, None)
        self.assertEqual(response, True)

        duplicate_card = paypal.CreditCard(self.credit_card_attributes)
        duplicate_card.request_id = self.credit_card.request_id
        duplicate_card_response = duplicate_card.create()

        mock.assert_called_with(self.credit_card.api, 'v1/vault/credit-cards',
                                self.credit_card_attributes, {'PayPal-Request-Id': self.credit_card.request_id}, None)
        self.assertEqual(mock.call_count, 2)
        self.assertEqual(duplicate_card_response, True)
        self.assertEqual(duplicate_card.id, self.credit_card.id)
