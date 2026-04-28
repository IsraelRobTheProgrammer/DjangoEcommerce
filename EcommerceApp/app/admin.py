from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced, WishList


# Register your models here.
@admin.register(Product)
class ProductAdminOptions(admin.ModelAdmin):
    list_display = ["id", "title", "discounted_price", "category", "product_image"]


@admin.register(Customer)
class CustomerAdminOptions(admin.ModelAdmin):
    list_display = ["id", "user", "locality", "city", "state", "zipcode"]


@admin.register(Cart)
class CartAdminOptions(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity"]


@admin.register(Payment)
class PaymentAdminOptions(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "amount",
        "tx_ref",
        "flw_payment_status",
        "flw_payment_id",
        "paid",
    ]


@admin.register(WishList)
class WishListAdminOptions(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "product",
    ]


@admin.register(OrderPlaced)
class OrderPlacedAdminOptions(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "customer",
        "product",
        "quantity",
        "ordered_date",
        "status",
    ]
