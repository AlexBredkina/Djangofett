from django.shortcuts import render
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    context = {
        'title': 'Главная страница',
    }

    return render(request, 'mainapp/index.html', context)


def products(request, page=1, category_id=None,):
    context = {
        'title': 'Товары',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    if category_id:
        products = Product.objects.filter(category_id = category_id).order_by('price')
    else:
        products = Product.objects.all().order_by('price')

    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator(1)
    except EmptyPage:
        products_paginator = paginator(paginator.num_pages)

    context.update({'products': products_paginator})

    return render(request, 'mainapp/products.html', context=context)


# def test_context(request):
#     context = {
#         'title': 'добро пожаловать!',
#         'username': 'Valeriy Pavlikov',
#         'products': [{'name': 'Черное худи', 'price': '2 9990 руб.'},
#                      {'name': 'Джинсы', 'price': '5 800 руб.'},
#
#                      ],
#         'promotion': True,
#         'promotion_products': [
#             {'name': 'Туфли Dr Martnes', 'price': '10 000 руб.'},
#         ],
#
#     }
#     products = context['products']
#     return render(request, 'mainapp/context.html', context)
