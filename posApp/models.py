from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone

# Create your models here.

# class Employees(models.Model):
#     code = models.CharField(max_length=100,blank=True) 
#     firstname = models.TextField() 
#     middlename = models.TextField(blank=True,null= True) 
#     lastname = models.TextField() 
#     gender = models.TextField(blank=True,null= True) 
#     dob = models.DateField(blank=True,null= True) 
#     contact = models.TextField() 
#     address = models.TextField() 
#     email = models.TextField() 
#     department_id = models.ForeignKey(Department, on_delete=models.CASCADE) 
#     position_id = models.ForeignKey(Position, on_delete=models.CASCADE) 
#     date_hired = models.DateField() 
#     salary = models.FloatField(default=0) 
#     status = models.IntegerField() 
#     date_added = models.DateTimeField(default=timezone.now) 
#     date_updated = models.DateTimeField(auto_now=True) 

    # def __str__(self):
    #     return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '
class Udhaar(models.Model):
    name = models.CharField(max_length=256)
    mobile = models.IntegerField(default=0)
    transaction_code=models.IntegerField(default=0)
    total = models.IntegerField(default=0) 
    payment = models.IntegerField(default=0) 
    udhaar = models.IntegerField(default=0) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Products(models.Model):
    code = models.CharField(max_length=100)
    name = models.TextField()
    price = models.FloatField(default=0)
    scale = models.CharField(max_length=255,null=True,blank=True)
    stock=models.FloatField(default=0 ,null=True,blank=True) 
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.code + " - " + self.name

class Sales(models.Model):
    name=models.CharField(max_length=255,null=True)
    mobile=models.CharField(max_length=255,null=True)   
    code = models.CharField(max_length=100,null=True)
    sub_total = models.FloatField(default=0,null=True)
    
    disc_amount = models.FloatField(default=0,null=True)
    grand_total = models.FloatField(default=0,null=True)
    payment = models.FloatField(default=0,null=True)
    udhaar = models.FloatField(default=0,null=True)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    
    
   
    
   
  


    def __str__(self):
        return self.code

class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    scale=models.CharField(max_length=255,null=True,blank=True)
    total = models.FloatField(default=0)


class Customer(models.Model):
    name=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    address=models.TextField()