from django.db.models import Count
from django.shortcuts import render
from django.views import View
from .models import Product

# Create your views here.


def home(req):
    return render(req, "index.html")


class CategoryView(View):
    def get(self, req, value):
        prod_obj = Product.objects.filter(category=value)
        products = prod_obj.values("title")

        return render(req, "category.html", locals())


category_view = CategoryView.as_view()


class CategoryTitle(View):
    def get(self, req, value):
        prod_obj = Product.objects.filter(title=value)
        products = Product.objects.filter(category=prod_obj[0].category).values("title")

        print(prod_obj, prod_obj[0])
        return render(req, "category.html", locals())


category_title = CategoryTitle.as_view()


class ProductDetail(View):
    def get(self, req, id):
        product = Product.objects.get(id=id)
        # print(product)

        return render(req, "product_detail.html", locals())


product_detail = ProductDetail.as_view()
