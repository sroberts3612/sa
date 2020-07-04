from test_helper import unittest, paypal, client_id, client_secret, assert_regex_matches
from paypalrestsdk.openid_connect import Tokeninfo, Userinfo, authorize_url, logout_url, endpoint


class TestTokeninfo(unittest.TestCase):

    def test_create(self):
        self.assertRaises(
            paypal.ResourceNotFound, Tokeninfo.create, "invalid-code")

    def test_userinfo(self):
        self.assertRaises(paypal.UnauthorizedAccess, Tokeninfo().userinfo, {})

    def test_refresh(self):
        self.assertRaises(paypal.ResourceNotFound, Tokeninfo().refresh, {})

    def test_create_with_refresh_token(self):
        self.assertRaises(
            paypal.ResourceNotFound, Tokeninfo.create_with_refresh_token, "invalid-token")


class TestUserinfo(unittest.TestCase):

    def test_get(self):
        self.assertRaises(paypal.UnauthorizedAccess, Userinfo.get, "invalid")


class TestUrls(unittest.TestCase):

    def test_authorize_url(self):
        url = authorize_url()
        assert_regex_matches(self, url, 'response_type=code')
        assert_regex_matches(self, url, 'scope=openid')
        assert_regex_matches(self, url, 'client_id=%s' % (client_id))
        assert_regex_matches(self, url, 'https://www.sandbox.paypal.com')

        self.assertEqual(endpoint(), 'https://api.sandbox.paypal.com')

    def test_live_mode_url(self):
        try:
            paypal.configure(
                mode='live', client_id=client_id, client_secret=client_secret)
            url = authorize_url()
            assert_regex_matches(self, url, 'response_type=code')
            assert_regex_matches(self, url, 'scope=openid')
            assert_regex_matches(self, url, 'client_id=%s' % (client_id))
            assert_regex_matches(self, url, 'https://www.paypal.com')

            self.assertEqual(endpoint(), 'https://api.paypal.com')
        finally:
            paypal.configure(
                mode='sandbox', client_id=client_id, client_secret=client_secret)

    def test_authorize_url_options(self):
        url = authorize_url({'scope': 'openid profile'})
        assert_regex_matches(self, url, 'scope=openid\+profile')

    def test_authorize_url_using_tokeninfo(self):
        url = Tokeninfo.authorize_url({'scope': 'openid profile'})
        assert_regex_matches(self, url, 'scope=openid\+profile')

    def test_logout_url(self):
        url = logout_url()
        assert_regex_matches(self, url, 'logout=true')

    def test_logout_url_options(self):
        url = logout_url({'id_token': '1234'})
        assert_regex_matches(self, url, 'id_token=1234')

    def test_logout_url_using_tokeninfo(self):
        url = Tokeninfo({'id_token': '1234'}).logout_url()
        assert_regex_matches(self, url, 'id_token=1234')
