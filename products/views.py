from django.shortcuts import render
import datetime
from .models import ProductCategory, Product


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'date': datetime.datetime.now(),
        'title': 'GeekShop - Каталог',
        'products': Product.objects.all(),
        'product_categorys': ProductCategory.objects.all()
    }
    return render(request, 'products/products.html', context)
