from enum import Enum

# Pydantic Import
from pydantic import (
    BaseModel,
    Field,
    FilePath,
)


class ErrorType(str, Enum):
    WARNING = "warning"
    ERROR = "error"


#
class ResponseClient(str, Enum):
    DEVELOPER = "developer"
    USER = "user"


# * <<----------------------------*** Response Class For Success ***--------------------------------->>
class SuccessResponse(BaseModel):
    """
    Represents a structured response for successful operations.
    """

    status: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Detailed error message")
    client: ResponseClient = Field(..., description="Client of the message")
    data: list | dict | None = Field(
        None,
        description="Additional information about the error",
    )
    links: dict | None = Field(
        default={"url": "https://www.example.com"},  # Example dictionary
        description="Quick access links for the next",
    )


# * <<--------------------------*** Response Class For Update ***------------------------------------------->>
class UpdateResponse(BaseModel):
    """
    Represents a structured response for updating operations.
    """

    status: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Detailed error message")
    client: ResponseClient = Field(..., description="Client of the message")
    details: dict | None = Field(
        None,
        description="Additional information about success",
    )
    links: dict | None = Field(
        default={"url": "https://www.care-box.com"},  # Example dictionary
        description="Quick access links for the next",
    )


# * <<-----------------------------*** Response Class For Error ***----------------------------------------->>
class ErrorResponse(BaseModel):
    """
    Represents a structured response for error operations.
    """

    status: int = Field(..., description="HTTP status code")
    type: ErrorType = Field(..., description="Error code indicating the type of error")
    message: str = Field(..., description="Detailed error message")
    client: ResponseClient = Field(..., description="Client error type")
    description: dict | None = Field(
        None,
        description="Additional information about the error",
    )


# * <<-----------------------------*** Response Class For No content ***------------------------------>>
class NoContentResponse(BaseModel):
    """
    Represents a structured response for successful deletion.
    This response is returned when a resource has been deleted successfully.
    """

    status: int = Field(204, description="HTTP status code for successful deletion")
    alternate_status: int = Field(200, description="HTTP status code")
    message: str = Field(
        "Resource deleted successfully",
        description="Confirmation message for deletion",
    )
    client: ResponseClient = Field(..., description="Client of the message")
    description: dict | None = Field(
        None,
        description="Additional information about delete operation",
    )


# * <<-----------------------------*** Response Class For Invalid Url ***--------------------------------->>
class InvalidUrlResponse(BaseModel):
    """
    Represents a structured response for invalid URLs.
    """

    status: int = Field(404, description="HTTP status code for successful deletion")
    message: str = Field(
        "404 Page Not Found",
        description="Message for page not found",
    )
    client: ResponseClient = Field(..., description="Client of the message")
    description: dict | None = Field(
        None,
        description="Additional information about invalid page url",
    )


# * <<-------------------------*** Response Class For File Upload ***------------------------------>>
class FileUploadResponse(BaseModel):
    """
    Represents a structured response for file uploads.
    """

    file: FilePath = Field(..., description="Path to the uploaded file")
