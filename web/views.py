from django.shortcuts import render, get_object_or_404, redirect
from web.models import Product, Category, SubCategory, CartItem
from django.http import HttpResponse
# login authentication
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from decimal import Decimal

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
        first_name = request.user.first_name
        name = first_name + " " + request.user.last_name
        email = request.user.email
    else:
        first_name = None
        name = None
        email = None
    return render(request, "mypage.html", {'first_name': first_name, 'name': name, 'email': email})


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
    else:
        mess = ""
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
                auth.login(request, user)
                return redirect('/mypage/')
        else:
            mess = "Please fill in all the required information."
    else:
        mess = ""
    return render(request, "register.html", locals())


def edit(request):
    user = request.user
    if request.method == "POST":
        if request.POST['first_name'] != "" and request.POST['last_name'] != "" and request.POST['account'] != "":
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            account = request.POST.get('account', '').strip()

            # 更新用户的姓氏和名字
            user.first_name = first_name
            user.last_name = last_name
            user.username = account
            user.email = account
            user.save()

            # 重定向到用户的个人资料页面或其他适当的页面
            return redirect('/mypage/')
        else:
            mess = "Please fill in all the required information."
    else:
        mess = ""
    return render(request, 'edit.html', {'user': user, 'mess': mess})


def shoppingCart(request):
    cart = request.COOKIES.get('cart')  # 從 Cookie 中獲取購物車數據
    cart_items = []
    total_price = 0
    if request.user.is_authenticated:
        user = request.user

        # 從後端資料庫獲取使用者的購物車項目
        cart_items_data = user.cart_items.all()

        for cart_item in cart_items_data:
            product = cart_item.product
            quantity = cart_item.quantity
            price = round(Decimal(product.price) * quantity)

            total_price += price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price
            })
    elif cart:
        cart_items_data = parseCartItems(cart)  # 解析購物車內容

        # 從資料庫中獲取購物車內商品的詳細資訊
        product_ids = list(cart_items_data.keys())
        products = Product.objects.filter(id__in=product_ids)

        # 計算金額總和並建立商品清單
        for product in products:
            quantity = cart_items_data[product.id]
            price = round(Decimal(product.price) * quantity)

            total_price += price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price
            })

    return render(request, 'shoppingCart.html', {'cart_items': cart_items, 'total_price': total_price})


def addToCart(request, id=None):
    product = get_object_or_404(Product, id=id)
    user = request.user

    # 從 Cookie 中獲取現有的購物車內容
    cart = request.COOKIES.get('cart', '')

    # 將購物車內容轉換為字典，如果購物車內容不存在，則創建一個空字典
    cart_items = {}
    if cart:
        cart_items = parseCartItems(cart)

    # 檢查商品是否已經在購物車中，如果是則增加數量，如果不是則添加新的商品
    if product.id in cart_items:
        cart_items[product.id] += 1
    else:
        cart_items[product.id] = 1

    # 檢查是否有使用者登入，如果有則將購物車內容同步到資料庫
    if user.is_authenticated:
        user.cart_items.all().delete()  # 先刪除用戶現有的購物車項目
        for product_id, quantity in cart_items.items():
            CartItem.objects.create(user=user, product_id=product_id, quantity=quantity)

    # 將更新後的購物車內容轉換為字符串
    updated_cart = stringifyCartItems(cart_items)

    # 將更新後的購物車內容存回 Cookie
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('cart', updated_cart)

    return response

def parseCartItems(cart):
    # 解析購物車內容字符串，返回字典形式的購物車內容
    # 例如，將 "1:2,3:1" 解析為 {1: 2, 3: 1}
    cart_items = {}
    items = cart.split(',')
    for item in items:
        if ":" in item:
            product_id, quantity = item.split(':')
            cart_items[int(product_id)] = int(quantity)
    return cart_items

def stringifyCartItems(cart_items):
    # 將字典形式的購物車內容轉換為字符串形式
    # 例如，將 {1: 2, 3: 1} 轉換為 "1:2,3:1"
    cart = ''
    for product_id, quantity in cart_items.items():
        cart += f'{product_id}:{quantity},'
    return cart

def delete_product(request, product_id):
    cart = request.COOKIES.get('cart')  # 從 Cookie 中獲取購物車數據

    if cart:
        cart_items = parseCartItems(cart)  # 解析購物車內容
        if product_id in cart_items:
            del cart_items[product_id]  # 移除指定商品ID
            updated_cart = stringifyCartItems(cart_items)  # 將更新後的購物車內容轉換為字符串
            messages.success(request, 'Product deleted successfully.')

            # 更新 Cookie 中的購物車數據
            response = redirect('/shoppingCart/')
            response.set_cookie('cart', updated_cart)
            return response

    return redirect('/shoppingCart/')

def decrease_quantity(request, product_id):
    user = request.user
    cart = request.COOKIES.get('cart')
    if cart:
        cart_items = parseCartItems(cart)
        if product_id in cart_items:
            cart_items[product_id] -= 1
            if cart_items[product_id] <= 0:
                del cart_items[product_id]
            updated_cart = stringifyCartItems(cart_items)
            response = redirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie('cart', updated_cart)
            
            # 更新後台資料庫中的購物車項目數量
            if user.is_authenticated:
                cart_item = get_object_or_404(CartItem, product_id=product_id, user=user)
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()

            return response
    return redirect('/shoppingCart/')

def increase_quantity(request, product_id):
    user = request.user
    cart = request.COOKIES.get('cart')
    if cart:
        cart_items = parseCartItems(cart)
        if product_id in cart_items:
            cart_items[product_id] += 1
            updated_cart = stringifyCartItems(cart_items)
            response = redirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie('cart', updated_cart)

            # 更新後台資料庫中的購物車項目數量
            if user.is_authenticated:
                cart_item, created = CartItem.objects.get_or_create(product_id=product_id, user=user)
                cart_item.quantity += 1
                cart_item.save()

            return response
    return redirect('/shoppingCart/')