# Recomendaciones para el proceso de desarrollo

## Verificar el entorno de desarrollo (virtual o global)
Al iniciar el editor, verica el entorno de desarrollo actual de la terminal. Siempre es recomendable trabajar con entornos virtuales especificos para cada proyecto.

### Verificar directorio
**pwd:** verifica la ruta del directorio actual
**pip list:** lista los paquetes instalados en el entorno actual. Verifica que concuerden con el entorno del proyecto

### Comprobar entorno virtual
`. .venv/bin/activate` activa el entorno virtual  
`deactivate` desactiva el entorno virtual  


## El orden de los Imports importa
Cuando el interprete encuentra un import, el contexto de ejecución cambia al de archivo que está siendo importado y todo su contenido ejecuta, si se encuentra un import allí, el proceso se repite. Por lo que se puede dar el caso de importar de un modulo parcialmente inicializado. Esto generalmente sucede al querer colocar los imports al principio del archivo. Para importar una variable de un modula, esta variable debe haber sido inicializada en el contexto de ejecucion.

## Recuperar archivo de un commit anterior
git checkout *commit_hash* -- *ruta/del/archivo*

## Object.keys, values, items to iterate objects
Verificar si el objeto está vacío Object.keys(deps_json).length === 0

## Usando enumerate()
Iterar sobre los elementos de una lista y sus indices, utilizando la funcion de python enumerate.

for index, item in enumerate(list, start=0)

el parametro start indica a partir de qué número se comienza a contar.

mas legible que for index in range(len(list))

## Using functions within templates
Functions can be pass to templates just as with variables, using render template, and be called within it using jinja syntax

Like with enumerate in crear-reporte.html. Enumerate being the built-in python function.

render_template('template.html', enumerate=enumerate)

Another approach would be to make the function global to all jinja templates using context_processor decorator

@app.context_processor
def fn_available(_in_all_templates)


## List comprehensions
List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list.
The iterable can be any iterable object, like a list, tuple, set etc. 

newlist = [expression for item in iterable if condition == True]

The condition is optional and can be omitted:

newlist = [x for x in fruits]

The expression is the current item in the iteration, but it is also the outcome, which you can manipulate before it ends up like a list item in the new list:

newlist = [x.upper() for x in fruits]

The expression can also contain conditions, not like a filter, but as a way to manipulate the outcome:

newlist = [x if x != "banana" else "orange" for x in fruits]