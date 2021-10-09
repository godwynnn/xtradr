from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.utils.text import slugify
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import authorised_user
from django.urls import reverse
from django.utils import timezone
import requests
from django.conf import settings
from .decorators import *
from django.core.mail import send_mail
from django.contrib.auth.views import redirect_to_login


from rest_framework import response
import json
import random
import uuid
import os


x=random.randint(10000,90000)

# Create your views here.
def IndexPage(request):
   
    dollar_amount=10000
    if dollar_amount >=10000:
        dollar_amount=+x
    btc_amount=dollar_amount/240000
    try:
        product=Package.objects.all()
        cart=Cart.objects.get(customer=request.user.customer)
        for product in cart.package.all():
            cart.package.remove(product)
        print("all items removed from cart.")
    except Exception as e:
        print(e)
    
    
    template='forex/index.html'
    context={
            'dollar_amount':dollar_amount,
            'btc_amount':btc_amount }

    return render(request,template,context)



def Basic_Page(request):
    packages=Package.objects.filter(category__iexact='basic')

    cart=''
    if request.user.is_authenticated:
        cart=Cart.objects.get(customer=request.user.customer)
        
        # for package in packages:
            
        #     if package not in cart.package.all():
        #         purchase=False

        #     elif cart.package.filter(id=package.id).exists():
        #         purchase=True

    template='forex/packages/basic.html'
    context={'packages':packages,
        'cart': cart
    #  'purchase':purchase, 
     }

    return render(request,template,context)

    
    
def Pro_Page(request):
    packages=Package.objects.filter(category__iexact='pro')

    cart=''
    if request.user.is_authenticated:
        cart=Cart.objects.get(customer=request.user.customer)


    template='forex/packages/pro.html'
    context={'packages':packages,'cart': cart}

    return render(request,template,context)

def Premium_Page(request):
    packages=Package.objects.filter(category__iexact='premium')


    cart=''
    if request.user.is_authenticated:
        cart=Cart.objects.get(customer=request.user.customer)
    

    template='forex/packages/premium.html'
    context={'packages':packages,'cart': cart }

    return render(request,template,context)


@authorised_user(roles=['admin','customer'])
def CreatePackagePage(request):

    form=PackageForm(request.POST or None,request.FILES)
    if request.method=='POST':
        if form.is_valid():
            q=form.save(commit=False)
            q.slug=slugify(q.name+'-'+q.description[:10])
            q.save()

        form=PackageForm()
    
    context={'form': form}
    template='forex/create.html'
    return render(request,template,context)




@authorised_user(roles=['admin'])
def UpdatePackagePage(request,slug):

    package=Package.objects.get(slug=slug)
    form=PackageForm(request.POST or None,request.FILES,instance=package)
    if request.method=='POST':
        if form.is_valid():
            q=form.save(commit=False)
            q.slug=slugify(q.name,+'-'+q.description[:10])
            q.save()

            
            form=PackageForm()
    
    context={'form': form}
    template='forex/update.html'
    return render(request,template,context)


    
@authorised_user(roles=['admin'])
def DetailPage(request,slug):
    
    
    package=Package.objects.get(slug=slug)
    purchase=False
    if request.user.is_authenticated:
        cart=Cart.objects.get(customer=request.user.customer)
        

        if package in cart.package.all():
            purchase=True
        
            
    template='forex/detail.html'
      
    context={'package':package,
    'purchase': purchase
    }
    return render(request,template,context)


@authorised_user(roles=['admin'])
def DeletePage(request,slug):
    package=Package.objects.get(slug=slug)
    package.delete()
    return render(request)


def SignupPage(request):
    form=RegistrationForm(request.POST or None,initial={'username':'' , 'password_1':'' })
    if request.method=='POST':
        if form.is_valid():
            user=form.save()
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            # password=form.cleaned_data['password1']
            # confirm_password=form.cleaned_data['password2']
            # username=email.split('@')[0]

            # for n in range(10):
            number=random.randint(0000,900000)
            # number=round(random()*1234567890)
            id_no='fx'+'-'+ str(number)

            customer=Customer.objects.create(
                user=user,
                first_name=first_name,
                second_name=last_name,
                email=email,
                id_no=id_no
                # password=password,
                # confirm_password=confirm_password,
                # username=username
            )
            Cart.objects.create(customer=customer)
            
          
            form=RegistrationForm()
            return redirect('login')
    template='forex/signup.html'
    context={'form':form}
    return render(request,template,context)


