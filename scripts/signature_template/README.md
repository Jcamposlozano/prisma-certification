# Plantilla de firma Westfield

Archivos que viven en S3 bajo `s3://{S3_BUCKET_NAME}/{SIGNATURE_TEMPLATE_PREFIX}/`.

Por defecto: `s3://prisma-certification/firmas_institucionales/westfield/`.

## Layout en el bucket (4 partes)

```
{prefix}/
  template.html        Plantilla Jinja del HTML compatible con Gmail
  styles.css           CSS auxiliar (inyectado en <style>)
  config.json          Required fields, mapping de assets, URLs por defecto
  assets/
    Background.png     Original — el backend lo recorta en runtime con Pillow
    icon-linkedin.png
    icon-instagram.png
    icon-facebook.png
    icon-youtube.png
```

## Cómo subirlo

1. Asegúrate de tener los archivos en `scripts/signature_template/`
   (este directorio).
2. Configura `.env` con `S3_BUCKET_NAME=prisma-certification` (o el bucket
   que uses), `SIGNATURE_TEMPLATE_PREFIX=firmas_institucionales/westfield` y
   credenciales `AWS_*`.
3. Ejecuta:
   ```bash
   poetry run python scripts/upload_signature_template.py
   ```

El script sube todo el árbol bajo `scripts/signature_template/` al prefix
configurado.

## Cómo funciona en runtime

- `POST /signatures/v1/generate` recibe `{name, title, phone, email, address}`.
- `SignatureService` lee `config.json`, `template.html`, `styles.css` y los
  assets desde S3.
- Recorta `Background.png` con cover-fit 560×160 y lo divide en dos mitades
  (310×160 + 250×160) replicando la lógica del JS original (Pillow + LANCZOS).
- Embebe todas las imágenes como `data:image/png;base64,...` para que Gmail
  las renderice sin hosting externo.
- Renderiza la plantilla Jinja con CSS, imágenes y datos del formulario.

## Variables disponibles en `template.html`

Del formulario (Pydantic schema): `name`, `title`, `phone`, `email`,
`address`.

Generadas por el service:
- `img_background` — data URI del background original (sin recortar).
- `img_background_left` — data URI de la mitad izquierda (310×160).
- `img_background_right` — data URI de la mitad derecha (250×160).
- `img_linkedin`, `img_instagram`, `img_facebook`, `img_youtube` — íconos.
- `css_content` — contenido de `styles.css`.

Desde `config.json > defaults`:
- `url_linkedin`, `url_instagram`, `url_facebook`, `url_youtube`.
