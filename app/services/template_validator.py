class TemplateValidationError(Exception):
    pass


def validate_required_fields(required_fields: list[str], data: dict) -> None:
    missing = [
        field for field in required_fields
        if field not in data or data[field] in (None, "")
    ]

    if missing:
        raise TemplateValidationError(
            f"Missing required fields: {', '.join(missing)}"
        )