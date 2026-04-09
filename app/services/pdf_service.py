from weasyprint import HTML


class PdfService:
    def generate_pdf_bytes(self, html_content: str) -> bytes:
        return HTML(string=html_content).write_pdf()