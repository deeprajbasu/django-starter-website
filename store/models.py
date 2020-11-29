from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE,related_name='customer')
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)

    # def __str__(self):
    #     return self.name

class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True,default='placeholder.png')

    def __str__(self):
        return self.name
    
    @property
    def imageUrl(self):
        
        # # try:
        # #     url = self.image.url
        # # except:
        # #     url = ''
        return self.image.url

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,
    null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id=models.CharField(max_length=200,null=True,blank=True)

    @property
    def shipping(self):
        shipping = False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping
        
    
    def __str__(self):
        return str (self.id)
    
    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total for item in items])
        return total
    
    @property
    def get_quant_total(self):
        items = self.orderitem_set.all()
        total = sum([item.quantity for item in items])
        return total


class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,
    null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,
    null=True,blank=True)


    quantity=models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        return self.product.price*self.quantity 

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,
    null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,
    null=True,blank=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    zipcode=models.CharField(max_length=200)
    
    def __str__(self):
        return self.address

# Create your models here.
