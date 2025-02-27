# * PYDANTIC IMPORTS

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from apps.common.models import ActiveStatusChoices


# * <<-------------------------------------*** Brand Create Request Data Model ***--------------------------------->>
class BrandCreateRequestModel(BaseModel):
    brand_name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="The product brand name, i.e. Apple",
    )
    origin_country: str | None = Field(
        default="Bangladesh",
        min_length=3,
        max_length=255,
        description="The brand origin country, i.e. Bangladesh",
    )
    brand_logo: str | None = Field(
        None,
        description="The brand logo image URL",
    )
    contact_number: str | None = Field(
        None,
        description="The brand contact number",
    )
    brand_email: EmailStr | None = Field(
        None,
        description="The brand Email",
    )
    active_status: ActiveStatusChoices | None = Field(
        default=ActiveStatusChoices.ACTIVE,
        description="The brand is active or inactive",
    )
    description: str | None = Field(
        None,
        min_length=10,
        max_length=500,
        description="The product brand description",
    )
