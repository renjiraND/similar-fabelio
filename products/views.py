from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Products
from difflib import SequenceMatcher
import locale
import csv

locale.setlocale(locale.LC_ALL,"id_ID.UTF-8")

def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

@csrf_exempt
def reset(request):
    products = Products.objects.all()
    for product in products:
        product.seen = False
        product.save()
    return HttpResponseRedirect('/')       

def index(request):
    products = Products.objects.filter(in_stock=True)
    out_of_stock = get_or_none(Products,in_stock=False)
    chosen = choseSimilar(out_of_stock, products)
    if not chosen == -1:
        change = products[chosen]
        change.seen = True
        change.save()
        chosen_product = products[chosen]
        chosen_product.price = locale.currency(chosen_product.price)
    else:
        chosen_product = None
    context = {
        'chosen': chosen_product,
    }
    response = render(request, "index.html", context)
    response.set_cookie("cookie", "COOKIE_"+str(chosen))
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
    maxidx = -1
    if out_of_stock == None:
        return maxidx

    maxval = 0
    for i in range(len(products)):
        if products[i].seen == False:
            score = getScore(out_of_stock, products[i])
            if(score > maxval):
                maxidx = i
                maxval = score
    return maxidx
