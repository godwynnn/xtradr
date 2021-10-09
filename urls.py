from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns=[
    path('', IndexPage,  name='landing'),
    path('create', CreatePackagePage, name='create_package'),
    path('basic', Basic_Page, name='basic_package'),
    path('pro', Pro_Page, name='pro_package'),
    path('premium', Premium_Page, name='premium_package'),
    path('update/<slug:slug>/', UpdatePackagePage, name='update_package'),
    path('detail/<slug:slug>/', DetailPage, name='detail_package'),
    path('delete/<slug:slug>/', DeletePage, name='delete_package'),
    path('backoffice/', Dashboard, name='dashboard'),
    path('profile/', CustomerProfile, name='profile'),
    path('admin-dashboard/', Admin_Panel, name='admin'),
    path('delete/<str:pk>/', Delete_user, name='delete_user'),
    path('userpackage/<str:pk>/', UserPackage_Page, name='user_package'),
    path('signup/', SignupPage, name='signup'),
    path('login/', LoginPage, name='login'),
    path('logout/', Logout, name='logout'),
    path('checkout/<slug:slug>/', Add_to_cart, name='Add_to_cart'),
    path('remove/<slug:slug>/',Remove_from_cart , name='remove_from_cart'),
    path('cart/', CartFlow, name='cart'),
    path('checkout/', CheckoutSession, name='checkout'),
    path('invoice/<str:pk>', Instant_invoice, name='instant_invoice'),
    path('success/', Payment_complete, name='success'),


]
