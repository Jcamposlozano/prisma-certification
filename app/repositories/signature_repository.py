import json

import boto3


class SignatureRepository:
    """Repositorio dedicado al bucket de firmas. No comparte ruta con
    certificados — el bucket es exclusivo para este ejercicio."""

    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        region_name: str | None = None,
    ):
        self.bucket_name = bucket_name

        client_kwargs = {}
        if aws_access_key_id:
            client_kwargs["aws_access_key_id"] = aws_access_key_id
        if aws_secret_access_key:
            client_kwargs["aws_secret_access_key"] = aws_secret_access_key
        if region_name:
            client_kwargs["region_name"] = region_name

        self.s3 = boto3.client("s3", **client_kwargs)

    def _read_text(self, key: str) -> str:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return response["Body"].read().decode("utf-8")

    def _read_bytes(self, key: str) -> bytes:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return response["Body"].read()

    def get_config(self, prefix: str) -> dict:
        return json.loads(self._read_text(f"{prefix}/config.json"))

    def get_html(self, prefix: str, html_file: str) -> str:
        return self._read_text(f"{prefix}/{html_file}")

    def get_asset_bytes(self, prefix: str, asset_path: str) -> bytes:
        return self._read_bytes(f"{prefix}/{asset_path}")
