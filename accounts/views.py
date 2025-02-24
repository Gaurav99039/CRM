from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CreateUserFrom
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unautheicated_user,allowed_users,admin_only
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
@unautheicated_user
def register(request):
        form = CreateUserFrom()
        if request.method == 'POST':
            form = CreateUserFrom(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='customer')
                user.groups.add(group)
                messages.success(request,'You have sucessfully registered' + username)
                return redirect('login')
        context = {'form':form}
        return render(request,'accounts/register.html',context)

@unautheicated_user
@csrf_exempt
def login_user(request):
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_auth = authenticate(request,username = username,password = password)
            if user_auth is not None:
                login(request,user_auth)
                return redirect('home')
            else:
                messages.info(request,"UserName and Password is incorrect")
        return render(request,'accounts/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='pending').count()
    context = {'customers':customers,'orders':orders,'total_orders':total_orders
                ,'delivered': delivered,'pending':pending}
    return render(request,'accounts/dashboard.html',context)

def userpage(request):
    context = {}
    return render(request,'accounts/user.html')

@login_required(login_url='login')
@allowed_users(['admin'])
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(['admin'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    myfilter = OrderFilter(request.GET,queryset=orders)
    orders = myfilter.qs
    order_count = orders.count()
    context = {'customer':customer,'orders':orders,'order_count':order_count,'myfilter':myfilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(['admin'])
def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request,'accounts/create_order.html',context)

@login_required(login_url='login')
@allowed_users(['admin'])
def update_order(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/create_order.html',context)

@login_required(login_url='login')
@allowed_users(['admin'])
def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order':order}
    return render(request,'accounts/delete_order.html',context)    