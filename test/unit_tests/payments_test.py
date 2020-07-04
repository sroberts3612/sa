from test_helper import paypal, unittest
from mock import patch, ANY


class TestPayment(unittest.TestCase):

    def setUp(self):
        self.payment_attributes = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                      "credit_card": {
                          "type": "visa",
                          "number": "4417119669820331",
                          "expire_month": "11",
                          "expire_year": "2018",
                          "cvv2": "874",
                          "first_name": "Joe",
                          "last_name": "Shopper"}}]},
            "transactions": [{
                "item_list": {
                      "items": [{
                          "name": "item",
                          "sku": "item",
                          "price": "1.00",
                          "currency": "USD",
                          "quantity": 1}]},
                "amount": {
                      "total": "1.00",
                      "currency": "USD"},
                "description": "This is the payment transaction description."}]}
        self.payment = paypal.Payment(self.payment_attributes)
        self.refresh_token = 'long_living_refresh_token'
        self.correlation_id = 'paypal_application_correlation_id'

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        response = self.payment.create()
        self.assertNotEqual(self.payment.request_id, None)
        mock.assert_called_once_with(self.payment.api, 'v1/payments/payment',
                                     self.payment_attributes, {'PayPal-Request-Id': self.payment.request_id}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create_future_payment(self, mock):
        response = self.payment.create(
            refresh_token=self.refresh_token,
            correlation_id=self.correlation_id
        )
        self.assertNotEqual(self.payment.request_id, None)
        mock.assert_called_once_with(
            self.payment.api, 'v1/payments/payment',
            self.payment_attributes,
            {'PayPal-Request-Id': self.payment.request_id, 'Paypal-Application-Correlation-Id': self.correlation_id,
             'Paypal-Client-Metadata-Id': self.correlation_id}, self.refresh_token
        )
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_validation(self, mock):
        '''
        Check that validation fails on trying to create a payment
        with required fields missing
        '''

        payment = paypal.Payment({})
        mock.return_value = {'error': 'validation', 'message': 'Invalid request - see details',
                             'debug_id': 'b8ef6b0aa6329',
                             'information_link': 'https://developer.paypal.com/webapps/developer/docs/api/#VALIDATION_ERROR'
                             }
        response = payment.create()
        mock.assert_called_once_with(
            self.payment.api, 'v1/payments/payment', {}, {'PayPal-Request-Id': payment.request_id}, None)

        self.assertEqual(response, False)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_all(self, mock):
        mock.return_value = {'count': 1, 'next_id': 'PAY-5TU016908T094823BKLKU7MY', 'payments': [{'update_time': '2014-01-14T15:00:41Z', 'links': [],
                                                                                                  'payer': {'payment_method': 'paypal', 'payer_info': {}}, 'transactions': [], 'state': 'created', 'intent': 'sale', 'id': 'PAY-0A963503EW637094HKLKVCGI'}]}

        payment_history = paypal.Payment.all({"count": 1})

        mock.assert_called_once_with(
            self.payment.api, 'v1/payments/payment?count=1')
        self.assertEqual(payment_history.count, 1)

        self.assertEqual(payment_history.payments[0].__class__, paypal.Payment)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        mock.return_value = {'count': 1, 'next_id': 'PAY-5TU016908T094823BKLKU7MY', 'payments': [{'update_time': '2014-01-14T15:00:41Z', 'links': [],
                                                                                                  'payer': {'payment_method': 'paypal', 'payer_info': {}}, 'transactions': [], 'state': 'created', 'intent': 'sale', 'id': 'PAY-0A963503EW637094HKLKVCGI'}]}

        payment_history = paypal.Payment.all({"count": 1})
        mock.assert_called_once_with(
            self.payment.api, 'v1/payments/payment?count=1')

        payment_id = payment_history.payments[0]['id']
        mock.return_value = {'id': 'PAY-3KM36407UD294123NKLKV34I', 'intent': 'sale',
                             'state': 'completed', 'description': 'This is the payment transaction'}
        payment = paypal.Payment.find(payment_id)

        mock.assert_called_with(
            self.payment.api, 'v1/payments/payment/PAY-0A963503EW637094HKLKVCGI', refresh_token=None)

        self.assertNotEqual(payment.id, payment_id)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_not_found(self, mock):
        mock.side_effect = paypal.ResourceNotFound('', '')
        self.assertRaises(
            paypal.ResourceNotFound, paypal.Payment.find, ("PAY-1234"))

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_execute(self, mock):
        paypal_payment_attrib = {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment/execute",
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "1.00",
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": "1.00",
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]}
        payment = paypal.Payment(paypal_payment_attrib)
        mock.return_value = {'id': 'AY-7JD471929T152531RKLKWR6Q', 'intent': 'sale',
                             'state': 'completed', 'description': 'This is the payment transaction'}

        response = payment.create()
        mock.assert_called_once_with(self.payment.api, 'v1/payments/payment',
                                     paypal_payment_attrib, {'PayPal-Request-Id': payment.request_id}, None)
        self.assertEqual(response, True)

        payment.execute({'payer_id': 'HZH2W8NPXUE5W'})
        mock.assert_called_with(self.payment.api, 'v1/payments/payment/AY-7JD471929T152531RKLKWR6Q/execute', {
                                'payer_id': 'HZH2W8NPXUE5W'}, {'PayPal-Request-Id': ANY}, None)


