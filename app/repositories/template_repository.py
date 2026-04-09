import json
import boto3


class TemplateRepository:
    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        region_name: str | None = None,
        base_prefix: str = "institutions",
    ):
        self.bucket_name = bucket_name
        self.base_prefix = base_prefix

        client_kwargs = {}
        if aws_access_key_id:
            client_kwargs["aws_access_key_id"] = aws_access_key_id
        if aws_secret_access_key:
            client_kwargs["aws_secret_access_key"] = aws_secret_access_key
        if region_name:
            client_kwargs["region_name"] = region_name

        self.s3 = boto3.client("s3", **client_kwargs)

    def _read_text_file(self, key: str) -> str:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return response["Body"].read().decode("utf-8")

    def _read_binary_file(self, key: str) -> bytes:
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return response["Body"].read()

    def _build_prefix(self, institution_id: str, template_id: str) -> str:
        return f"{self.base_prefix}/{institution_id}/templates/{template_id}"

    def get_template_config(self, institution_id: str, template_id: str) -> dict:
        key = f"{self._build_prefix(institution_id, template_id)}/config.json"
        content = self._read_text_file(key)
        return json.loads(content)

    def get_template_html(self, institution_id: str, template_id: str, html_file: str) -> str:
        key = f"{self._build_prefix(institution_id, template_id)}/{html_file}"
        return self._read_text_file(key)

    def get_template_css(self, institution_id: str, template_id: str, css_file: str) -> str:
        key = f"{self._build_prefix(institution_id, template_id)}/{css_file}"
        return self._read_text_file(key)

    def get_asset_bytes(self, institution_id: str, template_id: str, asset_path: str) -> bytes:
        key = f"{self._build_prefix(institution_id, template_id)}/{asset_path}"
        return self._read_binary_file(key)

    def list_keys(self, prefix: str) -> list[str]:
        keys: list[str] = []
        continuation_token = None

        while True:
            kwargs = {
                "Bucket": self.bucket_name,
                "Prefix": prefix,
            }
            if continuation_token:
                kwargs["ContinuationToken"] = continuation_token

            response = self.s3.list_objects_v2(**kwargs)

            for obj in response.get("Contents", []):
                keys.append(obj["Key"])

            if response.get("IsTruncated"):
                continuation_token = response.get("NextContinuationToken")
            else:
                break

        return keys