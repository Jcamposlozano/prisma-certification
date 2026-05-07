import mimetypes
from copy import deepcopy
from io import BytesIO

from PIL import Image

from app.utils.file_utils import bytes_to_data_uri


# Dimensiones de la firma de correo (replican el JS original).
SIG_WIDTH = 560
SIG_HEIGHT = 160
LEFT_WIDTH = 310
RIGHT_WIDTH = SIG_WIDTH - LEFT_WIDTH
NAVY_RGBA = (1, 13, 38, 255)


class SignatureService:
    """Renderiza la firma corporativa Westfield embebiendo todos los assets
    como data URIs (compatible con Gmail sin hosting externo).

    Replica en Python la lógica original del HTML+JS de la carpeta firmas:
      - Carga template HTML, CSS y config.json desde S3
      - Carga el background y los íconos sociales desde assets/
      - Recorta el background con cover-fit centrado en 560x160 y lo divide
        en una mitad izquierda (310x160) y otra derecha (250x160)
      - Inyecta CSS y data URIs en el template y renderiza con Jinja
    """

    def __init__(self, repository, render_service, prefix: str):
        self.repository = repository
        self.render_service = render_service
        self.prefix = prefix.rstrip("/")

    def render_html(self, form_data: dict) -> str:
        config = self.repository.get_config(self.prefix)

        required_fields = config.get("required_fields", [])
        missing = [f for f in required_fields if not form_data.get(f)]
        if missing:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing)}")

        html_file = config.get("html_file", "template.html")
        css_file = config.get("css_file", "styles.css")
        assets = config.get("assets", {})
        background_field = config.get("background_field", "img_background")
        defaults = deepcopy(config.get("defaults", {}))

        html_template = self.repository.get_html(self.prefix, html_file)

        try:
            css_content = self.repository.get_css(self.prefix, css_file)
        except Exception:
            css_content = ""

        asset_context = self._load_assets(assets, background_field)

        context = {
            **defaults,
            **asset_context,
            **form_data,
            "css_content": css_content,
        }

        return self.render_service.render(html_template=html_template, context=context)

    # ---------- helpers ----------

    def _load_assets(
        self, assets: dict[str, str], background_field: str
    ) -> dict[str, str | None]:
        """Carga assets desde S3, hace slicing del background y devuelve un
        diccionario con data URIs listas para inyectar en el template."""
        ctx: dict[str, str | None] = {}

        for field_name, asset_path in assets.items():
            try:
                raw = self.repository.get_asset_bytes(self.prefix, asset_path)
            except Exception:
                ctx[field_name] = None
                continue

            if field_name == background_field:
                left_bytes, right_bytes = self._slice_background(raw)
                ctx[f"{field_name}_left"] = bytes_to_data_uri(left_bytes)
                ctx[f"{field_name}_right"] = bytes_to_data_uri(right_bytes)
                ctx[field_name] = bytes_to_data_uri(raw)
            else:
                mime, _ = mimetypes.guess_type(asset_path)
                ctx[field_name] = bytes_to_data_uri(raw, mime_type=mime or "image/png")

        return ctx

    @staticmethod
    def _slice_background(image_bytes: bytes) -> tuple[bytes, bytes]:
        """Replica la lógica de cropBackgroundSlices() del JS original:
        cover-fit del background a 560x160, centrado, y partido en dos
        mitades (310x160 + 250x160)."""
        img = Image.open(BytesIO(image_bytes)).convert("RGBA")

        scale = max(SIG_WIDTH / img.width, SIG_HEIGHT / img.height)
        draw_w = int(round(img.width * scale))
        draw_h = int(round(img.height * scale))
        offset_x = (SIG_WIDTH - draw_w) // 2
        offset_y = (SIG_HEIGHT - draw_h) // 2
        resized = img.resize((draw_w, draw_h), Image.LANCZOS)

        def make_slice(x: int, w: int) -> bytes:
            canvas = Image.new("RGBA", (w, SIG_HEIGHT), NAVY_RGBA)
            canvas.paste(resized, (offset_x - x, offset_y), resized)
            buf = BytesIO()
            canvas.save(buf, "PNG", optimize=True)
            return buf.getvalue()

        return make_slice(0, LEFT_WIDTH), make_slice(LEFT_WIDTH, RIGHT_WIDTH)
