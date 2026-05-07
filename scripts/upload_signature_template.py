"""Sube la plantilla de firma Westfield (config + html + assets) al bucket
dedicado de firmas.

Uso:
    poetry run python scripts/upload_signature_template.py

Lee credenciales y bucket de las variables de entorno (.env). Espera la
estructura local en scripts/signature_template/.

El bucket queda con el layout:
    {SIGNATURE_TEMPLATE_PREFIX}/config.json
    {SIGNATURE_TEMPLATE_PREFIX}/template.html
    {SIGNATURE_TEMPLATE_PREFIX}/assets/<archivos>
"""

from __future__ import annotations

import mimetypes
import sys
from pathlib import Path

# Permite ejecutar el script directamente (poetry run python scripts/...)
# sin que falle el import de app.* — añadimos la raíz del proyecto a sys.path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import boto3  # noqa: E402

from app.core.config import settings  # noqa: E402

LOCAL_ROOT = Path(__file__).parent / "signature_template"


def upload() -> int:
    bucket = settings.S3_SIGNATURE_BUCKET_NAME or settings.S3_BUCKET_NAME
    if not bucket:
        print("ERROR: S3_BUCKET_NAME (o S3_SIGNATURE_BUCKET_NAME) no está configurado en .env")
        return 1

    if not LOCAL_ROOT.is_dir():
        print(f"ERROR: no existe la carpeta local {LOCAL_ROOT}")
        return 1

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION,
    )

    prefix = settings.SIGNATURE_TEMPLATE_PREFIX.strip("/")

    uploaded = 0
    for path in LOCAL_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(LOCAL_ROOT).as_posix()
        key = f"{prefix}/{rel}"
        mime, _ = mimetypes.guess_type(path.name)
        extra = {"ContentType": mime} if mime else {}
        s3.upload_file(str(path), bucket, key, ExtraArgs=extra)
        print(f"  ↑ s3://{bucket}/{key}")
        uploaded += 1

    print(f"\nSubidos {uploaded} archivos al bucket de firmas.")
    return 0


if __name__ == "__main__":
    sys.exit(upload())
