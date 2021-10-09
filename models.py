from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE,unique=True)
    # username=models.CharField(max_length=200,null=True,blank=True,unique=True)
    first_name=models.CharField(max_length=20,null=True,blank=True)
    second_name=models.CharField(max_length=20,null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    image=models.ImageField(upload_to='picture/',null=True,blank=True)
    id_no=models.CharField(max_length=200,null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        ordering=['-date_joined']


class Package(models.Model):
    Category=(
        ('basic','basic'),
        ('pro','pro'),
        ('premium','premium'),
        ('feedback','feedback')
    )
    name=models.CharField(max_length=200,null=True,blank=True)
    price=models.FloatField(default=0)
    image=models.ImageField(blank=True,null=True)
    slug=models.SlugField(blank=True,null=True)
    category=models.CharField(max_length=100,blank=True,null=True,choices=Category)
    quantity=models.IntegerField(default=1)
    description=models.TextField()
    date_added=models.DateField(auto_now_add=True,null=True, blank=True)
    date_ordered=models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.name
    
    def product_price(self):
        return self.price
    
    class Meta:
        ordering=['-date_added']
    


class Cart(models.Model):
    customer=models.OneToOneField(Customer,null=True, blank=True, on_delete=models.CASCADE)
    package=models.ManyToManyField(Package,blank=True,)
    date_ordered=models.DateTimeField(null=True)


    def __str__(self):
        return str(self.customer)

    def total_sum(self):
        price_list=[]
        for product in self.package.all():
            price_list.append(product.price)
        return sum(price_list)



class Invoice(models.Model):

    customer=models.ForeignKey(Customer,null=True, blank=True, on_delete=models.SET_NULL)
    cart=models.ForeignKey(Cart,null=True, blank=True, on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    order_id=models.CharField(max_length=200,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    btc_value=models.FloatField(blank=True,null=True)
    satoshi_value=models.IntegerField(blank=True,null=True)
    usd_value=models.IntegerField(blank=True,null=True)
    received=models.IntegerField(blank=True,null=True)
    txid=models.CharField(max_length=300,null=True,blank=True)
    rbf=models.IntegerField(blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.cart}|{self.id}'
   

class UserPackage(models.Model):
    customer=models.ForeignKey(Customer,null=True, blank=True, on_delete=models.CASCADE)
    package=models.ManyToManyField(Package,blank=True,)

    def __str__(self):
        return f'{self.customer}-{self.id}'
