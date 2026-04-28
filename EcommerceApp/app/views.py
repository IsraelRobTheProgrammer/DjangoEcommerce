import secrets
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CustomerProfileForm, CustomerRegForm
from .models import Cart, Customer, Product, OrderPlaced, Payment, WishList

import threading
import requests


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


def search(request):
    query = request.GET.get("search")
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "search.html", locals())


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
            messages.success(
                request, "Profile Saved Successfully, Check out our Products Category"
            )
            return redirect("home")

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
        wishlist = WishList.objects.filter(Q(user=request.user) & Q(product=product))
        return render(request, "product_detail.html", locals())


product_detail = ProductDetail.as_view()


def wishlist(request):
    wishlist_items = WishList.objects.filter(user=request.user)
    return render(request, "wishlist.html", locals())


# Cart/Order Section
def orders(request):
    orders_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, "orders.html", locals())


def add_to_cart(request):
    if request.method == "POST":
        try:
            user = request.user
            if user.is_anonymous:
                messages.error(request, "Please Login First")
                return redirect("customer_login")
            product_id = request.POST.get("prod_id")
            product = Product.objects.get(id=product_id)

            cart_item, created = Cart.objects.get_or_create(user=user, product=product)
            # print(cart_item)

            if created is not True:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, "Item Already In Cart, Quantity Increased")
                return redirect(request.META.get("HTTP_REFERER"))

            cart_item.save()
            messages.success(request, "Item Successfully Added To Cart")
            return redirect(request.META.get("HTTP_REFERER"))

        except Exception as e:
            print(e, "error")
            messages.error(request, "Item Not Added To Cart")
            return redirect(request.META.get("HTTP_REFERER"))


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0

    for item in cart:
        value = item.quantity * item.product.discounted_price
        amount += value
    totalamount = amount + 800

    return render(request, "show_cart.html", locals())


class CheckOut(View):
    def get(self, request):
        user = request.user
        address = Customer.objects.filter(user=user)

        user_cart = Cart.objects.filter(user=user)

        cart_has_items = True if user_cart.count() > 0 else False

        amount = 0

        for item in user_cart:
            value = item.quantity * item.product.discounted_price
            amount += value
        totalamount = amount + 800

        return render(request, "checkout.html", locals())

    def post(self, request):
        try:
            domain = get_current_site(request).domain
            user = request.user
            print(request.POST)
            cust_id = request.POST.get("custid")
            totalamount = request.POST.get("totalamount")

            # global user_cart

            tx_ref = f"tx_{secrets.token_urlsafe(20)}"

            # user_cart = Cart.objects.filter(user=user)
            # amount = 0
            # for item in user_cart:
            #     value = item.quantity * item.product.discounted_price
            #     amount += value
            # totalamount = amount + 800

            if user.is_anonymous:
                messages.error(request, "Please Login First")
                return redirect("customer_login")

            flutterwave_url = "https://api.flutterwave.com/v3/payments"
            secret_key = settings.FLUTTERWAVE_KEY

            payload = {
                "tx_ref": tx_ref,
                "amount": totalamount,
                "currency": "NGN",
                "redirect_url": f"http://{domain}/confirm_payment/" + cust_id,
                # "payment_type": "card",
                "customer": {"email": user.email, "name": user.username},
                "customizations": {
                    "title": "DJECOMMERCE PAYMENTS",
                    # "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png",
                },
            }

            headers = {
                "Authorization": f"Bearer {secret_key}",
                "Content-Type": "application/json",
            }
            # return TypeError
        except Exception as e:
            # print(cust_id, totalamount)
            print(e, "An occured error")
            messages.error(request, "No Address Selected")
            return redirect(request.META.get("HTTP_REFERER"))

        try:
            payment = Payment(
                user=user,
                amount=totalamount,
                tx_ref=tx_ref,
            )
            payment.save()

            response = requests.post(flutterwave_url, json=payload, headers=headers)
            response_data = response.json()
            if response_data["status"] == "success":
                messages.info(request, "Redirecting to Payment Page")
                return redirect(f"{response_data['data']['link']}")

            return JsonResponse(response_data, status=200)

        except requests.exceptions.RequestException as err:
            # Handle request exceptions
            print(err)
            print(request.META, "META")
            messages.error(request, "Payment initiation failed, Please Try Again")
            return redirect(request.META.get("HTTP_REFERER"))
        except ValueError as err:
            print(err)
            print(request.META, "META")
            # Handle JSON decoding error
            messages.error(request, "Payment initiation failed, Please Try Again")
            return redirect(request.META.get("HTTP_REFERER"))


checkout_view = CheckOut.as_view()


def confirm_payment(request, custid):
    # cust_id = request.GET.get("cust_id")
    status = request.GET.get("status")
    tx_ref = request.GET.get("tx_ref")

    user = request.user

    customer = Customer.objects.get(id=custid)
    payment = Payment.objects.get(tx_ref=tx_ref)

    # order_id = "order_" + user
    if status == "successful" or "completed":
        payment.paid = True
        payment.flw_payment_id = f"paid_{user.username}_{secrets.token_hex(10)}"
        payment.save()

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity,
            payment=payment,
        ).save()
        c.delete()

    messages.success(
        request,
        "Payment made successfully",
    )

    return redirect("home")


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.quantity += 1
        cart_item.save()

        user = request.user
        user_cart = Cart.objects.filter(user=user)
        amount = 0

        for item in user_cart:
            value = item.quantity * item.product.discounted_price
            amount += value
        totalamount = amount + 800

        data = {
            "quantity": cart_item.quantity,
            "amount": amount,
            "totalamount": totalamount,
        }

        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.quantity -= 1
        cart_item.save()

        user = request.user
        user_cart = Cart.objects.filter(user=user)
        amount = 0

        for item in user_cart:
            value = item.quantity * item.product.discounted_price
            amount += value
        totalamount = amount + 800

        data = {
            "quantity": cart_item.quantity,
            "amount": amount,
            "totalamount": totalamount,
        }

        return JsonResponse(data)


def remove_item(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.delete()

        user = request.user
        user_cart = Cart.objects.filter(user=user)
        amount = 0

        for item in user_cart:
            value = item.quantity * item.product.discounted_price
            amount += value
        totalamount = amount + 800

        data = {"amount": amount, "totalamount": totalamount}

        return JsonResponse(data)


def plus_wishlist(request):
    if request.method == "GET":
        try:
            prod_id = request.GET["prod_id"]
            product = Product.objects.get(id=prod_id)

            WishList(user=request.user, product=product).save()
            messages.success(request, "Item Added To WishList")

            data = {
                "message": "Item Added To WishList",
            }

            return JsonResponse(data)
        except ObjectDoesNotExist as e:
            print(e)
            messages.error(request, "Item couldn't be added, Please Try Again")
            return redirect(request.META.get("HTTP_REFERER"))


def minus_wishlist(request):
    if request.method == "GET":
        try:
            prod_id = request.GET["prod_id"]
            product = Product.objects.get(id=prod_id)

            wishlist = WishList.objects.filter(
                Q(user=request.user) & Q(product=product)
            )
            wishlist.delete()
            messages.success(request, "Item Removed From WishList")

            data = {
                "message": "Item Removed From WishList",
            }

            return JsonResponse(data)
        except ObjectDoesNotExist as e:
            print(e)
            messages.error(request, "Item couldn't be added, Please Try Again")
            return redirect(request.META.get("HTTP_REFERER"))
