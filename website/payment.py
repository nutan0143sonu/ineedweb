import paypalrestsdk
import logging


def paypal_payment():
    logging.basicConfig(level=logging.INFO)
    

    paypalrestsdk.configure({
    "mode": "sandbox", # sandbox or live
    "client_id": "AeVCM_GtOxKkhHi0EiSYQ8zODGT0ciQmY9cWgzDxF7RfYvV7R0seiAsVFQs4gr1fbX2J6MXsHHTQbC1Q",
    "client_secret": "EKlnm8npyegPaDYJhy4wFK73xmcYSIYXYtyTKS3j2zSrjEFNMdTOgJHm_WpYFAt1bvj6-gCRqzThBjXZ" })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8080/execute",
            "cancel_url": "http://localhost:8080/cancel"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "5.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "5.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})
    print("payment",payment)
    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                # Convert to str to avoid Google App Engine Unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                approval_url = str(link.href)
                print("Redirect for approval: %s" % (approval_url))
        payment = paypalrestsdk.Payment.find("PAY-57363176S1057143SKE2HO3A")
# Get List of Payments
        payment_history = paypalrestsdk.Payment.all({"count": 10})
        payment_history.payments
        print("Payment created successfully")
    else:
        print(payment.error)
    return payment