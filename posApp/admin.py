from django.contrib import admin
from posApp.models import Udhaar, Products, Sales, salesItems

class SalesAdmin(admin.ModelAdmin):
    list_display=('id','name','mobile','code','sub_total','disc_amount','grand_total','payment','udhaar','date_added','date_updated')

#Register your models here.
admin.site.register(Udhaar)
admin.site.register(Products)
admin.site.register(Sales,SalesAdmin)
admin.site.register(salesItems)
#admin.site.register(Employees)
