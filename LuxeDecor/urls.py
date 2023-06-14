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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
