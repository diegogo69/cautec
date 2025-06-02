import pdfkit
import jinja2
import platform


def crear_pdf(data_template, ruta_template, ruta_css, ruta_pdf=None):

    # Generar rutas de archivo acorde al sistema operativo del servidor
    # Se utilizan rutas genéricas para Windows y Linux
    # Obtén la ruta de wkhtmltopdf con el siguiente comando:
    # windows: where wkhtmltopdf
    # linux: which wkhtmltopdf
    nombre_sistema_operativo = platform.system()

    if nombre_sistema_operativo == 'Windows':
        nombre_template = ruta_template.split("\\")[-1]
        ruta_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    else:
        nombre_template = ruta_template.split("/")[-1]
        ruta_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
        
    carpeta_template = ruta_template.replace(nombre_template, "")

    env_template = jinja2.Environment(loader=jinja2.FileSystemLoader(carpeta_template))
    template = env_template.get_template(nombre_template)
    html_string = template.render(data_template)

    # from version 0.12.6 wkhtmltopdf disables local file access by default
    # use 'enable-local-file-access' option to allow local images being rendered in the pdf  
    options = {
        "page-size": "letter",
        "margin-bottom": "3cm",
        "margin-left": "3cm",
        "margin-right": "3cm",
        "margin-top": "4cm",
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
    }
    
    config = pdfkit.configuration(wkhtmltopdf = ruta_wkhtmltopdf)

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
    pdf = '/home/diego/repos/cautec/Nota_de_servico.pdf'
    # pdf = None
    crear_pdf(data, template, css, pdf)