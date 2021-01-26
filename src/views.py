from django.shortcuts import render
import razorpay 
from .models import Payer
from django.views.decorators.csrf import csrf_exempt
import json

def home(request): 
    if request.method == "POST":
        name = request.POST.get("name")
        amount = int(request.POST.get("amount")) * 100
        client = razorpay.Client(auth = ("rzp_test_16E6X4U9fNZlne", "pFPT33TAYuEo4ehSh5cFbAzt"))
        payment = client.order.create(({'amount':amount, 'currency':'INR', 'payment_capture':'1'}))
        print(payment)
        payer = Payer(name = name, amount = amount, payment_id = payment['id'])
        payer.save()
        return render(request, "index.html", {'payment':payment})
    return render(request, "index.html")

@csrf_exempt
def success(request):
    print(request)
    print(request.body)
    if request.method == "POST":
        received_data = request.body
        data = json.loads(received_data)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        print(data['id'])
        order_id = data['id']
        user = Payer.objects.filter(payment_id = order_id).first()
        print(user)
        user.paid = True
        user.save()
    return render(request, "success.html")