from copy import deepcopy

from app.utils.file_utils import bytes_to_data_uri
from app.services.template_validator import validate_required_fields


class CertificateService:
    def __init__(self, template_repository, render_service, pdf_service=None):
        self.template_repository = template_repository
        self.render_service = render_service
        self.pdf_service = pdf_service

    def build_context(self, institution_id: str, template_id: str, request_data: dict) -> dict:
        config = self.template_repository.get_template_config(institution_id, template_id)

        required_fields = config.get("required_fields", [])
        validate_required_fields(required_fields, request_data)

        html_file = config.get("html_file", "template.html")
        css_file = config.get("css_file", "styles.css")
        assets = config.get("assets", {})
        defaults = deepcopy(config.get("defaults", {}))

        html_content = self.template_repository.get_template_html(
            institution_id, template_id, html_file
        )
        css_content = self.template_repository.get_template_css(
            institution_id, template_id, css_file
        )

        asset_context = {}
        for field_name, asset_path in assets.items():
            try:
                asset_bytes = self.template_repository.get_asset_bytes(
                    institution_id, template_id, asset_path
                )
                asset_context[field_name] = bytes_to_data_uri(asset_bytes)
            except Exception:
                asset_context[field_name] = None

        context = {
            **defaults,
            **asset_context,
            **request_data,
            "css_content": css_content,
        }

        return {
            "html_content": html_content,
            "context": context,
        }

    def render_html(self, institution_id: str, template_id: str, request_data: dict) -> str:
        payload = self.build_context(institution_id, template_id, request_data)

        return self.render_service.render(
            html_template=payload["html_content"],
            context=payload["context"],
        )

    def generate_pdf(self, institution_id: str, template_id: str, request_data: dict) -> bytes:
        if self.pdf_service is None:
            raise ValueError("PdfService no está configurado")

        html = self.render_html(
            institution_id=institution_id,
            template_id=template_id,
            request_data=request_data,
        )

        return self.pdf_service.generate_pdf_bytes(html)