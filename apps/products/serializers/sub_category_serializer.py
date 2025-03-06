from rest_framework.serializers import (
    ModelSerializer,
)

from apps.common.mixinclass.serializer_mixin import FilterFieldMixin

# Import Models
from apps.products.models.sub_category_model import SubCategory
from apps.products.serializers.category_serializer import CategorySerializer


# * <<-------------------------------------*** SubCategory Serializer ***-------------------------------------->>
class SubCategorySerializer(FilterFieldMixin, ModelSerializer):
    """
    Serializer for SubCategory model.
    """

    def __init__(self, *args, **kwargs):
        model_field = self.fields
        super().__init__(model_field, *args, **kwargs)

    class Meta:
        model = SubCategory
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Check if 'allowed_fields' is defined
        model_fields = getattr(self, "model_field", None)

        if model_fields:
            if "category" in model_fields and instance.category:
                data["category"] = CategorySerializer(
                    instance.category,
                    fields=[
                        "id",
                        "category_name",
                    ],
                ).data

        return data


# * <<-------------------------------------*** SubCategory Update Serializer ***-------------------------------------->>
class SubCategoryUpdateSerializer(ModelSerializer):
    """
    Serializer for SubCategory model (Update).
    """

    class Meta:
        model = SubCategory
        fields = (
            "sub_category_name",
            "parent_id",
            "category",
            "is_client_usable",
            "active_status",
            "description",
            "sub_category_icon",
        )
        extra_kwargs = {
            "sub_category_name": {"required": False},
            "category": {"required": False},
            "parent_id": {"required": False},
            "is_client_usable": {"required": False},
            "active_status": {"required": False},
            "description": {"required": False},
            "sub_category_icon": {"required": False},
        }
        read_only_fields = (
            "created_at",
            "updated_at",
        )
