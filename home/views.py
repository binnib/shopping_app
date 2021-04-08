from django.shortcuts import render, redirect,get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout, authenticate, login
from .models import Category, UnitMeasure,Product,Customer,ProductWishlist,CartItem,Address,Order,OrderTrack
from .forms import ProductForm,CategoryForm
from django.http import JsonResponse
from django.db.models import Sum
from django.utils.crypto import get_random_string
import datetime

# password for test user is demo12345
# Create your views here.
def index(request):
    # print(request.user)  
    # print(User.objects.last().is_staff)
    category_name = request.GET.get('category')
    category = Category.objects.filter(name=category_name).last()
    
    if category_name == None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category_id=category.id)
    # print(products.exists())    
    categories = Category.objects.all()
    
    context = { 
        "products" : products,
        "categories" : categories,
    }
    
    if request.user.is_anonymous:
        return redirect("/login") 
    return render(request, 'index.html',context)

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            request.session['user_id'] = user.id
            customer = Customer.objects.filter(user_id=user.id).last()
            print("===========Customer ID=======",customer.id)
            request.session['customer_id'] = customer.id
            return redirect("/")
        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")

def registerUser(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                print("Username taken")
                # messages.info(request,"Username taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                print("Email taken")
                 # messages.info(request,"Email taken")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name,email=email)
                user.save()
                customer = Customer(user_id=user.id)
                customer.save()
                print("customer created")
                print('user created')
        else:
            print("password not matching..")
            # messages.info(request,'password not matching..')
            return redirect("register")
        return redirect("/login")
    else:
        return render(request, 'register.html')
    
    
def add_show(request):
    if request.method == 'POST':
        fm = ProductForm(request.POST,request.FILES)
        print(request.FILES)
        print(fm.is_valid())
        if fm.is_valid():
            fm.save()
            return redirect("/")
    else:
        fm = ProductForm()
    context = {"form": fm,}
    return render(request, 'addandshow.html', context)


def product_detail(request,id):
    product = Product.objects.get(id=id)
    # product_wishlist = ProductWishlist.objects.get(product_id=product.id)
    try:
        product_wishlist = ProductWishlist.objects.filter(product_id=product.id).last()
    except ObjectDoesNotExist:
        product_wishlist = None
                
    context = { 
        "product" : product,
        "product_wishlist" : product_wishlist,
    }
    return render(request, 'product_detail.html',context)

def category_creation(request):
    if request.method == 'POST':
        fm = CategoryForm(request.POST,request.FILES)
        print(request.FILES)
        print(fm.is_valid())
        if fm.is_valid():
            fm.save()
            return redirect("/")
    else:
        fm = CategoryForm()
    context = {"form": fm,}
    return render(request, 'add_category.html', context)

def add_to_wishlist(request,product_id):
    if request.method == 'GET':
        result = ''
        product_wishlist = ProductWishlist.objects.filter(product_id=product_id).last()
        if product_wishlist == None:
            wishlist = ProductWishlist(customer_id=request.session.get('customer_id'),product_id=product_id,is_favourite=True)
            wishlist.save()
            result = "Favourite"
        else:
            product_wishlist.delete()
        return JsonResponse({'result': result })
    
def remove_wishlist(request,id):
    if request.method == 'GET':
        product_wishlist = ProductWishlist.objects.filter(id=id).last()
        # product_wishlist.is_favourite = False
        # product_wishlist.save()
        product_wishlist.delete()
        
        return redirect("/shop_wishlist")
    
def shop_wishlist(request):
    print("Request Customer ID==========",request.session.get('customer_id'))
    customer = Customer.objects.filter(id=request.session.get('customer_id')).last()
    wishlist_products = ProductWishlist.objects.filter(customer_id=customer.id,is_favourite=True)
        
    context = { 
        "wishlist_products" : wishlist_products,
    }
    
    return render(request, 'shop_wishlist.html',context)
    
def shop_cart(request):
    cart_products = CartItem.objects.filter(customer_id=request.session.get('customer_id'),ordered=False)
    
    calculated_price = cart_products.aggregate(Sum('total_price'))
    
    customer = Customer.objects.filter(user_id=request.session.get('user_id')).last()    
    address = Address.objects.filter(customer_id=request.session.get('customer_id'),is_active=True).last()
    
    context = { 
        "cart_products" : cart_products,
        "cart_products_count" : cart_products.count(),
        "calculated_price" : calculated_price["total_price__sum"],
        "customer" : customer,
        "address" : address,
    }
    return render(request, 'shop_cart.html',context)

def myaccount(request):
    return render(request, 'myaccount.html')

def profile_creation(request):
    print(request.method)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        phone_no = request.POST.get('phone_no')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
                
        customer = Customer(user_id=user_id,phone_no=phone_no,date_of_birth=date_of_birth,gender=gender)
        # customer = Customer(user_id=user_id,phone_no=phone_no,gender=gender)
                
        registered_customer = Customer.objects.filter(user_id=request.session.get('user_id')).last()
        
        if registered_customer == None:
            customer.save()
        else:
            registered_customer.phone_no = phone_no
            registered_customer.date_of_birth = date_of_birth
            registered_customer.gender = gender
            registered_customer.save()
        
        return redirect("/profile")
    else:
        return redirect("/profile")
    
def profile(request):
    registered_customer = Customer.objects.filter(user_id=request.session.get('user_id')).last()    
    context = { 
        "customer" : registered_customer,
    }
    return render(request, 'profile.html',context)

def add_to_cart(request):
    print(request.session.get('customer_id'))
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        product = Product.objects.filter(id=product_id).last()
        
        total_calculated_price = product.price
               
        cart_item = CartItem(customer_id=request.session.get('customer_id'),product_id=product_id,total_price=total_calculated_price)
        cart_item.save()
        
        return redirect("/")
    
def remove_cart(request):
    cart_item_id = request.GET.get('cart_item_id')
    cart_type = request.GET.get('cart_type')
    print(request)
    if cart_type == "single":
        print("Single")
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
    else:
        print("All")
        cart_items = CartItem.objects.filter(customer_id=request.session.get('customer_id'))
        cart_items.delete()
            
    return redirect("/shop_cart")

def dynamic_add_to_cart(request):
    print(request.method)
    if request.method == 'POST':
        calculated_price = ''
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')
        
        cart_item = CartItem.objects.filter(id=cart_item_id).last()
        
        if cart_item != None:
            cart_item.quantity = quantity
            
            total_price_for_item = int(quantity) * cart_item.product.price
            cart_item.total_price = total_price_for_item
            cart_item.save()
            
            calculated_price = CartItem.objects.filter(customer_id=request.session.get('customer_id'),ordered=False).aggregate(Sum('total_price'))
            
    return JsonResponse({'calculated_price': calculated_price["total_price__sum"]})


def address_listing(request):
    customer = Customer.objects.filter(user_id=request.session.get('user_id')).last()    
    address = Address.objects.filter(customer_id=request.session.get('customer_id'),is_active=True).last()
    context = { 
        "customer" : customer,
        "address" : address,
    }
    return render(request, 'my_addresses.html',context)

def address_form(request):
    customer = Customer.objects.filter(user_id=request.session.get('user_id')).last()    
    address = Address.objects.filter(customer_id=request.session.get('customer_id'),is_active=True).last()
    context = { 
        "customer" : customer,
        "address" : address,
    }
    return render(request, 'address_form.html',context)

def setup_address(request):
    print(request.method)
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        address_details = request.POST.get('address_details')
        state = request.POST.get('state')
        city = request.POST.get('city')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        landmark = request.POST.get('landmark')
        resident_type = request.POST.get('resident_type')
                
        address = Address(customer_id=customer_id,address_details=address_details,state=state,city=city,country=country,pincode=pincode,landmark=landmark,resident_type=resident_type)
                
        registered_address = Address.objects.filter(customer_id=request.session.get('customer_id'),is_active=True).last()
        
        if registered_address == None:
            address.save()
        else:
            registered_address.address_details = address_details
            registered_address.state = state
            registered_address.city = city
            registered_address.country = country
            registered_address.pincode = pincode
            registered_address.landmark = landmark
            registered_address.resident_type = resident_type
            registered_address.save()
        
        return redirect("/address_listing")
    else:
        return redirect("/address_form")
    
def remove_address(request,id):
    if request.method == 'GET':
        address = Address.objects.filter(id=id).last()
        address.is_active = False
        address.save()
                
        return redirect("/address_listing")

def order_listing(request):
    orders = Order.objects.filter(customer_id=request.session.get('customer_id')).order_by('-id')
    context = { 
        "orders" : orders,
    }
    return render(request, 'order_listing.html',context)

def order_detail(request,order_code):
    order = Order.objects.get(order_code=order_code)
    cart_items = CartItem.objects.filter(order_id=order.id)
    
    customer = Customer.objects.filter(user_id=request.session.get('user_id')).last()    
    address = Address.objects.filter(customer_id=request.session.get('customer_id'),is_active=True).last()
    context = { 
        "order" : order,
        "cart_items" : cart_items,
        "customer" : customer,
        "address" : address,
    }
    return render(request, 'order_detail.html',context)

def place_order(request):
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        customer_id = request.session.get('customer_id')
        
        calculated_price = CartItem.objects.filter(customer_id=request.session.get('customer_id'),ordered=False).aggregate(Sum('total_price'))
        total_price = calculated_price["total_price__sum"]
        
        order_code = get_random_string(15)
        
        address = Address.objects.filter(customer_id=request.session.get('customer_id'),is_active=True).last()
                       
        order = Order(order_code=order_code,payment_type=payment_type,total_price=total_price,address_id=address.id,customer_id=request.session.get('customer_id'),status="CONFIRMED")

        order.save()
        
        if order.save() == None:
            cart_items = CartItem.objects.filter(customer_id=request.session.get('customer_id'),ordered=False).update(ordered=True,order_id=order.id)
            OrderTrack.objects.create(order_id=order.id,customer_id=request.session.get('customer_id'),status=order.status,track_period=datetime.datetime.now())
            
            return redirect("/shop_cart")
        
def update_status(request):
    if request.method == 'POST':
        order_code = request.POST.get('order_code')
        status = request.POST.get('status')
        order_delivered_date = None
        
        if status == "DELIVERED":
            order_delivered_date = datetime.datetime.now()

        order = Order.objects.get(order_code=order_code)
        order.status = status
        order.order_delivered_date = order_delivered_date
        order.save()
        
        order_track = OrderTrack.objects.filter(customer_id=request.session.get('customer_id'),order_id=order.id,status=order.status)
        
        if order_track.exists() == False:
            OrderTrack.objects.create(order_id=order.id,customer_id=request.session.get('customer_id'),status=order.status,track_period=datetime.datetime.now())
        
        return HttpResponseRedirect('/order_detail/'+order_code+'/')