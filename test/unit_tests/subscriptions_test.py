from test_helper import paypal, unittest
from mock import patch, ANY

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class TestBillingPlan(unittest.TestCase):

    def setUp(self):
        self.billing_plan_attributes = {
            "description": "Create Plan for Regular",
            "merchant_preferences": {
                "auto_bill_amount": "yes",
                "cancel_url": "http://www.cancel.com",
                "initial_fail_amount_action": "continue",
                "max_fail_attempts": "1",
                "return_url": "http://www.success.com",
                "setup_fee": {
                    "currency": "USD",
                    "value": "25"
                }
            },
            "name": "Testing1-Regular1",
            "payment_definitions": [
                {
                    "amount": {
                        "currency": "USD",
                        "value": "100"
                    },
                    "charge_models": [
                        {
                            "amount": {
                                "currency": "USD",
                                "value": "10.60"
                            },
                            "type": "SHIPPING"
                        },
                        {
                            "amount": {
                                "currency": "USD",
                                "value": "20"
                            },
                            "type": "TAX"
                        }
                    ],
                    "cycles": "0",
                    "frequency": "MONTH",
                    "frequency_interval": "1",
                    "name": "Regular 1",
                    "type": "REGULAR"
                },
                {
                    "amount": {
                        "currency": "USD",
                        "value": "20"
                    },
                    "charge_models": [
                        {
                            "amount": {
                                "currency": "USD",
                                "value": "10.60"
                            },
                            "type": "SHIPPING"
                        },
                        {
                            "amount": {
                                "currency": "USD",
                                "value": "20"
                            },
                            "type": "TAX"
                        }
                    ],
                    "cycles": "4",
                    "frequency": "MONTH",
                    "frequency_interval": "1",
                    "name": "Trial 1",
                    "type": "TRIAL"
                }
            ],
            "type": "INFINITE"
        }
        self.billing_plan_update_attributes = [
            {
                "op": "replace",
                "path": "/",
                "value": {
                    "state": "ACTIVE"
                }
            }
        ]
        self.billing_plan = paypal.BillingPlan(self.billing_plan_attributes)
        self.billing_plan_id = 'P-0NJ10521L3680291SOAQIVTQ'

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        response = self.billing_plan.create()

        mock.assert_called_once_with(self.billing_plan.api, 'v1/payments/billing-plans',
                                     self.billing_plan_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        billing_plan = paypal.BillingPlan.find(self.billing_plan_id)

        mock.assert_called_once_with(
            self.billing_plan.api, 'v1/payments/billing-plans/' + self.billing_plan_id, refresh_token=None)
        self.assertTrue(isinstance(billing_plan, paypal.BillingPlan))

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_all(self, mock):
        mock.return_value = {'plans': [self.billing_plan_attributes]}
        history = paypal.BillingPlan.all({'status': 'CREATED'})

        mock.assert_called_once_with(
            self.billing_plan.api, 'v1/payments/billing-plans?status=CREATED')
        self.assertEqual(len(history.plans), 1)

    @patch('test_helper.paypal.Api.patch', autospec=True)
    def test_replace(self, mock):
        self.billing_plan.id = self.billing_plan_id
        response = self.billing_plan.replace(
            self.billing_plan_update_attributes)

        mock.assert_called_once_with(self.billing_plan.api, 'v1/payments/billing-plans/' +
                                     self.billing_plan_id, self.billing_plan_update_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.patch', autospec=True)
    def test_activate(self, mock):
        self.billing_plan.id = self.billing_plan_id
        response = self.billing_plan.activate()

        mock.assert_called_once_with(self.billing_plan.api, 'v1/payments/billing-plans/' +
                                     self.billing_plan_id, self.billing_plan_update_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)


class TestBillingAgreement(unittest.TestCase):

    def setUp(self):
        self.billing_agreement_attributes = {
            "name": "Fast Speed Agreement",
            "description": "Agreement for Fast Speed Plan",
            "start_date": "2015-02-19T00:37:04Z",
            "plan": {
                "id": "P-0NJ10521L3680291SOAQIVTQ"
            },
            "payer": {
                "payment_method": "paypal"
            },
            "shipping_address": {
                "line1": "StayBr111idge Suites",
                "line2": "Cro12ok Street",
                "city": "San Jose",
                "state": "CA",
                "postal_code": "95112",
                "country_code": "US"
            }
        }

        self.billing_agreement_attributes_created = {
            "name": "Fast Speed Agreement",
            "description": "Agreement for Fast Speed Plan",
            "links": [
                {
                    "href": "https://localhost/cgi-bin/webscr?cmd=_express-checkout&token=EC-7MD89916KU283780J",
                    "rel": "approval_url",
                    "method": "REDIRECT"
                },
                {
                    "href": "https://api.sandbox.paypal.com/v1/payments/billing-agreements/EC-7MD89916KU283780J/agreement-execute",
                    "rel": "execute",
                    "method": "POST"
                }
            ],
            "start_date": "2015-02-19T00:37:04Z",
            "plan": {
                "id": "P-0NJ10521L3680291SOAQIVTQ",
                "state": "ACTIVE",
                "name": "Fast Speed Plan",
                "description": "Template creation.",
                "type": "FIXED",
                "payment_definitions": [{
                    "id": "PD-0NJ10521L3680291SOAQIVTQ",
                    "name": "Payment Definition-1",
                    "type": "REGULAR",
                    "frequency": "Month",
                    "frequency_interval": "2",
                    "amount": {
                        "value": "100"
                    }
                }],
                "currency_code": "USD"
            }
        }

        self.billing_agreement_update_attributes = [
            {
                "op": "replace",
                "path": "/",
                "value": {
                    "description": "New Description",
                    "name": "New Name",
                    "shipping_address": {
                        "line1": "StayBr111idge Suites",
                        "line2": "Cro12ok Street",
                        "city": "San Jose",
                        "state": "CA",
                        "postal_code": "95112",
                        "country_code": "US"
                    }
                }
            }
        ]

        self.billing_agreement_executed_attributes = {
            "id": "I-THNVHK6X9H0V",
            "links": [{
                "href": "https://api.sandbox.paypal.com/v1/payments/billing-agreements/I-THNVHK6X9H0V",
                "rel": "self",
                "method": "GET"
            }]
        }

        self.billing_agreement = paypal.BillingAgreement(
            self.billing_agreement_attributes)
        self.billing_agreement_id = "I-THNVHK6X9H0V"
        self.ec_token = "EC-7MD89916KU283780J"

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        response = self.billing_agreement.create()

        mock.assert_called_once_with(self.billing_agreement.api, 'v1/payments/billing-agreements',
                                     self.billing_agreement_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):

        billing_agreement = paypal.BillingAgreement.find(
            self.billing_agreement_id)

        mock.assert_called_once_with(
            self.billing_agreement.api, 'v1/payments/billing-agreements/' + self.billing_agreement_id, refresh_token=None)
        self.assertTrue(isinstance(billing_agreement, paypal.BillingAgreement))

    @patch('test_helper.paypal.Api.patch', autospec=True)
    def test_replace(self, mock):
        self.billing_agreement.id = self.billing_agreement_id
        response = self.billing_agreement.replace(
            self.billing_agreement_update_attributes)

        mock.assert_called_once_with(self.billing_agreement.api, 'v1/payments/billing-agreements/' +
                                     self.billing_agreement_id, self.billing_agreement_update_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_search_transactions(self, mock):
        start_date = "2014-07-20"
        end_date = "2014-07-30"
        mock.return_value = {
            "agreement_transaction_list": [
                {
                    "transaction_id": "I-HT38K76XPMGJ",
                    "status": "Created",
                    "transaction_type": "Recurring Payment",
                    "amount": "",
                    "fee_amount": "",
                    "net_amount": "",
                    "currency_code": "",
                    "payer_email": "",
                    "payer_name": "Jose Ramirez",
                    "time_stamp": "2014-07-29T13:05:48Z",
                    "time_zone": "GMT"
                },
                {
                    "transaction_id": "18972938Y4931603B",
                    "status": "Completed",
                    "transaction_type": "Recurring Payment",
                    "amount": "1.00",
                    "fee_amount": "-0.33",
                    "net_amount": "0.67",
                    "currency_code": "USD",
                    "payer_email": "sai@paypal.com",
                    "payer_name": "Jose Ramirez",
                    "time_stamp": "2014-07-29T13:06:04Z",
                    "time_zone": "GMT"
                }
            ]
        }
        self.billing_agreement.id = self.billing_agreement_id
        transactions = self.billing_agreement.search_transactions(
            start_date, end_date)
        mock.assert_called_once_with(self.billing_agreement.api, 'v1/payments/billing-agreements/' + self.billing_agreement_id
                                     + '/transactions?start_date=' + start_date + '&end_date=' + end_date)
        self.assertEqual(len(transactions.agreement_transaction_list), 2)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_suspend(self, mock):
        suspend_attributes = {
            "note": "Suspending the agreement"
        }
        self.billing_agreement.id = self.billing_agreement_id
        response = self.billing_agreement.suspend(suspend_attributes)

        mock.assert_called_once_with(self.billing_agreement.api, 'v1/payments/billing-agreements/' + self.billing_agreement_id + '/suspend',
                                     suspend_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_reactivate(self, mock):
        reactivate_attributes = {
            "note": "Reactivating the agreement"
        }
        self.billing_agreement.id = self.billing_agreement_id
        response = self.billing_agreement.reactivate(reactivate_attributes)

        mock.assert_called_once_with(self.billing_agreement.api, 'v1/payments/billing-agreements/' + self.billing_agreement_id + '/re-activate',
                                     reactivate_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_cancel(self, mock):
        cancel_attributes = {
            "note": "Canceling the agreement"
        }
        self.billing_agreement.id = self.billing_agreement_id
        response = self.billing_agreement.cancel(cancel_attributes)

        mock.assert_called_once_with(self.billing_agreement.api, 'v1/payments/billing-agreements/' + self.billing_agreement_id + '/cancel',
                                     cancel_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_set_balance(self, mock):
        set_balance_attributes = {
            "value": "10",
            "currency": "USD"
        }
        self.billing_agreement.id = self.billing_agreement_id
        response = self.billing_agreement.set_balance(set_balance_attributes)

        mock.assert_called_once_with(self.billing_agreement.api, 'v1/payments/billing-agreements/' + self.billing_agreement_id + '/set-balance',
                                     set_balance_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_bill_balance(self, mock):
        bill_balance_attributes = {
            "note": "Billing Balance Amount",
            "amount": {
                "value": "10",
                "currency": "USD"
            }
        }
        self.billing_agreement.id = self.billing_agreement_id
        response = self.billing_agreement.bill_balance(bill_balance_attributes)

        mock.assert_called_once_with(self.billing_agreement.api, 'v1/payments/billing-agreements/' + self.billing_agreement_id + '/bill-balance',
                                     bill_balance_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_execute(self, mock):
        mock.return_value = self.billing_agreement_executed_attributes

        response = self.billing_agreement.execute(self.ec_token)
        # Test that execute actually makes a http post to the href element of
        # links array with id
        execute_url = [link['href'] for link in self.billing_agreement_attributes_created.get(
            'links') if link['rel'] == 'execute'][0]
        execute_url_path = urlparse(execute_url).path[1:]

        mock.assert_called_with(
            self.billing_agreement.api, execute_url_path, {})
