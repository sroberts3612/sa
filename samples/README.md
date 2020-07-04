# Running Samples

## System Requirements
PayPal SDK depends on the following system libraries:

* libssl-dev
* libffi-dev

On Debian-based systems, run:

```sh
apt-get install libssl-dev libffi-dev
```
# Installation
```sh
git clone https://github.com/paypal/PayPal-Python-SDK.git
cd PayPal-Python-SDK
pip install -e .
```

## Configuration
```sh
export PAYPAL_MODE=sandbox   # sandbox or live
export PAYPAL_CLIENT_ID=YOUR_CLIENT_ID_FROM_PAYPAL # https://developer.paypal.com/docs/integration/admin/manage-apps/
export PAYPAL_CLIENT_SECRET=YOUR_CLIENT_SECRET_FROM_PAYPAL # https://developer.paypal.com/docs/integration/admin/manage-apps/
```

## Run Sample
There may be additional comments in the sample file that you must complete before running.

```sh
python samples/payment/create_with_paypal.py
```