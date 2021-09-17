from django.http import request
from accounts.filters import Orderfilter
from django.shortcuts import render,redirect
from accounts.models import *
from django.forms import inlineformset_factory
from accounts.forms import CustomerForm,Productform,Orderform,CreateUserForm
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib.auth import authenticate,logout,login 
from django.urls.base import reverse_lazy
from django.contrib import messages
from .decorators import admin_only, allowed_used, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group

@unauthenticated_user
def RegisterPage(request):
    form=CreateUserForm
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
           user=form.save()
           username= form.cleaned_data.get('username')

           messages.success(request,'Account was successfully created for' + username)
           return redirect('login')
    return render(request,'accounts/register.html',{'form':form})

@unauthenticated_user
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')
            return render(request,'accounts/login.html') 
    return render(request,'accounts/login.html')  

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customer=Customer.objects.all()
    orders=Order.objects.all().order_by('-data_created')[0:5]
    totalorder=Order.objects.all().count()
    deliveredorder=Order.objects.filter(status='Delivered').count()
    pendingorder=Order.objects.filter(status='Pending').count()
    return render(request,'accounts/dashboard.html',{
        'customer':customer,
        'orders':orders,
        'totalorder':totalorder,
        'deliveredorder':deliveredorder,
        'pendingorder':pendingorder,
        })

@login_required(login_url='login')
@allowed_used(allowed_roles=['admin'])
def products(request):
    product=Product.objects.all()
    return render(request,'accounts/product.html',{'product':product})

@login_required(login_url='login')
@allowed_used(allowed_roles=['customer'])
def account_settings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)

    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    return render(request,'accounts/account_settings.html',{'form':form})

@login_required(login_url='login')
@allowed_used(allowed_roles=['customer'])
def Userpage(request):
    orders=request.user.customer.order_set.all()
    totalorder=orders.count()
    deliveredorder=orders.filter(status='Delivered').count()
    pendingorder=orders.filter(status='Pending').count()
    return render(request,'accounts/user.html',{
        'orders':orders,
        'totalorder':totalorder,
        'deliveredorder':deliveredorder,
        'pendingorder':pendingorder,
        })


@login_required(login_url='login')
@allowed_used(allowed_roles=['admin'])
def Createcustomer(request):
    if request.method=='POST':
        custObj=CustomerForm(request.POST or None, request.FILES or None)
        if custObj.is_valid():
            custObj.save()
            return redirect('home')
    else:
        custObj=CustomerForm()
        return render(request,'accounts/Customer_form.html',{'form':custObj})

@login_required(login_url='login')
@allowed_used(allowed_roles=['admin'])
def Createproduct(request):
    if request.method=='POST':
        prodObj=Productform(request.POST or None, request.FILES or None)
        if prodObj.is_valid():
            prodObj.save()
            return redirect('products')
    else:
        prodObj=Productform()
        return render(request,'accounts/Product_form.html',{'form':prodObj}) 


@login_required(login_url='login')
@allowed_used(allowed_roles=['admin'])
def CustomerDetailView(request,pk):
    cust=Customer.objects.get(pk=pk)
    orders=cust.order_set.all()
    products=Product.objects.all()
    myfilter=Orderfilter(request.GET,queryset=orders)
    orders=myfilter.qs
    return render(request,'accounts/Customer_detail.html',{'cust':cust,'orders':orders,'products':products,'myfilters':myfilter})


@login_required(login_url='login')
@allowed_used(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer, Order, fields=('product','status'),extra=10)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = Orderform(initial={'customer':customer})
    if request.method == 'POST':
	#     # form = Orderform(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')          
    context =  {'form':formset}
    return render(request, 'accounts/Order_form.html', context)   

@login_required(login_url='login')
@allowed_used(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = Orderform(instance=order)
    if request.method == 'POST':
	    form = Orderform(request.POST, instance=order)
	    if form.is_valid():
		    form.save()
		    return render(request, 'accounts/dashboard.html')
    context =  {'form':form}
    return render(request, 'accounts/Order_form.html', context)     


@login_required(login_url='login')
@allowed_used(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
	    customer_id = order.customer.id
	    order.delete()
	    return redirect('home')
    return render(request, 'accounts/Order_confirm_delete.html', {'item':order})

