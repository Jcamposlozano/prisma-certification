from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.repositories.signature_repository import SignatureRepository
from app.schemas.signature import GenerateSignatureRequest, GenerateSignatureResponse
from app.services.signature_service import SignatureService
from app.services.template_render_service import TemplateRenderService

router = APIRouter(prefix="/signatures", tags=["signatures"])

_signature_repository: SignatureRepository | None = None
_signature_service: SignatureService | None = None


def _get_signature_service() -> SignatureService:
    global _signature_repository, _signature_service

    if _signature_service is not None:
        return _signature_service

    if not settings.S3_SIGNATURE_BUCKET_NAME:
        raise HTTPException(
            status_code=500,
            detail="S3_SIGNATURE_BUCKET_NAME no está configurado",
        )

    _signature_repository = SignatureRepository(
        bucket_name=settings.S3_SIGNATURE_BUCKET_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION,
    )
    _signature_service = SignatureService(
        repository=_signature_repository,
        render_service=TemplateRenderService(),
        prefix=settings.SIGNATURE_TEMPLATE_PREFIX,
    )
    return _signature_service


@router.post("/v1/generate", response_model=GenerateSignatureResponse)
def generate_signature(request: GenerateSignatureRequest):
    service = _get_signature_service()
    try:
        html = service.render_html(request.model_dump())
        return GenerateSignatureResponse(html=html)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
