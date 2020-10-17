from django.urls import path
from products.models import Products
import csv
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reset', views.reset, name='reset'),
]

def ready():
    Products.objects.all().delete()
    dataReader = csv.reader(open('intern-test-data.csv'), delimiter=',', quotechar='"')
    next(dataReader)
    for row in dataReader:
        _, product = Products.objects.get_or_create(
            product_name = row[0],
            price = row[1],
            dimension = row[2],
            colours = row[3],
            material = row[4],
            image = row[5],
            seen = False,
            in_stock = True
        )
    out = Products.objects.get(product_name="Sofa 2 dudukan Vienna")
    out.in_stock = False
    out.save()

# ready()