class TestBillingPlan(unittest.TestCase):

    def setUp(self):
        super(TestBillingPlan, self).setUp()
        self.billing_plan = paypal.BillingPlan()

    @patch('test_helper.paypal.Api.post', autospec=True)
    @patch('test_helper.paypal.Api.patch', autospec=True)
    def test_activate_inactivate(self, patch_mock, post_mock):
        post_mock.return_value = {
            "id": "P-7DC96732KA7763723UOPKETA",
            "state": "CREATED",
        }
        patch_mock.side_effect =[
            {
                "id": "P-7DC96732KA7763723UOPKETA",
                "state": "ACTIVE",
            },
            {
                "id": "P-7DC96732KA7763723UOPKETA",
                "state": "INACTIVE",
            },
        ]

        response = self.billing_plan.create()
        self.assertTrue(response)
        self.assertEqual(self.billing_plan['state'], 'CREATED')

        response = self.billing_plan.activate()
        self.assertTrue(response)
        self.assertEqual(self.billing_plan['state'], 'ACTIVE')

        response = self.billing_plan.inactivate()
        self.assertTrue(response)
        self.assertEqual(self.billing_plan['state'], 'INACTIVE')


class TestSale(unittest.TestCase):

    def setUp(self):
        self.payment_attributes = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                      "credit_card": {
                          "type": "visa",
                          "number": "4417119669820331",
                          "expire_month": "11",
                          "expire_year": "2018",
                          "cvv2": "874",
                          "first_name": "Joe",
                          "last_name": "Shopper"}}]},
            "transactions": [{
                "item_list": {
                      "items": [{
                          "name": "item",
                          "sku": "item",
                          "price": "1.00",
                          "currency": "USD",
                          "quantity": 1}]},
                "amount": {
                      "total": "1.00",
                      "currency": "USD"},
                "description": "This is the payment transaction description."}]}
        self.payment = paypal.Payment(self.payment_attributes)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def create_sale(self, mock):
        mock.return_value = {
            'id': 'PAY-888868365Y436124EKLKW6JA',
            'update_time': '2014-01-14T17:09:00Z',
            'links': [],
            'payer': {},
            'transactions': [{
                'related_resources': [{
                    'sale': {
                        'update_time': '2014-01-14T17:09:00Z',
                        'links': [],
                        'state': 'completed',
                        'id': '5VX40080GX603650',
                        'amount': {'currency': 'USD', 'total': '1.00'},
                    },
                }],
            }]
        }
        response = self.payment.create()
        self.assertEqual(response, True)
        return self.payment.transactions[0].related_resources[0].sale

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        sale = paypal.Sale.find(self.create_sale().id)
        mock.assert_called_once_with(
            sale.api, 'v1/payments/sale/5VX40080GX603650', refresh_token=None)
        self.assertEqual(sale.__class__, paypal.Sale)