def LoginPage(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('landing')
        else:
            messages.info(request,"incorrect Username OR Password")
        
    template='forex/login.html'
    return render(request,template)


def Logout(request):
    logout(request)
    return redirect ('landing')



@login_required(login_url='login')
def Dashboard(request):
    carts=Cart.objects.get(customer=request.user.customer)
    packages=Package.objects.all()
    products=UserPackage.objects.get(customer=request.user.customer)
    user_inv=Invoice.objects.filter(customer=request.user.customer)
    template='forex/customer.html'
    context={'products':products,'user_inv':user_inv} 
    return render(request,template,context)

@authorised_user(roles=['admin'])
def Admin_Panel(request):
    customers=Customer.objects.all()
    context={'customers': customers}
    return render(request, 'forex/admin.html',context)



@login_required(login_url='login')
def Add_to_cart(request,slug):
    product=Package.objects.get(slug=slug)
    
    purchase=False


    if product.category=='basic':
        if request.method=='POST':
            cart=Cart.objects.get(customer=request.user.customer)
            

            if  product in cart.package.all():
                purchase=True

            else:
                # ordered_date=timezone.now()
                # Cart.objects.create(date_ordered=ordered_date)
                cart.package.add(product)
                purchase=True
                

                return HttpResponseRedirect(reverse('basic_package',args=[str(product.slug)]))
               
     

    if product.category=='pro':
        if request.method=='POST':
            cart=Cart.objects.get(customer=request.user.customer)
            

            if  product in cart.package.all():
                messages.info(request,'you carted this goods')

            else:
                # ordered_date=timezone.now()
                # Cart.objects.create(date_ordered=ordered_date)
                cart.package.add(product)
                purchase=True
                

                return HttpResponseRedirect(reverse('pro_package'))


    if product.category=='premium':
        if request.method=='POST':
            cart=Cart.objects.get(customer=request.user.customer)
            

            if  product in cart.package.all():
                messages.info(request,'you carted this goods')

            else:
                # ordered_date=timezone.now()
                # Cart.objects.create(date_ordered=ordered_date)
                cart.package.add(product)
                purchase=True
                

                return HttpResponseRedirect(reverse('premium_package'))


def Remove_from_cart(request,slug):
    product=Package.objects.get(slug=slug)
   
    if request.method=='GET':
        cart=Cart.objects.get(customer=request.user.customer)
        purchase=True

        if  product in cart.package.all():
            cart.package.remove(product)
            
            

            purchase=False
            

        return HttpResponseRedirect(reverse('cart'))
        # return redirect('detail_package')



def CartFlow(request):
    if request.user.is_authenticated:

        cart=Cart.objects.get(customer=request.user.customer)
        carts=cart.package.all()
        # cart_time=Cart.objects.get(customer=request.user.customer)
        # # print('Package: '+ cart.package)
        cart_total=cart.total_sum()
    else:
        carts= ''
        cart_total=''
    context={'carts': carts,'cart_total':cart_total}
    template='forex/cart.html'
  
    return render(request,template,context)

def exchange_rate(amount):


    url = 'https://www.blockonomics.co/api/price?currency=USD'

    r=requests.get(url)
    response=r.json()
    return amount/response['price']



def CheckoutSession(request):

    cart=Cart.objects.get(customer=request.user.customer)
    
    btc=exchange_rate(cart.total_sum())
    order_id=uuid.uuid1()
    invoice=Invoice.objects.create(
        status=True,
        customer=request.user.customer,
        order_id=order_id,
        btc_value=btc,
        satoshi_value=btc*1e8,
        cart=cart,
        usd_value=cart.total_sum(),
        )
    UserPackage.objects.create(customer=request.user.customer)
    return HttpResponseRedirect(reverse('instant_invoice', kwargs={'pk':invoice.id}))

def Instant_invoice(request,pk):
    bill=False
    invoice=request.user.customer.invoice_set.get(id=pk)
    carts=invoice.cart.package.all()
    if invoice.status==True:
        bill=True
    data={
        'order_id':invoice.order_id,
        'btc': invoice.satoshi_value/1e8,
        'value': invoice.cart.total_sum(),
        'addr': 'VqiB4vHvXQNhpcC84kg3kGKAHxHdnqkznhLF5s8SIOw',
        'invoice_status': invoice.status,
        'bill':bill,
        'carts':carts,

    }
    

    return render(request, 'forex/cart.html',data)


def Payment_complete(request):
    if (request.method != 'GET'):
        return 
    
    txid  = request.GET.get('txid')
    value = request.GET.get('value')
    status = request.GET.get('status')
    addr = request.GET.get('addr')

    invoice = Invoice.objects.get(address = addr)
    
    invoice.status = int(status)
    if (int(status) == 2):
        invoice.received = value
    invoice.txid = txid
    invoice.save()
    return HttpResponse(200)

    return(render,'forex/success.html')




def User_Invoice(request):


    invoices=request.user.customer.invoice_set.all()

    context={'invoices':invoices}
    template='forex/invoice.html'
    return render(request,template,context)

def Send_email(request):
    if request.method=='POST':

        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']

        send_mail(
            'Message From'+ name,
            message,
            email,
            ['miraclegodwin67@gmail.com']
        )

    context={'message':message,'name':name }
    return render(request,'forex/index.html',context)


def CustomerProfile(request):
    customer=Customer.objects.get(user=request.user)
    form=CustomerProfileForm(request.POST or None,request.FILES, instance=customer)
    if request.method=='POST':
        if form.is_valid:
            form.save()
        return redirect('profile')
    context={'form':form,'customer':customer}
    template='forex/profile.html'
    return render(request,template,context)

def Delete_user(request,pk):
    customer=Customer.objects.get(id=pk)
    customer.delete()
    return render(request)

def UserPackage_Page(request,pk):
    customer=Customer.objects.get(id=pk)
    package=customer.userpackage
    form=UserPackageForm(request.POST or None, instance=package)
    if request.method=='POST':
        if form.is_valid():
            form.save()

            return redirect('admin')
    context={'form': form}
    return render(request,'forex/package_create.html',context)

