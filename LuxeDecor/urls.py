"""
URL configuration for LuxeDecor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views as webviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', webviews.index),
    path('about/', webviews.about),
    path('product/category/<str:category_name>/<str:subcategory_name>/', webviews.product),
    path('product/category/<str:category_name>/', webviews.product),
    path('product/<slug:slug>/', webviews.detail, name='detail'),
    # login
    path('account/', webviews.account),
    path('login/', webviews.login),
    path('logout/', webviews.logout),
    path('mypage/', webviews.mypage),
    path('edit/', webviews.edit),
    path('register/', webviews.register),
    # shopping cart
    path('addToCart/<int:id>/', webviews.addToCart, name='addToCart'),
    path('addToCart/decrease_quantity/', webviews.addToCart_decrease_quantity),
    path('addToCart/increase_quantity/', webviews.addToCart_increase_quantity),
    path('shoppingCart/', webviews.shoppingCart),
    path('shoppingCart/delete/<int:product_id>/', webviews.delete_product, name='delete_product'),
    path('shoppingCart/decrease_quantity/<int:product_id>/', webviews.decrease_quantity, name='decrease_quantity'),
    path('shoppingCart/increase_quantity/<int:product_id>/', webviews.increase_quantity, name='increase_quantity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
