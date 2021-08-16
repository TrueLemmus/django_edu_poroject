from django.shortcuts import render
import datetime
import json


def json_import(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as json_data:
        return json.load(json_data)


def index(request):
    context = {
        'title': 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'date': datetime.datetime.now(),
        'title': 'GeekShop - Каталог',
        'products': json_import('products/fixtures/products.json')
    }
    return render(request, 'products/products.html', context)
