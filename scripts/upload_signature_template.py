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

import boto3

from app.core.config import settings

LOCAL_ROOT = Path(__file__).parent / "signature_template"


def upload() -> int:
    if not settings.S3_SIGNATURE_BUCKET_NAME:
        print("ERROR: S3_SIGNATURE_BUCKET_NAME no está configurado en .env")
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
    bucket = settings.S3_SIGNATURE_BUCKET_NAME

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
