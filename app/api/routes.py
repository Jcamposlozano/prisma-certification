from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.core.config import settings
from app.schemas.certificate import GenerateCertificateRequest
from app.schemas.catalog import (
    CertificatesCatalogResponse,
    CertificateCatalogDetailResponse,
)
from app.repositories.template_repository import TemplateRepository
from app.services.template_render_service import TemplateRenderService
from app.services.template_validator import TemplateValidationError
from app.services.certificate_service import CertificateService
from app.services.pdf_service import PdfService
from app.services.catalog_service import CatalogService

router = APIRouter()

template_repository = TemplateRepository(
    bucket_name=settings.S3_BUCKET_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_DEFAULT_REGION,
)

render_service = TemplateRenderService()
pdf_service = PdfService()

certificate_service = CertificateService(
    template_repository=template_repository,
    render_service=render_service,
    pdf_service=pdf_service,
)

catalog_service = CatalogService(template_repository)


@router.get("/v1/certificates/catalog", response_model=CertificatesCatalogResponse)
def get_certificates_catalog():
    try:
        return catalog_service.get_catalog()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/v1/certificates/catalog/{institution_id}/{template_id}",
    response_model=CertificateCatalogDetailResponse,
)
def get_certificate_template_detail(institution_id: str, template_id: str):
    try:
        return catalog_service.get_template_detail(
            institution_id=institution_id,
            template_id=template_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v1/certificates/generate")
def generate_certificate(request: GenerateCertificateRequest):
    try:
        pdf_bytes = certificate_service.generate_pdf(
            institution_id=request.institution_id,
            template_id=request.template_id,
            request_data=request.data,
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=certificate.pdf"},
        )

    except TemplateValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))