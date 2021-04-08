from django.contrib import admin
from django.urls import path,re_path
from home import views
from shoppingcart import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('',views.index, name="home"),
    re_path(r'^home/$', views.index, name='home'),
    path('login',views.loginUser, name="login"),
    path('logout',views.logoutUser, name="logout"),
    path('register',views.registerUser, name="register"),
    path('addandshow',views.add_show, name="addandshow"),
    path('product_detail/<int:id>/', views.product_detail),
    path('add_category',views.category_creation, name="add_category"),
    path('add_to_wishlist/<int:product_id>/',views.add_to_wishlist),
    path('shop_wishlist',views.shop_wishlist, name='shop_wishlist'),
    path('remove_wishlist/<int:id>/',views.remove_wishlist, name='remove_wishlist'),
    path('shop_cart',views.shop_cart, name='shop_cart'),
    path('myaccount',views.myaccount, name='myaccount'),
    path('profile',views.profile, name='profile'),
    path('profile_creation',views.profile_creation, name='profile_creation'),
    path('add_to_cart',views.add_to_cart, name='add_to_cart'),
    # path('remove_product_from_cart/<int:id>/',views.remove_product_from_cart, name='remove_product_from_cart'),
    re_path(r'^remove_cart/$', views.remove_cart, name='remove_cart'),
    path('dynamic_add_to_cart',views.dynamic_add_to_cart, name='dynamic_add_to_cart'),
    path('address_listing',views.address_listing, name='address_listing'),
    path('address_form',views.address_form, name='address_form'),
    path('setup_address',views.setup_address, name='setup_address'),
    re_path(r'^remove_address/$', views.remove_address, name='remove_address'),
    path('order_detail/<str:order_code>/',views.order_detail, name='order_detail'),
    path('order_listing',views.order_listing, name='order_listing'),
    path('place_order',views.place_order, name='place_order'),
    path('update_status',views.update_status, name='update_status'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)