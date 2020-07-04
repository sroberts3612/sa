from test_helper import paypal, unittest
from mock import patch, ANY


class TestWebProfile(unittest.TestCase):

    def setUp(self):
        self.web_profile_attributes = {
            "name": "Best Brand Profile",
            "presentation": {
                "brand_name": "YeowZa Paypal",
                "logo_image": "https://www.paypalobjects.com/webstatic/mktg/logo/AM_SbyPP_mc_vs_dc_ae.jpg",
                "locale_code": "US"
            },
            "input_fields": {
                "allow_note": True,
                "no_shipping": 1,
                "address_override": 1
            },
            "flow_config": {
                "landing_page_type": "billing",
                "bank_txn_pending_url": "http://www.yeowza.com"
            }
        }
        self.web_profile = paypal.WebProfile(self.web_profile_attributes)
        self.profile_id = 'XP-UX9K-6ESG-TFUJ-TA6D'
        self.web_profile_create_response = {'presentation': {'locale_code': 'US', 'brand_name': 'YeowZa Paypal',
                                                             'logo_image': 'https://www.paypalobjects.com/webstatic/mktg/logo/AM_SbyPP_mc_vs_dc_ae.jpg'},
                                            'input_fields': {'allow_note': True, 'no_shipping': 1, 'address_override': 1},
                                            'name': 'BKJGUPDRFMCT', 'flow_config': {'landing_page_type': 'billing', 'bank_txn_pending_url': 'http://www.yeowza.com'},
                                            'id': 'XP-UX9K-6ESG-TFUJ-TA6D'}
        self.web_profile_replace_attributes = [
            {
                "op": "replace",
                "path": "/presentation/brand_name",
                "value": "New Brand Name"
            }
        ]

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        mock.return_value = self.web_profile_create_response
        response = self.web_profile.create()
        mock.assert_called_once_with(
            self.web_profile.api, '/v1/payment-experience/web-profiles', self.web_profile_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)
        self.assertNotEqual(self.web_profile.id, None)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        web_profile = paypal.WebProfile.find(self.profile_id)
        self.assertEqual(web_profile.__class__, paypal.WebProfile)
        mock.assert_called_once_with(
            web_profile.api, '/v1/payment-experience/web-profiles/' + self.profile_id, refresh_token=None)

    @patch('test_helper.paypal.Api.patch', autospec=True)
    def test_replace(self, mock):
        self.web_profile.id = self.profile_id
        response = self.web_profile.replace(
            self.web_profile_replace_attributes)

        mock.assert_called_once_with(self.web_profile.api, '/v1/payment-experience/web-profiles/' +
                                     self.profile_id, self.web_profile_replace_attributes, {'PayPal-Request-Id': ANY}, None)
        self.assertEqual(response, True)
