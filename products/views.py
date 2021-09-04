from django.shortcuts import render
import datetime
from .models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    context = {
        'date': datetime.datetime.now(),
        'title': 'GeekShop - Каталог',
        'product_categories': ProductCategory.objects.all()
    }

    prods = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    context['products'] = prods

    return render(request, 'products/products.html', context)
