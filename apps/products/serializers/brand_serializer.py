from rest_framework.serializers import (
    ModelSerializer,
)

from apps.common.mixinclass.serializer_mixin import FilterFieldMixin

# Import Models
from apps.products.models.brand_model import Brand


# * <<-------------------------------------*** Brand Serializer ***-------------------------------------->>
class BrandSerializer(FilterFieldMixin, ModelSerializer):
    """
    Serializer for Brand model.
    """

    def __init__(self, *args, **kwargs):
        model_field = self.fields
        super().__init__(model_field, *args, **kwargs)

    class Meta:
        model = Brand
        fields = "__all__"
        extra_kwargs = {
            "brand_name": {"required": True},
            "origin_country": {"required": False},
            "brand_logo": {"required": False},
            "contact_number": {"required": False},
            "brand_email": {"required": False},
            "active_status": {"required": False},
            "description": {"required": False},
        }
        read_only_fields = (
            "created_at",
            "updated_at",
        )


# * <<-------------------------------------*** Brand Update Serializer ***-------------------------------------->>
class BrandUpdateSerializer(ModelSerializer):
    """
    Serializer for Brand model (Update).
    """

    class Meta:
        model = Brand
        fields = (
            "brand_name",
            "origin_country",
            "brand_logo",
            "contact_number",
            "brand_email",
            "active_status",
            "description",
        )
        extra_kwargs = {
            "brand_name": {"required": False},
            "origin_country": {"required": False},
            "brand_logo": {"required": False},
            "contact_number": {"required": False},
            "brand_email": {"required": False},
            "active_status": {"required": False},
            "description": {"required": False},
        }
        read_only_fields = (
            "created_at",
            "updated_at",
        )
