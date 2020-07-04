from test_helper import paypal, unittest
from mock import patch, ANY
import zlib
import json


class TestWebhook(unittest.TestCase):

    def setUp(self):
        self.webhook_event_types = [
            {
                "name": "PAYMENT.AUTHORIZATION.CREATED"
            },
            {
                "name": "PAYMENT.AUTHORIZATION.VOIDED"
            }
        ]
        self.webhook_attributes = {
            "url": "https://www.yeowza.com/ppwebhook",
            "event_types": self.webhook_event_types
        }

        self.webhook = paypal.Webhook(self.webhook_attributes)
        self.webhook_id = '6HY79521VR978045E'

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        response = self.webhook.create()

        mock.assert_called_once_with(self.webhook.api, '/v1/notifications/webhooks/',
                                     self.webhook_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_get_event_types(self, mock):
        self.webhook.id = self.webhook_id
        event_types = self.webhook.get_event_types()
        mock.assert_called_once_with(
            self.webhook.api, '/v1/notifications/webhooks/' + self.webhook_id + '/event-types')


class TestWebhookEvents(unittest.TestCase):

    def setUp(self):
        self.webhook_event_id = 'WH-1S115631EN580315E-9KH94552VF7913711'
        self.event_body = '{"id":"WH-0G2756385H040842W-5Y612302CV158622M","create_time":"2015-05-18T15:45:13Z","resource_type":"sale","event_type":"PAYMENT.SALE.COMPLETED","summary":"Payment completed for $ 20.0 USD","resource":{"id":"4EU7004268015634R","create_time":"2015-05-18T15:44:02Z","update_time":"2015-05-18T15:44:21Z","amount":{"total":"20.00","currency":"USD"},"payment_mode":"INSTANT_TRANSFER","state":"completed","protection_eligibility":"ELIGIBLE","protection_eligibility_type":"ITEM_NOT_RECEIVED_ELIGIBLE,UNAUTHORIZED_PAYMENT_ELIGIBLE","parent_payment":"PAY-86C81811X5228590KKVNARQQ","transaction_fee":{"value":"0.88","currency":"USD"},"links":[{"href":"https://api.sandbox.paypal.com/v1/payments/sale/4EU7004268015634R","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v1/payments/sale/4EU7004268015634R/refund","rel":"refund","method":"POST"},{"href":"https://api.sandbox.paypal.com/v1/payments/payment/PAY-86C81811X5228590KKVNARQQ","rel":"parent_payment","method":"GET"}]},"links":[{"href":"https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-0G2756385H040842W-5Y612302CV158622M","rel":"self","method":"GET"},{"href":"https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-0G2756385H040842W-5Y612302CV158622M/resend","rel":"resend","method":"POST"}]}'
        self.transmission_id = "dfb3be50-fd74-11e4-8bf3-77339302725b"
        self.timestamp = "2015-05-18T15:45:13Z"
        self.webhook_id = "4JH86294D6297924G"
        self.actual_signature = "thy4/U002quzxFavHPwbfJGcc46E8rc5jzgyeafWm5mICTBdY/8rl7WJpn8JA0GKA+oDTPsSruqusw+XXg5RLAP7ip53Euh9Xu3UbUhQFX7UgwzE2FeYoY6lyRMiiiQLzy9BvHfIzNIVhPad4KnC339dr6y2l+mN8ALgI4GCdIh3/SoJO5wE64Bh/ueWtt8EVuvsvXfda2Le5a2TrOI9vLEzsm9GS79hAR/5oLexNz8UiZr045Mr5ObroH4w4oNfmkTaDk9Rj0G19uvISs5QzgmBpauKr7Nw++JI0pr/v5mFctQkoWJSGfBGzPRXawrvIIVHQ9Wer48GR2g9ZiApWg=="
        self.cert_url = 'https://api.sandbox.paypal.com/v1/notifications/certs/CERT-360caa42-fca2a594-a5cafa77'
        self.expected_signature = self.transmission_id + "|" + self.timestamp + "|" + \
            self.webhook_id + "|" + \
            str(zlib.crc32(self.event_body.encode('utf-8')) & 0xffffffff)

    @patch('test_helper.paypal.Api.get', autospec=True)
    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_find_and_resend(self, mock_post, mock_get):
        webhook_event = paypal.WebhookEvent.find(self.webhook_event_id)
        mock_get.assert_called_once_with(
            webhook_event.api, '/v1/notifications/webhooks-events/' + self.webhook_event_id, refresh_token=None)
        self.assertTrue(isinstance(webhook_event, paypal.WebhookEvent))
        webhook_event.id = self.webhook_event_id

        response = webhook_event.resend()
        mock_post.assert_called_once_with(
            webhook_event.api, '/v1/notifications/webhooks-events/' + self.webhook_event_id + '/resend', {}, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)

    def test_verify_signature(self):
        cert = paypal.WebhookEvent._get_cert(self.cert_url)
        response = paypal.WebhookEvent._verify_signature(
            self.transmission_id, self.timestamp, self.webhook_id, self.event_body, cert, self.actual_signature, 'sha256')
        self.assertEqual(response, True)

    def test_verify(self):
        response = paypal.WebhookEvent.verify(
            self.transmission_id, self.timestamp, self.webhook_id, self.event_body, self.cert_url, self.actual_signature, 'sha256')
        self.assertEqual(response, True)

    def test_verify_with_auth_algo_header(self):
        # Test digest method mapping works
        response = paypal.WebhookEvent.verify(
            self.transmission_id, self.timestamp, self.webhook_id, self.event_body, self.cert_url, self.actual_signature, 'SHA256withRSA')
        self.assertEqual(response, True)

    def test_verify_with_auth_algo_value(self):
        # Test digest method mapped value passed in directly works
        response = paypal.WebhookEvent.verify(
            self.transmission_id, self.timestamp, self.webhook_id, self.event_body, self.cert_url, self.actual_signature, 'sha256WithRSAEncryption')
        self.assertEqual(response, True)

    def test_verify_with_invalid_auth_algo_name(self):
        response = paypal.WebhookEvent.verify(
            self.transmission_id, self.timestamp, self.webhook_id, self.event_body, self.cert_url, self.actual_signature, 'invalid_digest_method')
        self.assertEqual(response, False)

    def test_verify_with_incorrect_auth_algo(self):
        response = paypal.WebhookEvent.verify(
            self.transmission_id, self.timestamp, self.webhook_id, self.event_body, self.cert_url, self.actual_signature, 'SHA1withRSA')
        self.assertEqual(response, False)

    def test_verify_certificate(self):
        cert = paypal.WebhookEvent._get_cert(self.cert_url)
        response = paypal.WebhookEvent._verify_certificate(cert)
        self.assertEqual(response, True)

    def test_get_expected_sig(self):
        expected_sig = paypal.WebhookEvent._get_expected_sig(
            self.transmission_id, self.timestamp, self.webhook_id, self.event_body)
        self.assertEqual(expected_sig, self.expected_signature)

    def test_get_resource(self):
        webhook_event = paypal.WebhookEvent(json.loads(self.event_body))
        event_resource = webhook_event.get_resource()
        self.assertTrue(isinstance(event_resource, paypal.Sale))

    def test_get_cert(self):
        cert = paypal.WebhookEvent._get_cert(self.cert_url)
        self.assertNotEqual(cert, None)

    def test_is_common_name_valid(self):
        cert = paypal.WebhookEvent._get_cert(self.cert_url)
        response = paypal.WebhookEvent._is_common_name_valid(cert)
        self.assertEqual(response, True)

    def test_get_certificate_store(self):
        store = paypal.WebhookEvent._get_certificate_store()
        from OpenSSL import crypto
        self.assertTrue(isinstance(store, crypto.X509Store))

    def test_verify_certificate_chain(self):
        cert = paypal.WebhookEvent._get_cert(self.cert_url)
        response = paypal.WebhookEvent._verify_certificate_chain(cert)
        self.assertEqual(response, True)
