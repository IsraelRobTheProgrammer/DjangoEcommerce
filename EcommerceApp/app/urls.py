from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("", views.home),
    path("category/<slug:value>", views.category_view, name="category"),
    path("category-title/<str:value>", views.category_title, name="category_title"),
    path("product-detail/<int:id>", views.product_detail, name="product-detail"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
