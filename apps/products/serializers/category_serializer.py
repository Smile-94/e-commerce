from rest_framework.serializers import (
    ModelSerializer,
)

from apps.common.mixinclass.serializer_mixin import FilterFieldMixin

# Import Models
from apps.products.models.category_model import Category


# * <<-------------------------------------*** Category Serializer ***-------------------------------------->>
class CategorySerializer(FilterFieldMixin, ModelSerializer):
    """
    Serializer for Category model.
    """

    def __init__(self, *args, **kwargs):
        model_field = self.fields
        super().__init__(model_field, *args, **kwargs)

    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            "category_name": {"required": True},
            "parent_id": {"required": False},
            "is_client_usable": {"required": False},
            "active_status": {"required": False},
        }
        read_only_fields = (
            "created_at",
            "updated_at",
        )


# * <<-------------------------------------*** Category Update Serializer ***-------------------------------------->>
class CategoryUpdateSerializer(ModelSerializer):
    """
    Serializer for Category model (Update).
    """

    class Meta:
        model = Category
        fields = (
            "category_name",
            "parent_id",
            "is_client_usable",
            "active_status",
        )
        extra_kwargs = {
            "category_name": {"required": False},
            "parent_id": {"required": False},
            "is_client_usable": {"required": False},
            "active_status": {"required": False},
        }
        read_only_fields = (
            "created_at",
            "updated_at",
        )
