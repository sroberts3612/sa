from paypalrestsdk import Invoice
import logging
import json
logging.basicConfig(level=logging.INFO)


my_invoices = []
page_size = 2

for i in range(3):
    
    options = {
        "start_invoice_date": "2016-01-01 PST",
        "end_invoice_date": "2030-03-26 PST",
        "status": ["SENT", "DRAFT", "PAID", "CANCELLED"],
        "total_count_required": True,
        "page": i * page_size,
        "page_size": page_size
    }
    
    invoices = Invoice.search(options)

    if invoices.success():  # return True or False
        for inv in invoices.invoices:
            my_invoices.append(inv.id)
    else:
        print(invoices.error)

   
print(json.dumps(my_invoices, sort_keys=False, indent=4))
