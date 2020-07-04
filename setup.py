from distutils.core import setup

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'paypalrestsdk'))
from config import __version__, __pypi_packagename__, __github_username__, __github_reponame__

long_description="""
    The PayPal REST SDK provides Python APIs to create, process and manage payments.

    1. https://github.com/paypal/PayPal-Python-SDK/ - README and Samples
    2. https://developer.paypal.com/webapps/developer/docs/api/ - API Reference
  """

license='PayPal SDK License'

url='https://github.com/' + __github_username__ + '/' + __github_reponame__

setup(
  name=__pypi_packagename__,
  version= __version__,
  author='PayPal',
  author_email='DL-PP-PYTHON-SDK@paypal.com',
  packages=['paypalrestsdk'],
  scripts=[],
  url=url,
  license=license,
  description='The PayPal REST SDK provides Python APIs to create, process and manage payments.',
  long_description=long_description,
  package_data={'paypalrestsdk': ['data/*.crt.pem']},
  install_requires=['requests>=1.0.0', 'six>=1.0.0', 'pyopenssl>=0.15'],
  classifiers=[
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  keywords=['paypal', 'rest', 'sdk', 'payments', 'invoice', 'subscription', 'webhook']
)
