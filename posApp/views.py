from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
from flask import jsonify
from posApp.models import Udhaar, Products, Sales, salesItems,Customer
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json, sys
from datetime import date, datetime
from django.db.models import Q
import math as m

# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    condition = Q(udhaar=0)
    not_condition=  ~condition


    udhaar_list = Sales.objects.filter(not_condition).count()
    products = Products.objects.all()
    list=[]
    for prod in products:
        if prod.stock==0 or prod.stock<0:
            list.append("missing")
    
    missing=len(list)
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    total_sales = m.ceil(sum(today_sales.values_list('grand_total',flat=True)))
    context = {
        'page_title':'Home',
        'udhaarlist' : udhaar_list,
        'products' : missing,
        'transaction' : transaction,
        'total_sales' : total_sales,
    }
    return render(request, 'posApp/home.html',context)


def about(request):
    context = {
        'page_title':'About',
    }
    return render(request, 'posApp/about.html',context)

#Categories
@login_required
def category(request):
    condition = Q(udhaar=0)
    not_condition=  ~condition
    udhaar_list = Sales.objects.filter(not_condition).all()
    # category_list = {}
    context = {
        'page_title':'Udhaar List',
        'udhaar':udhaar_list,
    }
    return render(request, 'posApp/category.html',context)
@login_required
def manage_category(request):
    udhaar = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            udhaar = Sales.objects.filter(id=id).first()
    
    context = {
        'udhaar' : udhaar
    }
    return render(request, 'posApp/manage_category.html',context)

