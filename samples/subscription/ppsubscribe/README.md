ppsubscribe - Subscribe to the Hipster Magazine
===========

Flask application for a developer/merchant using Paypal's subscription apis in the python sdk. A merchant (The Hipster Magazine publisher in this app) can log in, create a new billing plan and activate the plan. A customer (subscriber to The Hipster Magazine) can look at the available plans and agree to subscribe to a plan, forming a billing agreement and view the transaction history on that agreement. Deployed on Heroku at http://ppsubscribe.herokuapp.com/

Install requirements using pip:

    pip install -r requirements.txt

## Configuration

Get your client credentials from https://developer.paypal.com/ and put them in a `paypal_config.py` file:

    $ cat paypal_config.py
    MODE = "sandbox"
    CLIENT_ID = "<client id from sandbox>"
    CLIENT_SECRET = "<client secret from sandbox>"

## Run the server

    python app.py
    // * Running on http://0.0.0.0:5000/
    // * Restarting with reloader

PEP 8
-----

All code follows the [PEP 8](http://www.python.org/dev/peps/pep-0008/) style guide, with the exception of E501, E261, and E302.
