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