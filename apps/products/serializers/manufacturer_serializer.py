from rest_framework.serializers import (
    ModelSerializer,
)

from apps.common.mixinclass.serializer_mixin import FilterFieldMixin

# Import Models
from apps.products.models.manufacturer_model import (
    Manufacturer,
    ManufacturerProductCategory,
)


# * <<-------------------------------------*** Manufacturer Product Category Serializer ***-------------------------------------->>
class ManufacturerProductCategorySerializer(FilterFieldMixin, ModelSerializer):
    """
    Serializer for ManufacturerProductCategory model.
    """

    def __init__(self, *args, **kwargs):
        model_field = self.fields
        super().__init__(model_field, *args, **kwargs)

    class Meta:
        model = ManufacturerProductCategory
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
        )


# * <<-------------------------------------*** Manufacturer Product Category Update Serializer ***-------------------------------------->>
class ManufacturerProductCategoryUpdateSerializer(ModelSerializer):
    """
    Serializer for ManufacturerProductCategory model (Update).
    """

    class Meta:
        model = ManufacturerProductCategory
        fields = (
            "product_category",
            "active_status",
            "description",
        )
        extra_kwargs = {
            "product_category": {"required": False},
            "active_status": {"required": False},
            "description": {"required": False},
        }


# * <<-------------------------------------*** Manufacturer Serializer ***-------------------------------------->>
class ManufacturerSerializer(FilterFieldMixin, ModelSerializer):
    """
    Serializer for Manufacturer model.
    """

    def __init__(self, *args, **kwargs):
        model_field = self.fields
        super().__init__(model_field, *args, **kwargs)

    class Meta:
        model = Manufacturer
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
        )


# * <<-------------------------------------*** Manufacturer Update Serializer ***-------------------------------------->>
class ManufacturerUpdateSerializer(ModelSerializer):
    """
    Serializer for Manufacturer model (Update).
    """

    class Meta:
        model = Manufacturer
        fields = (
            "product_category",
            "manufacturer_name",
            "manufacturer_logo",
            "contact_person",
            "manufacturer_email",
            "manufacturer_phone",
            "manufacturer_address",
            "manufacturer_category",
            "active_status",
            "description",
        )
        extra_kwargs = {
            "product_category": {"required": False},
            "manufacturer_name": {"required": False},
            "manufacturer_logo": {"required": False},
            "contact_person": {"required": False},
            "manufacturer_email": {"required": False},
            "manufacturer_phone": {"required": False},
            "manufacturer_address": {"required": False},
            "manufacturer_category": {"required": False},
            "active_status": {"required": False},
            "description": {"required": False},
        }
        read_only_fields = (
            "created_at",
            "updated_at",
        )
