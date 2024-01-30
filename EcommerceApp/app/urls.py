from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from django.contrib.auth import views as auth_view
from .forms import LoginForm, PswdChangeForm, PswdResetForm, SetPswdForm


urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("category/<slug:value>", views.category_view, name="category"),
    path("category-title/<str:value>", views.category_title, name="category_title"),
    path("product-detail/<int:id>", views.product_detail, name="product-detail"),
    # USERS AND AUTH SECTION
    path("registration", views.customer_reg_view, name="customer_reg"),
    path("profile", views.profile_view, name="profile"),
    path("address", views.address, name="address"),
    path("update-address/<int:id>", views.update_address_view, name="update_address"),
    path(
        "login",
        auth_view.LoginView.as_view(
            template_name="customer_login.html",
            authentication_form=LoginForm,
        ),
        name="customer_login",
    ),
    path(
        "logout",
        auth_view.LogoutView.as_view(next_page="/"),
        name="customer_logout",
    ),
    path(
        "password-change",
        auth_view.PasswordChangeView.as_view(
            template_name="pswd_change.html",
            form_class=PswdChangeForm,
            success_url="/password-change-done",
        ),
        name="pswd_change",
    ),
    path(
        "password-change-done",
        auth_view.PasswordChangeDoneView.as_view(template_name="pswd_change_done.html"),
        name="pswd_change_done",
    ),
    # PSWD RESET
    path(
        "password-reset",
        auth_view.PasswordResetView.as_view(
            template_name="pswd_reset.html",
            form_class=PswdResetForm,
        ),
        name="pswd_reset",
    ),
    path(
        "password-reset/done",
        auth_view.PasswordResetDoneView.as_view(template_name="pswd_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth_view.PasswordResetConfirmView.as_view(
            template_name="pswd_reset_confirm.html", form_class=SetPswdForm
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete",
        auth_view.PasswordResetCompleteView.as_view(
            template_name="pswd_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
