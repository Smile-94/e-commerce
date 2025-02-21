from loguru import logger
from PIL import Image


def get_validate_image_extensions(
    images: list,
    valid_extensions: set[str] | None = None,
    *args,
    **kwargs,
) -> list[str] | None:
    """
    Validates the extensions of uploaded images.

    Args:
        images (list): A list of InMemoryUploadedFile objects.
        valid_extensions (Optional[Set[str]]): A set of valid file extensions provided by the user.
            If not provided, defaults to {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}.

    Returns:
        Optional[List[str]]: A list of invalid image names if any, otherwise None.
    """
    try:
        if valid_extensions is None:
            valid_extensions = {
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".tiff",
                ".webp",
            }

        invalid_images = []

        for image in images:
            if not image.name.lower().endswith(tuple(valid_extensions)):
                invalid_images.append(image.name)

        if invalid_images:
            return invalid_images
        else:
            return None

    except Exception as e:
        logger.error(f"ERROR(get_validate_image_extensions):---->> {str(e)}")
        return None


def get_validate_image_dimensions(
    images: list,
    max_width: int | None = None,
    max_height: int | None = None,
    min_width: int | None = None,
    min_height: int | None = None,
    *args,
    **kwargs,
) -> list[str] | None:
    """
    Validates the dimensions (height and width) of uploaded images.

    Args:
        images (list): A list of InMemoryUploadedFile objects.
        max_width (Optional[int]): Maximum allowed width for the images. If None, no constraint.
        max_height (Optional[int]): Maximum allowed height for the images. If None, no constraint.
        min_width (Optional[int]): Minimum allowed width for the images. If None, no constraint.
        min_height (Optional[int]): Minimum allowed height for the images. If None, no constraint.

    Returns:
        Optional[List[str]]: A list of image names that fail the validation, otherwise None.
    """
    try:
        invalid_images = []

        for image in images:
            # Open the image using Pillow
            img = Image.open(image)
            width, height = img.size

            # Validate dimensions
            if (
                (max_width is not None and width > max_width)
                or (max_height is not None and height > max_height)
                or (min_width is not None and width < min_width)
                or (min_height is not None and height < min_height)
            ):
                invalid_images.append(image.name)

        if invalid_images:
            return invalid_images
        else:
            return None

    except Exception as e:
        logger.error(f"An error occurred while validating image dimensions: {str(e)}")
        return None
