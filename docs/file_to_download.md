# Generando descargas de archivos en flask

Tres métodos se pueden utilizar para enviar un archivo del servidor al cliente como descarga, aunque en realidad son dos

## Usando send_file

El método send_file de flask está diseñado especialmente para este tipo de tareas. Gestionar de forma optimizada el envío de archivos del servidor al cliente como descarga. Es un método semántico, directo y optimizado para la tarea.

Sin embargo hay un factor que me hace dudar al momento de decidir si usarlo o no, puesto que en el caso de mi aplicación, el archivo de a descargar, no es un archivo local, guardado en el sistema de archivos del servidor; sino archivo en memoria, generado por método `pdfkit.fromstring()`, que devuelve un objeto de tipo archivo, que es una instancia de la clase '_bytes_'. Pero `send_file` recibe un objeto de instancia '_bytesIO_', es decir, en modo binario. Por lo que es necesario generar un archivo binario en memoria con `io.BytesIO()`. Un paso extra en la ecuación.

```
pdf = pdfkit.fromstring()
pdf_buffer = io.BytesIO(pdf)
print(type(pdf)) # <class 'bytes'>
print(type(pdf_buffer)) # <class '_io.BytesIO'>
```

### Ejemplo:

```
return send_file(
    pdf_buffer,
    download_name = 'descarga.pdf',
    # mimetype = 'application/pdf'
    # as_attachment = True, # Ofrecer descargar en vez de mostrar archivo
)
```

**mimetype**: indica el tipo de archivo enviado en el Response, es opcional, si no se se indica la función lo determina desde el mismo archivo.

**as_attachment**: indica al navegador si debe ofrecer descargar el archivo o mostrarlo dentro del navegador

## Usando make_response

According to flask documentation on Response.response:
Do not set to a plain string or bytes, that will cause
sending the response to be very inefficient
as it will iterate one byte at a time.

Según lo que entiendo, dice que no haga exactamente lo que este método hace, pasar un objecto de tipo _bytes_ como el contenido del response.

Mencionaba que en realidad eran 2 métodos y no dos, pues ambos se basan crear un objeto de tipo Response, y en vez de utilizar la clase Response directamente, que es una posibilidad, el método make_response está diseñado exactamente para eso. Creando un objeto Response con los bytes pasados como argumento como su contenido, al cuál se le pueden añadir header adicionales

### Ejemplo Response

```
headers = {
    'Content-Type': 'application/pdf',
    'Content-Disposition': f"attachment;filename='descarga.pdf'"
}
response = Response(pdf, headers=headers)
return response
```

### Ejemplo make_response

```
nombre_pdf = 'descarga_pdf_make_response.pdf'
response = make_response(pdf)
response.headers["Content-Type"] = "application/pdf"
response.headers["Content-Disposition"] = f"attachment;filename='descarga.pdf'"
return response
```

**attachment** sigue siendo un argumento opcional.

## Conclusión

Usando send_file es necesario utilizar BytesIO sobre pdf; mientras que al usar Response o make_response no es necesario.
send_file me parece más directo y semántico, sin embargo necesita ese paso extra.