class TestRefund(unittest.TestCase):

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        refund_id = '5C377143F71265517'
        mock.return_value = {'update_time': '2013-04-01T08:44:09Z',
                             'sale_id': '7DY409201T7922549', 'state': 'completed', 'id': refund_id,
                             'amount': {'currency': 'USD', 'total': '0.01'}}
        refund = paypal.Refund.find(refund_id)
        mock.assert_called_once_with(
            refund.api, 'v1/payments/refund/' + refund_id, refresh_token=None)
        self.assertEqual(refund.__class__, paypal.Refund)


class TestPayout(unittest.TestCase):

    def setUp(self):
        self.batch_payout_attributes = {
            "sender_batch_header": {
                "sender_batch_id": "batch_32",
                "email_subject": "You have a payment"
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": 0.99,
                        "currency": "USD"
                    },
                    "receiver": "shirt-supplier-one@mail.com",
                    "note": "Thank you.",
                    "sender_item_id": "item_1"
                },
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": 0.90,
                        "currency": "USD"
                    },
                    "receiver": "shirt-supplier-two@mail.com",
                    "note": "Thank you.",
                    "sender_item_id": "item_2"
                },
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": 2.00,
                        "currency": "USD"
                    },
                    "receiver": "shirt-supplier-three@mail.com",
                    "note": "Thank you.",
                    "sender_item_id": "item_3"
                }
            ]
        }

        self.payout_response_attr = {
            "batch_header": {
                "payout_batch_id": "H4HF4AT2GZXQN",
                "batch_status": "PENDING",
                "sender_batch_header": {
                    "email_subject": "You have a payment",
                    "sender_batch_id": "batch_25"
                }
            },
            "links": [
                {
                    "href": "https://api.sandbox.paypal.com/v1/payments/payouts/H4HF4AT2GZXQN",
                    "rel": "self",
                    "method": "GET"
                }
            ]
        }

        self.single_payout_attributes = {
            "sender_batch_header": {
                "sender_batch_id": "batch_25",
                "email_subject": "You have a payment"
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": 0.99,
                        "currency": "USD"
                    },
                    "receiver": "shirt-supplier-one@mail.com",
                    "note": "Thank you.",
                    "sender_item_id": "item_1"
                }
            ]
        }

        self.payout_id = "R3LFR867ESVQY"

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create_batch_payout(self, mock):
        payout = paypal.Payout(self.batch_payout_attributes)
        mock.return_value = self.payout_response_attr
        response = payout.create()
        mock.assert_called_once_with(
            payout.api, '/v1/payments/payouts/', self.batch_payout_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create_single_payout(self, mock):
        payout = paypal.Payout(self.single_payout_attributes)
        mock.return_value = self.payout_response_attr
        response = payout.create(sync_mode=True)
        mock.assert_called_once_with(
            payout.api, '/v1/payments/payouts?sync_mode=true', self.single_payout_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)


class TestPayoutItem(unittest.TestCase):

    def setUp(self):
        self.payout_item_id = "R3LFR867ESVQY"

        self.single_payout_details = {
            "payout_item_id": "1421342",
            "transaction_id": "4345",
            "transaction_status": "SUCCESS",
            "payout_batch_id": "20140724",
            "payout_item": {
                "amount": {
                    "value": "9.87",
                    "currency": "USD"
                },
                "recipient_type": "EMAIL",
                "note": "Thanks for your patronage!",
                "receiver": "shirt-supplier@mail.com",
                "sender_item_id": "14Feb_234"
            },
            "time_created": "2014-01-27T10:17:00Z",
            "time_processed": "2014-01-27T10:17:41Z"
        }

        self.payout_item = paypal.PayoutItem(self.single_payout_details)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        payout_item = paypal.PayoutItem.find(self.payout_item_id)
        self.assertEqual(payout_item.__class__, paypal.PayoutItem)
        mock.assert_called_once_with(
            payout_item.api, '/v1/payments/payouts-item/' + self.payout_item_id, refresh_token=None)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_cancel(self, mock):
        response = self.payout_item.cancel()

        mock.assert_called_once_with(
            self.payout_item.api, '/v1/payments/payouts-item/' + self.payout_item.payout_item_id + '/cancel', {}, {'PayPal-Request-Id': ANY}, None)


class TestOrder(unittest.TestCase):

    def setUp(self):
        self.payment_attributes = {
            "intent": "order",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://return.url",
                "cancel_url": "http://cancel.url"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "1.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "currency": "USD",
                    "total": "1.00"
                },
                "description": "This is the payment description."
            }]
        }
        self.payment = paypal.Payment(self.payment_attributes)
        self.order_id = 'O-2HT09787H36911800'
        self.order_attributes = {'update_time': '2014-09-05T15:36:47Z',
                                 'links': [{'href': 'https://api.sandbox.paypal.com/v1/payments/orders/O-2HT09787H36911800', 'method': 'GET', 'rel': 'self'},
                                           {'href': 'https://api.sandbox.paypal.com/v1/payments/payment/PAY-9KG19994R2259015YKQE5QVY',
                                               'method': 'GET', 'rel': 'parent_payment'},
                                           {'href': 'https://api.sandbox.paypal.com/v1/payments/orders/O-2HT09787H36911800/do-void',
                                               'method': 'POST', 'rel': 'void'},
                                           {'href': 'https://api.sandbox.paypal.com/v1/payments/orders/O-2HT09787H36911800/authorize',
                                            'method': 'POST', 'rel': 'authorization'},
                                           {'href': 'https://api.sandbox.paypal.com/v1/payments/orders/O-2HT09787H36911800/capture', 'method': 'POST', 'rel': 'capture'}],
                                 'state': 'partially_captured', 'parent_payment': 'PAY-9KG19994R2259015YKQE5QVY',
                                 'amount': {'currency': 'USD', 'total': '1.00', 'details': {'subtotal': '1.00'}},
                                 'create_time': '2014-09-05T15:35:51Z', 'id': 'O-2HT09787H36911800'}
        self.capture_attributes = {
            "amount": {"currency": "USD", "total": "4.54"}, "is_final_capture": True}
        self.authorize_attributes = {
            "amount": {"currency": "USD", "total": "1.00"}}

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        mock.return_value = {'id': 'PAY-888868365Y436124EKLKW6JA', 'update_time': '2014-01-14T17:09:00Z', 'links': [], 'payer': {},
                             'transactions': [{'related_resources': [{'authorization': self.order_attributes}]}]}
        response = self.payment.create()
        mock.assert_called_once_with(self.payment.api, 'v1/payments/payment',
                                     self.payment_attributes, {'PayPal-Request-Id': self.payment.request_id}, None)
        self.assertEqual(response, True)
        self.assertNotEqual(
            self.payment.transactions[0].related_resources[0].authorization.id, None)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        order = paypal.Order.find(self.order_id)
        self.assertEqual(order.__class__, paypal.Order)
        mock.assert_called_once_with(
            order.api, 'v1/payments/orders/' + self.order_id, refresh_token=None)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_void(self, mock):
        order = paypal.Order.find(self.order_id)
        self.assertEqual(order.void(), True)
        mock.assert_called_once_with(order.api, 'v1/payments/orders/' + self.order_id + '/do-void', {},
                                     {'PayPal-Request-Id': ANY}, None)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_capture(self, mock):
        order = paypal.Order.find(self.order_id)
        capture = order.capture(self.capture_attributes)
        self.assertEqual(capture.success(), True)
        mock.assert_called_once_with(order.api, 'v1/payments/orders/' + self.order_id + '/capture', self.capture_attributes,
                                     {'PayPal-Request-Id': ANY}, None)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_authorize(self, mock):
        order = paypal.Order.find(self.order_id)
        authorization = order.authorize(self.authorize_attributes)
        self.assertEqual(order.success(), True)
        mock.assert_called_once_with(order.api, 'v1/payments/orders/' + self.order_id + '/authorize', self.authorize_attributes,
                                     {'PayPal-Request-Id': ANY}, None)


