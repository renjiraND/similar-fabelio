from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Products
from difflib import SequenceMatcher
import locale

locale.setlocale(locale.LC_ALL,"id_ID.UTF-8")

@csrf_exempt
def reset(request):
    products = Products.objects.all()
    for product in products:
        product.seen = False
        product.save()
    return HttpResponseRedirect('/products')

def index(request):
    products = Products.objects.all()
    out_of_stock = products[0]
    products = products[1:len(products)-1]
    chosen = choseSimilar(out_of_stock, products)
    if not chosen == -1:
        change = products[chosen]
        change.seen = True
        change.save()
    chosen_product = products[chosen]
    print(chosen_product.seen)
    chosen_product.price = locale.currency(chosen_product.price)
    context = {
        'chosen': chosen_product,
    }
    response = render(request, "index.html", context)
    response.set_cookie("price", chosen_product.price)
    return response

def similarString(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getScore(a,b):
    score = 0
    score += similarString(a.product_name, b.product_name)
    score += similarString(a.colours, b.colours)
    score += similarString(a.material, b.material)
    score += similarString(a.dimension, b.dimension)
    return score

def choseSimilar(out_of_stock,products):
    maxval = 0
    maxidx = -1
    for i in range(len(products)):
        if products[i].seen == False:
            score = getScore(out_of_stock, products[i])
            if(score > maxval):
                maxidx = i
                maxval = score
    return maxidx
