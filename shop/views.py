from django.shortcuts import render
from .models import Product ,Contact,Orders,OrderUpdate
from django.http import HttpResponse
from math import ceil
import json

def index(request):
    prod = Product.objects.all()

    # n = len(prod)
    # nSlides = n // 4 + ceil((n / 4) - (n // 4))
    # allProds = [[prod, range(1, nSlides), nSlides],
    #              [prod, range(1, nSlides), nSlides]]
    # params = {'allProds': allProds}
    allProds = []
    catprods = Product.objects.values('category', 'id')
    print(catprods)
    cats = {item["category"] for item in catprods}
    # cats have different categories
    print(cats)
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        print(prod)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if (n!=0):
            allProds.append([prod, range(1, nSlides), nSlides])



    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)

def search(request):
    query = request.GET.get('search', 'off')
    prod = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    print(catprods)
    cats = {item["category"] for item in catprods}
    # cats have different categories
    for cat in cats:
        prod1=[]
        prod = Product.objects.filter(category=cat)
        for item in prod:
            if (match(query, item)):
                prod1.append(item)
        n = len(prod1)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if (n != 0):
            allProds.append([prod1, range(1, nSlides), nSlides])


    params = {'allProds': allProds}
    return render(request, "shop/search.html", params)
def match(query,item):
    #it will return true if query  is (ouser) and item_name is (trouser)
    if query.lower() in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    return False

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method=="POST":
        print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        print(name,email,phone, desc )
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "shop/contact.html")

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
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json},
                                          default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def productView(request,myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop/prodview.html", {'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                       zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')
