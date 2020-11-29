from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth import logout 
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.models import User

from . utils import cookieCart,cartData,guestOrder
# Create your views here.

# def tailwind(request):
#     cartitems = cartData(request)['cartitems']


#     products= Product.objects.all()
#     context={'products':products,'cartitems':cartitems}

#     return render(request,'store/tailwind.html',context)
def tailwind(request):
    return render(request,'store/tailwind.html')

def store(request):
    print(request.user)

    cartitems = cartData(request)['cartitems']


    products= Product.objects.all()
    context={'products':products,'cartitems':cartitems}
    return render(request,'store/store.html',context)

def cart(request):

    cartdata = cartData(request)
    cartitems =  cartdata['cartitems']
    order =  cartdata['order']
    items =  cartdata['items']

    context={'items':items,'order':order,'cartitems':cartitems}
    return render(request,'store/cart.html',context)
        
def checkout(request):

    cartdata = cartData(request)
    cartitems =  cartdata['cartitems']
    order =  cartdata['order']
    items =  cartdata['items']

    context={'items':items,'order':order,'cartitems':cartitems}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productID']
    action=data['action']

    print(action,productId)

    #reach database from user input
    #get_or_create updates or creates new data in one line 
    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=OrderItem.objects.get_or_create(order=order,product=product)
    #update database
    if action=='add':
        orderitem.quantity=orderitem.quantity+1
    elif action == 'remove':
        orderitem.quantity=orderitem.quantity-1
    orderitem.save()
    if orderitem.quantity <=0:
        orderitem.delete()
    return JsonResponse('item was updated',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:

        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        


    else : 
        order,customer = guestOrder(request,data)
    if order.shipping == True : 
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            state=data['shipping']['state'],
            city=data['shipping']['city'],
            zipcode=data['shipping']['zipcode'],
        )
    
    
    total = float(data['form']['total'])
    order.transaction_id=transaction_id
    
    if total == order.get_cart_total:
        order.complete= True
        
    order.save()
    print('data',request.body)
    return JsonResponse('Payment Complete!!!!',safe=False)

def showItemDetails(request):
    data = json.loads(request.body)

    # # action=data['action']
    productId=data['productID']
    product = Product.objects.get(id=productId)
    print(product.name)




    # print("aaaaaaaaaa")

    # cartdata = cartData(request)
    # cartitems =  cartdata['cartitems']
    # order =  cartdata['order']
    # items =  cartdata['items']

    
    # print("Aaaaaaaaaaaaaaaaaaaaaaaaa!!!!!!!!!!!!!!!")

    context={'product':product}
    
    # 
    page = render(request,'store/item.html',context)
    print(page)
    return page

from django.contrib.auth import authenticate
def Login (request):
    print(request.user)
    
    if request.method == "POST":
        print("!!!!!!!!!!!!!!!!!!!!")
        
        data = json.loads(request.body)
        print(data['user']['displayName'])
        print(data['user']['email'])
        print(data['user']['uid'])

        username = data['user']['displayName']
        password = data['user']['uid']
        email=data['user']['email']
        
        user = authenticate(username= username, password=password)
        print(user)
        if user is not None :
            print('user is authenticated')
            login(request,user)
            print('userlogged in')
            return redirect('store')
        if user is None :
            user = User.objects.create_user(username, email, password)
            customer , created = Customer.objects.get_or_create(user=user,email=email)
            print("createdCustomer")
            login(request,user)
            print(user)
            return JsonResponse('YY',safe=False)
    
    return render(request,'store/login.html')

# def authuser (request):
#     print(request)
#     print("YESSS")
#     return JsonResponse('gotuser',safe=False)       