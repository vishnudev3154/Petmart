from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [

    # Django Admin
    path('admin/', admin.site.urls),

    # Admin Pages
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('manageproduct/', views.manageproduct, name='manageproduct'),
    path('adminpage/orders/', views.admin_orders, name='adminorders'),
    path('users/', views.view_users, name='viewusers'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),


    # Product
    path('addproduct/', views.addproduct, name='addproduct'),
    path('update/<int:pk>/', views.viewproductupdate, name='updateproduct'),
    path('delete/<int:pk>/', views.viewproductdelet, name='deleteproduct'),

    # Auth
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),

    # User Page
    path('userpage/', views.userpage, name='userpage'),

    path('logout/', views.logout_view, name='logout'),

    # Cart
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='addtocart'),
    path('cart/', views.view_cart, name='viewcart'),
    path('remove-cart/<int:pk>/', views.remove_from_cart, name='removecart'),

    # ✅ Buy Now (ONLY THIS)
    path('buy-all/', views.buy_all_payment, name='buyall'),



    # Wishlist
    path('add-to-wishlist/<int:pk>/', views.add_to_wishlist, name='addtowishlist'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('remove-wishlist/<int:pk>/', views.remove_from_wishlist, name='removewishlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
