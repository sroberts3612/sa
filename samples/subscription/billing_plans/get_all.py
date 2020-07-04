from paypalrestsdk import BillingPlan
import logging
logging.basicConfig(level=logging.INFO)

history = BillingPlan.all(
    {"status": "CREATED", "page_size": 5, "page": 1, "total_required": "yes"})
print(history)

print("List BillingPlan:")
for plan in history.plans:
    print("  -> BillingPlan[%s]" % (plan.id))
