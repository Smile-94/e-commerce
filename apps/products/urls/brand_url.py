from django.urls import path

from apps.products.apis.brand_api import (
    CreateProductBrandAPIView,
    DeleteProductBrandAPIView,
    ListProductBrandAPIView,
    RetrieveProductBrandAPIView,
    UpdateProductBrandAPIView,
)

# * <<-------------------------------------*** Product Brand API Router ***-------------------------------------->>
urlpatterns = [
    path(
        "create/",
        CreateProductBrandAPIView.as_view(),
        name="create_product_brand",
    ),  # create product brand api endpoint
    path(
        "update/<int:id>/",
        UpdateProductBrandAPIView.as_view(),
        name="update_product_brand",
    ),  # update product brand api endpoint
    path(
        "list/",
        ListProductBrandAPIView.as_view(),
        name="list_product_brand",
    ),  # list product brand api endpoint
    path(
        "details/<int:id>/",
        RetrieveProductBrandAPIView.as_view(),
        name="retrieve_product_brand",
    ),  # retrieve product brand api endpoint
    path(
        "delete/<int:id>/",
        DeleteProductBrandAPIView.as_view(),
        name="delete_product_brand",
    ),  # delete product brand api endpoint
]
