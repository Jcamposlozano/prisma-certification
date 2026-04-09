from jinja2 import Template


class TemplateRenderService:
    def render(self, html_template: str, context: dict) -> str:
        template = Template(html_template)
        return template.render(**context)