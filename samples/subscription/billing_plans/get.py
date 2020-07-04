from paypalrestsdk import BillingPlan, ResourceNotFound
import logging
logging.basicConfig(level=logging.INFO)

try:
    billing_plan = BillingPlan.find("P-0NJ10521L3680291SOAQIVT")
    print("Got Billing Plan Details for Billing Plan[%s]" % (billing_plan.id))

except ResourceNotFound as error:
    print("Billing Plan Not Found")
