from django.shortcuts import render
import datetime
from .models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


@cache_page(60)
def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    context = {
        'date': datetime.datetime.now(),
        'title': 'GeekShop - Каталог',
        'product_categories': get_links_menu(),
    }

    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('name')
    else:
        products = get_products()
    paginator = Paginator(products, per_page=3)
    products_paginator = paginator.page(page)
    context.update({'product': products_paginator})
    return render(request, 'products/products.html', context)

