# Plantilla de firma Westfield

Archivos que viven en el bucket dedicado a firmas (`S3_SIGNATURE_BUCKET_NAME`),
bajo el prefijo `SIGNATURE_TEMPLATE_PREFIX` (default `westfield`).

## Layout esperado en el bucket

```
{prefix}/
  config.json
  template.html
  assets/
    background-left.png
    background-right.png
    icon-linkedin.png
    icon-instagram.png
    icon-facebook.png
    icon-youtube.png
```

## Cómo subirlo

1. Coloca los assets reales en `scripts/signature_template/assets/`. El layout
   parte el background de 560x160 en dos mitades:
   - `background-left.png` → 310x160 (lado izquierdo, logo)
   - `background-right.png` → 250x160 (lado derecho, datos)

   Genera ambas a partir del `Background.png` original (slicing 1:1 sin
   reescalar, igual que el JS hacía con canvas).

2. Configura `.env` con `S3_SIGNATURE_BUCKET_NAME` y credenciales AWS.

3. Ejecuta:
   ```bash
   poetry run python scripts/upload_signature_template.py
   ```

## Editar el HTML

Modifica `template.html` (Jinja2). Variables disponibles:

- `name`, `title`, `phone`, `email`, `address` — del formulario
- `img_background_left`, `img_background_right`, `img_linkedin`,
  `img_instagram`, `img_facebook`, `img_youtube` — assets como data URI
- `url_linkedin`, `url_instagram`, `url_facebook`, `url_youtube` — definidas
  en `config.json > defaults`
