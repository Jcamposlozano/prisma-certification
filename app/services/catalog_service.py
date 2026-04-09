from app.schemas.catalog import (
    CertificatesCatalogResponse,
    InstitutionCatalogItem,
    TemplateCatalogItem,
    CertificateCatalogDetailResponse,
    FormDefinitionResponse,
    FormFieldResponse,
)


class CatalogService:
    def __init__(self, template_repository):
        self.template_repository = template_repository

    @staticmethod
    def _prettify_label(raw_value: str) -> str:
        return raw_value.replace("-", " ").replace("_", " ").title()

    def get_catalog(self) -> CertificatesCatalogResponse:
        keys = self.template_repository.list_keys(prefix="institutions/")

        institutions_map: dict[str, dict] = {}

        for key in keys:
            parts = key.split("/")

            if len(parts) < 5:
                continue

            if parts[0] != "institutions":
                continue

            institution_id = parts[1]

            if parts[2] != "templates":
                continue

            template_id = parts[3]

            institutions_map.setdefault(
                institution_id,
                {
                    "id": institution_id,
                    "label": self._prettify_label(institution_id),
                    "templates": {},
                },
            )

            institutions_map[institution_id]["templates"].setdefault(
                template_id,
                {
                    "id": template_id,
                    "label": self._prettify_label(template_id),
                    "description": None,
                },
            )

        institutions_output: list[InstitutionCatalogItem] = []

        for institution_id, institution_data in sorted(institutions_map.items()):
            templates_output: list[TemplateCatalogItem] = []

            for template_id, template_data in sorted(institution_data["templates"].items()):
                try:
                    config = self.template_repository.get_template_config(
                        institution_id=institution_id,
                        template_id=template_id,
                    )

                    template_label = config.get("label") or template_data["label"]
                    template_description = config.get("description")

                except Exception:
                    template_label = template_data["label"]
                    template_description = None

                templates_output.append(
                    TemplateCatalogItem(
                        id=template_id,
                        label=template_label,
                        description=template_description,
                    )
                )

            institutions_output.append(
                InstitutionCatalogItem(
                    id=institution_id,
                    label=institution_data["label"],
                    templates=templates_output,
                )
            )

        return CertificatesCatalogResponse(institutions=institutions_output)

    def get_template_detail(
        self,
        institution_id: str,
        template_id: str,
    ) -> CertificateCatalogDetailResponse:
        config = self.template_repository.get_template_config(
            institution_id=institution_id,
            template_id=template_id,
        )

        form_config = config.get("form", {})
        fields_config = form_config.get("fields", [])

        fields = [
            FormFieldResponse(
                key=field["key"],
                label=field.get("label", self._prettify_label(field["key"])),
                type=field.get("type", "text"),
                required=field.get("required", False),
                placeholder=field.get("placeholder"),
                order=field.get("order"),
                options=field.get("options"),
            )
            for field in fields_config
        ]

        fields = sorted(fields, key=lambda f: f.order if f.order is not None else 9999)

        return CertificateCatalogDetailResponse(
            institution_id=institution_id,
            template_id=template_id,
            label=config.get("label", self._prettify_label(template_id)),
            description=config.get("description"),
            required_fields=config.get("required_fields", []),
            defaults=config.get("defaults", {}),
            form=FormDefinitionResponse(fields=fields),
        )
        keys = self.template_repository.list_keys(prefix="institutions/")

        institutions_map: dict[str, dict] = {}

        for key in keys:
            parts = key.split("/")

            # Esperamos estructura:
            # institutions/{institution_id}/templates/{template_id}/...
            if len(parts) < 5:
                continue

            if parts[0] != "institutions":
                continue

            institution_id = parts[1]

            if parts[2] != "templates":
                continue

            template_id = parts[3]

            institutions_map.setdefault(
                institution_id,
                {
                    "id": institution_id,
                    "label": self._prettify_label(institution_id),
                    "templates": {},
                },
            )

            institutions_map[institution_id]["templates"].setdefault(
                template_id,
                {
                    "id": template_id,
                    "label": self._prettify_label(template_id),
                    "description": None,
                },
            )

        institutions_output: list[InstitutionCatalogItem] = []

        for institution_id, institution_data in sorted(institutions_map.items()):
            templates_output: list[TemplateCatalogItem] = []

            for template_id, template_data in sorted(institution_data["templates"].items()):
                try:
                    config = self.template_repository.get_template_config(
                        institution_id=institution_id,
                        template_id=template_id,
                    )

                    template_label = config.get("label") or template_data["label"]
                    template_description = config.get("description")

                except Exception:
                    template_label = template_data["label"]
                    template_description = None

                templates_output.append(
                    TemplateCatalogItem(
                        id=template_id,
                        label=template_label,
                        description=template_description,
                    )
                )

            institutions_output.append(
                InstitutionCatalogItem(
                    id=institution_id,
                    label=institution_data["label"],
                    templates=templates_output,
                )
            )

        return CertificatesCatalogResponse(institutions=institutions_output)