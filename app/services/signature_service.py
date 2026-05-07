import mimetypes
from copy import deepcopy

from app.utils.file_utils import bytes_to_data_uri


class SignatureService:
    """Renderiza la firma corporativa Westfield con assets ya embebidos
    como data URIs (compatible con Gmail sin hosting externo)."""

    def __init__(self, repository, render_service, prefix: str):
        self.repository = repository
        self.render_service = render_service
        self.prefix = prefix

    def render_html(self, form_data: dict) -> str:
        config = self.repository.get_config(self.prefix)

        required_fields = config.get("required_fields", [])
        missing = [f for f in required_fields if not form_data.get(f)]
        if missing:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing)}")

        html_file = config.get("html_file", "template.html")
        assets = config.get("assets", {})
        defaults = deepcopy(config.get("defaults", {}))

        html_template = self.repository.get_html(self.prefix, html_file)

        asset_context: dict[str, str | None] = {}
        for field_name, asset_path in assets.items():
            try:
                asset_bytes = self.repository.get_asset_bytes(self.prefix, asset_path)
                mime, _ = mimetypes.guess_type(asset_path)
                asset_context[field_name] = bytes_to_data_uri(
                    asset_bytes, mime_type=mime or "image/png"
                )
            except Exception:
                asset_context[field_name] = None

        context = {
            **defaults,
            **asset_context,
            **form_data,
        }

        return self.render_service.render(html_template=html_template, context=context)
