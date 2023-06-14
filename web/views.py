from django.shortcuts import render, get_object_or_404, redirect
from web.models import Product, Category, SubCategory

# 匯入相關套件
from django.http import HttpResponse
# login authentication
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def product(request, category_name, subcategory_name=None):
    try:
        category = Category.objects.get(title=category_name)
    except Category.DoesNotExist:
        category = None

    try:
        subcategory = SubCategory.objects.get(
            category=category, title=subcategory_name)
    except SubCategory.DoesNotExist:
        subcategory = None

    if category and subcategory:
        product = Product.objects.filter(
            category=category, sub_category=subcategory)
    elif category:
        product = Product.objects.filter(category=category)
    else:
        product = []

    context = {
        'category': category_name,
        'subCategory': subcategory_name,
        'product': product,
    }

    return render(request, 'product.html', context)


def detail(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'detail.html', locals())


def account(request):
    if request.user.is_authenticated:
        return redirect('/mypage/')
    else:
        return redirect('/login/')


def mypage(request):
    if request.user.is_authenticated:
        name = request.user.username
    else:
        name = None
    return render(request, "mypage.html", {'name': name})


def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                mess = 'Login successful.'
                return redirect('/mypage/')
            else:
                mess = 'This account does not exist.'
        else:
            mess = 'Login failed.'
    return render(request, "login.html", locals())


def logout(request):
    auth.logout(request)
    return redirect('/login/')

def register(request):
    if request.method == "POST":
        if request.POST['account'] != "" and request.POST['password'] != "" and request.POST['firstName'] != "" and request.POST['lastName'] != "":
            account = request.POST['account']
            email = request.POST['account']
            password = request.POST['password']
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']

            try:
                user = User.objects.get(username=account)
                mess = "This account has already been registered."
            except User.DoesNotExist:
                # 新增 user
                user = User.objects.create_user(account, email, password)
                user.first_name = firstName  # 姓名
                user.last_name = lastName  # 姓氏
                user.save()
                auth.login(request,user)
                return redirect('/mypage/')
        else:
            mess = "Please fill in all the required information."
    else:
        mess = "Registration failed."
    return render(request, "register.html", locals())