from django.urls import path

# Import Category Views
from apps.products.apis.category_api import (
    CreateProductCategoryAPIView,
    DeleteProductCategoryAPIView,
    ListProductCategoryAPIView,
    RetrieveProductCategoryAPIView,
    UpdateProductCategoryAPIView,
)

# * <<-------------------------------------*** Product Category API Router ***-------------------------------------->>
urlpatterns = [
    path(
        "create/",
        CreateProductCategoryAPIView.as_view(),
        name="create_product_category",
    ),  # create product category api endpoint
    path(
        "update/<int:id>/",
        UpdateProductCategoryAPIView.as_view(),
        name="update_product_category",
    ),  # update product category api endpoint
    path(
        "list/",
        ListProductCategoryAPIView.as_view(),
        name="list_product_category",
    ),  # list product category api endpoint
    path(
        "details/<int:id>/",
        RetrieveProductCategoryAPIView.as_view(),
        name="retrieve_product_category",
    ),  # retrieve product category api endpoint
    path(
        "delete/<int:id>/",
        DeleteProductCategoryAPIView.as_view(),
        name="delete_product_category",
    ),  # delete product category api endpoint
]
