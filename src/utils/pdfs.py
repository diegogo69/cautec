import pdfkit
import jinja2
import platform
from pathlib import Path


def crear_pdf(data_template, ruta_template, ruta_css, ruta_pdf=None):
    Path_template = Path(ruta_template)
    Path_css = Path(ruta_css)
    nombre_template = Path_template.name
    carpeta_template = Path_template.parent
    
    print('-------------------------------------------------')
    print(data_template)
    print('-------------------------------------------------')
    # Generar rutas de archivo acorde al sistema operativo del servidor
    # Se utilizan rutas genéricas para Windows y Linux
    # Obtener la ruta de wkhtmltopdf con el siguiente comando:
    # windows: where wkhtmltopdf
    # linux: which wkhtmltopdf
    nombre_sistema_operativo = platform.system()

    # Get the file name 
    if nombre_sistema_operativo == 'Windows':
        ruta_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    else:
        ruta_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
    

    env_template = jinja2.Environment(loader=jinja2.FileSystemLoader(carpeta_template))
    template = env_template.get_template(nombre_template)
    html_string = template.render(data_template)
    print('------------------- HTML String ------------------------------')
    # print(html_string)
    print('-------------------------------------------------')

    # from version 0.12.6 wkhtmltopdf disables local file access by default
    # use 'enable-local-file-access' option to allow local images being rendered in the pdf  
    options = {
        "page-size": "letter",
        "margin-bottom": "2cm",
        "margin-left": "2cm",
        "margin-right": "2cm",
        "margin-top": "2cm",
        # "margin-top": "4cm",
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
    }
    
    config = pdfkit.configuration(wkhtmltopdf = ruta_wkhtmltopdf)

    pdf = pdfkit.from_string(
        html_string,
        output_path=Path(ruta_pdf) if ruta_pdf else None,
        options=options,
        css=Path_css,
        configuration=config,
        verbose=True, # Get output hints for debugging
    )

    return pdf

if __name__ == "__main__":
    ruta_file = Path(__file__)
    ruta_src = ruta_file.parent.parent
    ruta_template = ruta_src / 'templates' / 'pdfs' / 'solicitud_de_servicio.html'
    ruta_css = ruta_src / 'static' / 'css' / 'pdfs' / 'solicitud_de_servicio.css'
    ruta_pdf = ruta_src.parent / 'Nota_de_servicio.pdf'
    data = {}
    crear_pdf(data, ruta_template, ruta_css, ruta_pdf)