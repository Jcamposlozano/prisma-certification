from pydantic import BaseModel, Field


class GenerateSignatureRequest(BaseModel):
    name: str = Field(..., min_length=1)
    title: str = Field(default="")
    phone: str = Field(default="")
    email: str | None = None
    address: str = Field(default="")


class GenerateSignatureResponse(BaseModel):
    html: str
