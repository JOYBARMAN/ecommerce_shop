from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from math import ceil
from django.contrib import  messages
import json


def index(request):
    # products=Product_Table.objects.all()
    # print(products)
    # n=len(products)
    # nSlides=n//4+ceil((n/4)-(n//4))
    # allProds = [[products, range(1, nSlides), nSlides], [products, range(1,nSlides), nSlides],[products, range(1,nSlides), nSlides]]
    allProds = []
    catprods = Product_Table.objects.values('product_category', 'id')
    cats = {item["product_category"] for item in catprods}
    for cat in cats:
        prod = Product_Table.objects.filter(product_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    # param={'no_of_slide':nslide,'range':range(1,nslide),'product':products}
    return render(request,'shop2/index.html',params)

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        # if len(name)>5:
        #     print("valid User")
        # else:
        #     print("Invalid")
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        # sucess=True
        messages.success(request,"Your Feedback have been send sucessfully. we will review soon")
    return render(request,'shop2/contact.html')

def about(request):
    return render(request,'shop2/about.html')

def search(request):
    return HttpResponse("<h1>we are at search</h1>")

def productview(request,myid):
    # Fetch the product using the id

    product=Product_Table.objects.filter(id=myid)

    return render(request,'shop2/productview.html',{'product':product[0]})

def checkpoint(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                       zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop2/checkout.html', {'thank': thank, 'id': id})
    return render(request,"shop2/checkout.html")


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop2/tracker.html')


