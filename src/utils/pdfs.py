import pdfkit
import jinja2

def crear_pdf(data, ruta_template, ruta_css, ruta_pdf=None):
    nombre_template = ruta_template.split("/")[-1]
    carpeta_template = ruta_template.replace(nombre_template, "")

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(carpeta_template))
    template = env.get_template(nombre_template)
    html_string = template.render(data)

    # from version 0.12.6 wkhtmltopdf disables local file access by default
    # use 'enable-local-file-access' option to allow local images being rendered in the pdf  
    options = {
        "page-size": "letter",
        "margin-bottom": "3cm",
        "margin-left": "3cm",
        "margin-right": "3cm",
        "margin-top": "4cm",
        'encoding': 'UTF-8',
        'enable-local-file-access': '',
    }

    # obtén la ruta de wkhtmltopdf con el siguiente comando:
    # linux | which wkhtmltopdf
    # windows | where wkhtmltopdf 
    ruta_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
    # config = pdfkit.configuration() # By default pdfkit will attempt to locate this using which

    # Also you can pass an opened file:
    # with open('file.html') as f:
        # pdfkit.from_file(f, 'out.pdf')

    # If you wish to further process generated PDF, you can read it to a variable:
    # Without output_path, PDF is returned for assigning to a variable
    # pdf = pdfkit.from_url('http://google.com')

    pdf = pdfkit.from_string(
        html_string,
        output_path=ruta_pdf,
        options=options,
        css=ruta_css,
        configuration=config,
        verbose=True, # Get output hints for debugging
    )

    return pdf

if __name__ == "__main__":
    template = '/home/diego/repos/cautec/src/templates/pdfs/solicitud_de_servicio.html'
    data = {}
    css = '/home/diego/repos/cautec/src/static/css/pdfs/solicitud_de_servicio.css'
    # pdf = '/home/diego/repos/cautec/Nota_de_servico.pdf'
    pdf = None
    crear_pdf(data, template, css, pdf)