class TestAuthorization(unittest.TestCase):

    def setUp(self):
        self.payment_attributes = {
            "intent": "authorize",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": {
                        "type": "visa",
                        "number": "4417119669820331",
                        "expire_month": "11",
                        "expire_year": "2018",
                        "cvv2": "874",
                        "first_name": "Joe",
                        "last_name": "Shopper"}}]},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "1.00",
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": "1.00",
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]}
        self.payment = paypal.Payment(self.payment_attributes)
        self.auth_id = '3J872959AY1512221'
        self.authorization_attributes = {'valid_until': '2014-02-12T21:11:25Z',
                                         'update_time': '2014-01-14T21:11:33Z', 'links': [{'href': 'https://api.sandbox.paypal.com/v1/payments/authorization/3J872959AY1512221', 'method': 'GET', 'rel': 'self'},
                                                                                          {
                                                                                              'href': 'https://api.sandbox.paypal.com/v1/payments/authorization/3J872959AY1512221/capture', 'method': 'POST', 'rel': 'capture'},
                                                                                          {
                                                                                              'href': 'https://api.sandbox.paypal.com/v1/payments/authorization/3J872959AY1512221/void', 'method': 'POST', 'rel': 'void'},
                                                                                          {'href': 'https://api.sandbox.paypal.com/v1/payments/payment/PAY-1EE254486E964802VKLK2P7I', 'method': 'GET', 'rel': 'parent_payment'}],
                                         'state': 'authorized', 'parent_payment': 'PAY-1EE254486E964802VKLK2P7I', 'amount': {'currency': 'USD', 'total': '1.00', 'details': {'subtotal': '1.00'}},
                                         'create_time': '2014-01-14T21:11:25Z', 'id': '3J872959AY1512221'}
        self.capture_attributes = {
            "amount": {"currency": "USD", "total": "1.00"}}

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        mock.return_value = {'id': 'PAY-888868365Y436124EKLKW6JA', 'update_time': '2014-01-14T17:09:00Z', 'links': [], 'payer': {},
                             'transactions': [{'related_resources': [{'authorization': self.authorization_attributes}]}]}
        response = self.payment.create()
        mock.assert_called_once_with(self.payment.api, 'v1/payments/payment',
                                     self.payment_attributes, {'PayPal-Request-Id': self.payment.request_id}, None)
        self.assertEqual(response, True)
        self.assertNotEqual(
            self.payment.transactions[0].related_resources[0].authorization.id, None)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        authorization = paypal.Authorization.find(self.auth_id)
        self.assertEqual(authorization.__class__, paypal.Authorization)
        mock.assert_called_once_with(
            authorization.api, 'v1/payments/authorization/' + self.auth_id, refresh_token=None)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_capture(self, mock):
        authorization = paypal.Authorization.find(self.auth_id)
        capture = authorization.capture(self.capture_attributes)
        self.assertEqual(capture.success(), True)
        mock.assert_called_once_with(authorization.api, 'v1/payments/authorization/' + self.auth_id + '/capture', self.capture_attributes,
                                     {'PayPal-Request-Id': ANY}, None)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_void(self, mock):
        authorization = paypal.Authorization.find(self.auth_id)
        self.assertEqual(authorization.void(), True)
        mock.assert_called_once_with(authorization.api, 'v1/payments/authorization/' + self.auth_id + '/void', {},
                                     {'PayPal-Request-Id': ANY}, None)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_capture_find(self, mock):
        capture_id = '7S373777UY2709045'
        capture = paypal.Capture.find(capture_id)
        self.assertEqual(capture.__class__, paypal.Capture)
        mock.assert_called_once_with(
            capture.api, 'v1/payments/capture/' + capture_id, refresh_token=None)
