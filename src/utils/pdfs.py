import pdfkit
import jinja2

def crear_pdf(data, ruta_template, ruta_css, ruta_pdf):
    nombre_template = ruta_template.split("/")[-1]
    carpeta_template = ruta_template.replace(nombre_template, "")

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(carpeta_template))
    template = env.get_template(nombre_template)
    html_string = template.render(data)

    options = {
        "page-size": "letter",
        "margin-bottom": "3cm",
        "margin-left": "3cm",
        "margin-right": "3cm",
        "margin-top": "4cm",
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
    }

    ruta_wkhtmltopdf = '/usr/bin/wkhtmltopdf' # get by which wkhtmltopdf 
    config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
    # config = pdfkit.configuration() # By default pdfkit will attempt to locate this using which

    pdfkit.from_string(
        html_string,
        ruta_pdf,
        options=options,
        css=ruta_css,
        configuration=config,
    )

if __name__ == "__main__":
    template = '/home/diego/repos/cautec/src/templates/pdfs/solicitud_de_servicio.html'
    data = {}
    css = '/home/diego/repos/cautec/src/static/css/pdfs/solicitud_de_servicio.css'
    pdf = '/home/diego/repos/cautec/Nota_de_servico.pdf'
    crear_pdf(data, template, css, pdf)