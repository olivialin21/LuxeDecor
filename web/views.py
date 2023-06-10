from django.shortcuts import render, get_object_or_404
from web.models import Product, Category, SubCategory

# Create your views here.
def index(request):
  return render(request, 'index.html')

def product(request, category_name, subcategory_name=None):
    try:
        category = Category.objects.get(title=category_name)
    except Category.DoesNotExist:
        category = None

    try:
        subcategory = SubCategory.objects.get(category=category, title=subcategory_name)
    except SubCategory.DoesNotExist:
        subcategory = None
        
    if category and subcategory:
        product = Product.objects.filter(category=category, sub_category=subcategory)
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