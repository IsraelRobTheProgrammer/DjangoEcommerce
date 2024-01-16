import threading
from django.core.mail import EmailMessage
from django.db.models import Count
from django.shortcuts import render
from django.views import View
from .models import Product
from django.contrib import messages


# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send(fail_silently=False)


def home(req):
    return render(req, "index.html")


def about(req):
    return render(req, "about.html")


def contact(req):
    if req.method == "POST":
        name = req.POST["name"]
        email = req.POST["email"]
        subject = req.POST["subject"]
        message = req.POST["message"]

        email_body = (
            "Hello, My name is " + name + " and this is my message: \n" + message
        )
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=email,
            to=["israelrob965@gmail.com"],
        )
        EmailThread(email).start()
        messages.success(req, "Email Sent Succesfully 😊")
    return render(req, "contact.html")


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
