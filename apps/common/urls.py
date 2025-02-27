from django.urls import include, path

from apps.products.urls import brand_url

# * <<-------------------------------------*** Product API Router ***-------------------------------------->>
urlpatterns = [
    path("products/brand/", include(brand_url)),  # product brand api router
]
