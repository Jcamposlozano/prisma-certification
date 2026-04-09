from pydantic import BaseModel
from typing import List, Optional, Any


class TemplateCatalogItem(BaseModel):
    id: str
    label: str
    description: Optional[str] = None


class InstitutionCatalogItem(BaseModel):
    id: str
    label: str
    templates: List[TemplateCatalogItem]


class CertificatesCatalogResponse(BaseModel):
    institutions: List[InstitutionCatalogItem]


class FormFieldResponse(BaseModel):
    key: str
    label: str
    type: str
    required: bool = False
    placeholder: Optional[str] = None
    order: Optional[int] = None
    options: Optional[List[Any]] = None


class FormDefinitionResponse(BaseModel):
    fields: List[FormFieldResponse]


class CertificateCatalogDetailResponse(BaseModel):
    institution_id: str
    template_id: str
    label: str
    description: Optional[str] = None
    required_fields: List[str]
    defaults: dict
    form: FormDefinitionResponse