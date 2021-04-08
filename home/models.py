from django.db import models
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout, authenticate, login

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50,unique = True)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)
    
    def __str__(self):
        return self.name
    

class UnitMeasure(models.Model):
    unit = models.CharField(max_length=50)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)
    
    def __str__(self):
        return self.unit
    
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    unit_measure = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='uploads/products/',blank=True)
    is_favourite = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def favourite_count():
        return Product.objects.filter(is_favourite=True).count()
    
    # def product_wishlist_exist(self):
    #     product_wishlist = ProductWishlist.objects.filter(customer_id=request.session.get('customer_id'),product_id=self.id)
    #     if product_wishlist.count() > 0:
    #         return True
    
    def CartItemExist(self):
        cart_item = CartItem.objects.filter(product_id=self.id)
        if cart_item != None:
            return True
        else:
            return False
            
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    phone_no = models.CharField(max_length=50)
    gender = models.CharField(max_length=8)
    date_of_birth = models.CharField(null=True,max_length=15)
    
class ProductWishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    is_favourite = models.BooleanField(default=False)
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    order_id = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)
    
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    address_details = models.CharField(max_length=250)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    landmark = models.CharField(max_length=50)
    resident_type = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    
class Order(models.Model):
    order_code = models.CharField(max_length=15)
    # cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True)
    payment_type = models.CharField(max_length=20,null=True)
    total_price = models.IntegerField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_delivered_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=10)
    
    def getOrderProduct(self):
        cart_item = CartItem.objects.filter(order_id=self.id)
        if cart_item != None:
            return cart_item.first().product
        else:
            return ""
        
    def getProductCount(self):
        cart_item = CartItem.objects.filter(order_id=self.id)
        if cart_item != None:
            return cart_item.count()
        else:
            return ""
        
    def getOrderTrackData(self):
        order_track = OrderTrack.objects.get(order_id=self.id,status=self.status)
        if order_track != None:
            return order_track
        else:
            return ""
        
class OrderTrack(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=10)
    reason = models.CharField(max_length=150)
    track_period = models.DateTimeField(null=True)