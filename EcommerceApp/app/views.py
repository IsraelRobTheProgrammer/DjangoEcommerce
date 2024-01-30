import threading
from django.core.mail import EmailMessage
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product
from django.contrib import messages

from .forms import CustomerProfileForm, CustomerRegForm


# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send(fail_silently=False)


# Basic views
def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

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
        messages.success(request, "Email Sent Succesfully, thanks for the feedback 😊")
    return render(request, "contact.html")


# User Auth Views
class CustomerRegView(View):
    def get(self, request):
        form = CustomerRegForm()
        return render(request, "customer_reg.html", locals())

    def post(self, request):
        form = CustomerRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Registration Successfull, Please Login")
            return redirect("customer_login")
        return render(request, "customer_reg.html", locals())


customer_reg_view = CustomerRegView.as_view()


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            mobile = form.cleaned_data["mobile"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]

            customer = Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcode=zipcode,
            )

            customer.save()
            messages.success(request, "Profile Saved Successfully")

        else:
            messages.error(request, "Invalid Input Data")
        return render(request, "profile.html", locals())


profile_view = ProfileView.as_view()


def address(request):
    user_addresses = Customer.objects.filter(user=request.user)
    return render(request, "address.html", locals())


class UpdateAddress(View):
    def get(self, request, id):
        address = Customer.objects.get(id=id)
        form = CustomerProfileForm(instance=address)
        return render(request, "update_address.html", locals())

    def post(self, request, id):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            address = Customer.objects.get(id=id)
            address.name = form.cleaned_data["name"]
            address.locality = form.cleaned_data["locality"]
            address.city = form.cleaned_data["city"]
            address.mobile = form.cleaned_data["mobile"]
            address.state = form.cleaned_data["state"]
            address.zipcode = form.cleaned_data["zipcode"]

            address.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            messages.error(request, "Invalid Input Data")
        return redirect("address")


update_address_view = UpdateAddress.as_view()


# Product, Category Views
class CategoryView(View):
    def get(self, request, value):
        prod_obj = Product.objects.filter(category=value)
        products = prod_obj.values("title")

        return render(request, "category.html", locals())


category_view = CategoryView.as_view()


class CategoryTitle(View):
    def get(self, request, value):
        prod_obj = Product.objects.filter(title=value)
        products = Product.objects.filter(category=prod_obj[0].category).values("title")

        return render(request, "category.html", locals())


category_title = CategoryTitle.as_view()


class ProductDetail(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, "product_detail.html", locals())


product_detail = ProductDetail.as_view()
