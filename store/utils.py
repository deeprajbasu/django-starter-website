import json
from . models import *
def cartData(request):
    #print(request.user.is_authenticated)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartitems=order.get_quant_total
        
    else : 
        cookieCartData = cookieCart(request)
        cartitems =  cookieCartData['cartitems']
        order =  cookieCartData['order']
        items =  cookieCartData['items']

    return {'items':items,'order':order,'cartitems':cartitems}

def guestOrder(request,data): 
    #print('user is not logged in')
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    cartitems =  cookieData['cartitems']
    order =  cookieData['order']
    items =  cookieData['items']

    customer , created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer,complete=False)
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderitem=OrderItem.objects.create(order=order,product=product,quantity=item['quantity'])

    return order,customer
    
def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_quant_total':0,'get_cart_total':0,'shipping':False}
    cartitems=order['get_cart_total']

    for i in cart:
        try:

            cartitems+=cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.price *cart[i]['quantity']
            order['get_cart_total']+=total
            order['get_quant_total']+=cart[i]['quantity']
            
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageUrl':product.imageUrl,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,


            }
            items.append(item)
            if product.digital==False:
                order['shipping']=True
        except:
            pass
    return {'items':items,'order':order,'cartitems':cartitems}