@login_required
def save_category(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_category = Sales.objects.filter(id = data['id']).update(name=data['name'], mobile=data['mobile'],code=data['code'],sub_total=data['sub_total'],disc_amount=data['disc_amount'],grand_total=data['grand_total'],payment=data['payment'],udhaar=data['udhaar'])
        else:
            save_category = Sales(name=data['name'], mobile=data['mobile'],code=data['code'],sub_total=data['sub_total'],disc_amount=data['disc_amount'],grand_total=data['grand_total'],payment=data['payment'],udhaar=data['udhaar'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Sale Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
# def delete_category(request):
#     data =  request.POST
#     resp = {'status':''}
#     try:
#         Udhaar.objects.filter(id = data['id']).delete()
#         resp['status'] = 'success'
#         messages.success(request, 'Category Successfully deleted.')
#     except:
#         resp['status'] = 'failed'
#     return HttpResponse(json.dumps(resp), content_type="application/json")

# Products
@login_required
def products(request):
    product_list = Products.objects.all()
    context = {
        'page_title':'Product List',
        'products':product_list,
    }
    return render(request, 'posApp/products.html',context)
@login_required
def manage_products(request):
    product = {}
    #categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()
    
    context = {
        'product' : product,
    }
    return render(request, 'posApp/manage_product.html',context)
def test(request):
    categories = Udhaar.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'posApp/test.html',context)
@login_required
def save_product(request):
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_product = Products.objects.filter(id = data['id']).update(code=data['code'], name=data['name'], stock = data['stock'], price = float(data['price']),scale=data['scale'],status = data['status'])
            else:
                save_product = Products(code=data['code'], name=data['name'], stock = data['stock'], price = float(data['price']),scale=data['scale'],status = data['status'])
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_product(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Products.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
@login_required
def pos(request):
    # Reverse Condition
    condition = Q(stock=0)
    condition1 = Q(stock__lt=0)
    not_condition=  ~condition
    not_condition1=  ~condition1
    combined_condition = not_condition & not_condition1
    products = Products.objects.filter(combined_condition)
    product_json = []
    for product in products:
        product_json.append({'id':product.id, 'name':product.name, 'price':float(product.price),'scale':product.scale,'stock':product.stock})
    context = {
        'page_title' : "Point of Sale",
        'products' : products,
        'product_json' : json.dumps(product_json)
    }
    # return HttpResponse('')
    return render(request, 'posApp/pos.html',context)

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total =float(request.GET['grand_total'])
        grand_total=m.floor(grand_total)
       
    context = {
        'payable_amount' : grand_total,
    }
    return render(request, 'posApp/checkout.html',context)

@login_required
def save_pos(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    pref = datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        sales = Sales(
        name=data['customer_name'],
        mobile=data['customer_mobile'],
        code=code,
        sub_total=data['sub_total'],
        disc_amount=data['disc_amount'],
        grand_total=data['grand_total'],
        payment=data['payment'],
        udhaar=data['udhaar'])
        sales.save()
       
        sale_id = Sales.objects.last().pk
        # if data['udhaar'] != 0:
        #     udhaar = Udhaar(
        #         name=data['customer_name'],
        #         mobile=data['customer_mobile'],
        #         transaction_code=code,
        #         total=data['grand_total'],
        #         payment=data['payment'],
        #         udhaar=data['udhaar']
        #     )
        #     udhaar.save()
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod 
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            product_stock=product.stock
            qty = data.getlist('qty[]')[i] 
            price = data.getlist('price[]')[i] 
            scale = data.getlist('product_scale[]')[i] 
            total = float(qty) * float(price)
            remaining_stock=float(product_stock)-float(qty)
            updated_product=Products.objects.filter(id=product_id).update(stock=remaining_stock)
            print({'sale_id' : sale, 'product_id' : product, 'qty' : qty, 'price' : price, 'total' : total,'scale':scale})
            salesItems(sale_id = sale, product_id = product, qty = qty, price = price,scale=scale, total = total).save()
            i += int(1)

           
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occuredd"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def salesList(request):
    sales = Sales.objects.all()
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale,field.name)
        data['items'] = salesItems.objects.filter(sale_id = sale).all()
        data['item_count'] = len(data['items'])
        if 'disc_amount' in data:
            data['tax_amount'] = format(float(data['disc_amount']),'.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)
    context = {
        'page_title':'Sales Transactions',
        'sale_data':sale_data,
    }
    # return HttpResponse('')
    return render(request, 'posApp/sales.html',context)

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id = sales).all()
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }

    return render(request, 'posApp/receipt.html',context)
    # return HttpResponse('')

@login_required
def delete_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id = id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')

@login_required
def customers(request):
    customer_list = Customer.objects.all()
    context = {
        'page_title':'Customer List',
        'customers':customer_list,
    }
    return render(request, 'posApp/customer.html',context)

@login_required
def manage_customer(request):
    customer = {}
    #categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            customer =Customer.objects.filter(id=id).first()
    
    context = {
        'customer' : customer,
    }
    return render(request, 'posApp/manage_customer.html',context)


@login_required
def save_customer(request):
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Customer.objects.exclude(id=id).filter(mobile=data['mobile']).all()
    else:
        check = Customer.objects.filter(mobile=data['mobile']).all()
    if len(check) > 0 :
        resp['msg'] = "Customer Mobile Already Exists in the database"
    else:
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_customer = Customer.objects.filter(id = data['id']).update(name=data['name'], mobile=data['mobile'], address = data['address'])
            else:
                save_customer =Customer(name=data['name'], mobile = data['mobile'], address =data['address'])
                save_customer.save()
            resp['status'] = 'success'
            messages.success(request, 'Customer Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_customer(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Customer.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Customer Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
# def manage_customer_search(request):
#     customer={}
#     if request.method == 'GET':
#         data =  request.GET
#         id = ''
#         if 'id' in data:
#             id= data['id']
#         if id.isnumeric() and int(id) > 0:
#             customer =Customer.objects.filter(id=id).first()
    
#     context = {
#         'customer' : customer,
#     }
#     return render(request, 'posApp/customer_search.html',context)

@login_required
def search_customer(request):
    #data = request.POST['search']
    
    if request.method=='POST':
        data=request.POST
        try:
         if str(data['search']).isnumeric():
            searched = Sales.objects.filter(mobile=data['search']).all()
            length=len(searched)
            total_sales=m.ceil(sum(searched.values_list('grand_total',flat=True)))
            total_payment=m.ceil(sum(searched.values_list('payment',flat=True)))
            total_udhaar=m.ceil(sum(searched.values_list('udhaar',flat=True)))
         else:
            searched = Sales.objects.filter(name=data['search']).all()
            length=len(searched)
            total_sales=m.ceil(sum(searched.values_list('grand_total',flat=True)))
            total_payment=m.ceil(sum(searched.values_list('payment',flat=True)))
            total_udhaar=m.ceil(sum(searched.values_list('udhaar',flat=True)))
        except Sales.DoesNotExist:
          messages.error(request, 'No Match in your data')  # Add an error message
        

    

    context = {
        'search': searched,
        'total_sales':total_sales,
        'total_payment':total_payment,
        'total_udhaar':total_udhaar,
        'length':length,

    }

    return render(request, "posApp/search.html", context)   
   


