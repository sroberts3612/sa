"""Searching webhook events. As of Nov 2014, only searching
events within last six months and for a 45 day window is
supported
"""
from paypalrestsdk import WebhookEvent
import logging
logging.basicConfig(level=logging.INFO)

parameters = {"page_size": 15,
              "start_time": "2014-11-06T11:00:00Z",
              "end_time": "2014-12-06T11:00:00Z"
              }

events = WebhookEvent.all(parameters)
print(events)
