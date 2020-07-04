from test_helper import paypal, unittest
import random
import string
from mock import patch, ANY


class TestInvoiceTemplate(unittest.TestCase):

    def setUp(self):
        self.invoice_template_attributes = {
            "name": "Hours Template_".join([random.choice(string.ascii_uppercase) for i in range(5)]),
            "default": True,
            "unit_of_measure": "HOURS",
            "template_data": {
                "items": [{
                        "name": "Nutri Bullet",
                        "quantity": 1,
                        "unit_price": {
                            "currency": "USD",
                            "value": "50.00"
                        }
                    }
                ],
                "merchant_info": {
                    "email": "stevendcoffey-facilitator@gmail.com"
                },
                "tax_calculated_after_discount": False,
                "tax_inclusive": False,
                "note": "Thank you for your business.",
                "logo_url": "https://pics.paypal.com/v1/images/redDot.jpeg"
            },
            "settings": [
                {
                    "field_name": "items.date",
                    "display_preference": {
                        "hidden": True
                    }
                },
                {
                    "field_name": "custom",
                    "display_preference": {
                        "hidden": True
                    }
                }
            ]
        }
        self.invoice_template = paypal.InvoiceTemplate(self.invoice_template_attributes)
        self.invoice_template.template_id = 'TEMP-XYZ'

    def test_getitem_override_reads_id_as_template_id(self):
        attributes = self.invoice_template_attributes.copy()
        attributes["id"] = "wrong"
        attributes["template_id"] = "right"

        invoice_template = paypal.InvoiceTemplate(attributes)
        self.assertEqual(invoice_template["id"], "right")

    @patch('test_helper.paypal.Api.post', autospec=True)
    def test_create(self, mock):
        invoice_template = paypal.InvoiceTemplate(self.invoice_template_attributes)
        response = invoice_template.create()

        mock.assert_called_once_with(self.invoice_template.api,
                'v1/invoicing/templates', self.invoice_template_attributes, {'PayPal-Request-Id': invoice_template.request_id}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.delete', autospec=True)
    def test_delete(self, mock):
        response = self.invoice_template.delete()
        mock.assert_called_once_with(self.invoice_template.api,
                'v1/invoicing/templates/' + self.invoice_template.template_id)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.put', autospec=True)
    def test_update(self, mock):
        response = self.invoice_template.update(self.invoice_template_attributes)

        mock.assert_called_once_with(self.invoice_template.api,
                'v1/invoicing/templates/' + self.invoice_template.template_id, 
                self.invoice_template_attributes, {'PayPal-Request-Id': self.invoice_template.request_id}, None)
        self.assertEqual(response, True)

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_find(self, mock):
        invoice_template = paypal.InvoiceTemplate.find(self.invoice_template.template_id)

        mock.assert_called_once_with(self.invoice_template.api,
                'v1/invoicing/templates/' + self.invoice_template.template_id, refresh_token=None)
        self.assertTrue(isinstance(invoice_template, paypal.InvoiceTemplate))

    @patch('test_helper.paypal.Api.get', autospec=True)
    def test_all(self, mock):
        mock.return_value = {
            'total_count': 1,
            'templates': [self.invoice_template]
        }
        history = paypal.InvoiceTemplate.all()

        mock.assert_called_once_with(self.invoice_template.api,
            'v1/invoicing/templates')
        self.assertEqual(history.total_count, 1)
        self.assertTrue(isinstance(history.templates[0], paypal.InvoiceTemplate))




