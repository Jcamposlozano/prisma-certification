from pydantic import BaseModel, Field
from typing import Dict, Any


class GenerateCertificateRequest(BaseModel):
    institution_id: str = Field(..., min_length=1)
    template_id: str = Field(..., min_length=1)
    data: Dict[str, Any]