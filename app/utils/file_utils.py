import base64


def bytes_to_data_uri(file_bytes: bytes, mime_type: str = "image/png") -> str:
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"