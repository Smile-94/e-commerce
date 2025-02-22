from datetime import datetime


def get_generated_barcode(product_id: str) -> str:
    """
    Generates a barcode with the format (product_id)(month)(day)(4-digit counter).

    Args:
        product_id (str): The product ID in the format "PROXXXXXXX" (e.g., "PRO1711240001").
        counter (int): The counter value for the barcode.

    Returns:
        str: The generated barcode in the specified format.

    Example:
        For product_id="PRO1711240001", counter=12 on Nov 18:
        Output: "171124000111180012"
    """
    # Extract the numeric part of the product_id
    numeric_product_id = product_id[3:]  # Remove the "PRO" prefix

    # Get the current date
    current_date = datetime.date.today()
    month = current_date.strftime("%m")  # Extract month as two digits
    day = current_date.strftime("%d")  # Extract day as two digits

    # Ensure the counter is 4 digits with leading zeros
    formatted_counter = str(12).zfill(4)

    # Combine all parts to create the barcode
    barcode = f"{numeric_product_id}{month}{day}{formatted_counter}"
    return barcode
