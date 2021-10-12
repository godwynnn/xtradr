from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin


# class UserAdminConfig(UserAdmin):
#     ordering=('-start_date')
#     list_display=('price','description',
#     'date_added')

admin.site.register(Customer)
admin.site.register(Package)
admin.site.register(Invoice)
admin.site.register(Cart)
admin.site.register(UserPackage)