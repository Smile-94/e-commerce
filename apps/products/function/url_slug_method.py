from django.utils.text import slugify


def get_generated_slug(
    product_name: str,
    product_unit: str | None = None,
    unit_attribute: str | None = None,
) -> str:
    """
    Generate a slug using product name, product unit, and unit attribute.

    Args:
        product_name (str): The name of the product.
        product_unit (Optional[str]): The unit of the product.
        unit_attribute (Optional[str]): Additional attribute of the product.

    Returns:
        str: A URL-friendly slug.
    """
    if not product_name:
        return ""  # Ensure product name is required for slug creation.

    # Append the unit and attribute if available
    components = [
        product_name,
    ]
    if product_unit:
        components.append(product_unit)
    if unit_attribute:
        components.append(unit_attribute)

    # Combine and slugify the final result
    slug_url = slugify(" ".join(components))
    return slug_url
