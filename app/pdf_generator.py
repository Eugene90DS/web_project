
from jinja2 import Template
import pdfkit

def generate_pdf(payload):
    with open("templates/act_template.html", "r") as f:
        template = Template(f.read())
    html_content = template.render(payload=payload)
    output_path = f"/tmp/generated_act_{payload['order_id']}.pdf"
    pdfkit.from_string(html_content, output_path)
    return output_path
