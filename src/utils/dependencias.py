import json
import csv
import re

# ---------------------------------------------------------
# 1. DATOS DE ENTRADA
# ---------------------------------------------------------
RAW_MARKDOWN = """## Torre A

### Planta baja

Laboratorio demostrativo. Cood. Fran Daboin

Laboratorio de Fisica I y II

Laboratorio de Termodinámica

Oficina GRINCEF

Laboratorio de física

Sala de profesores

Laboratorio de Fisica I

### Piso 1

Laboratorio de Genética y microbiología

Laboratorio de Bioquímica

Laboratorio de biología animal y humana

Laboratorio de fisiología vegetal

Sala de secado

Sala de preparacion

Laboratorio de biología vegetal, botánica y morfoanatomía vegetal

### Piso 2

Laboratorio de Química orgánica

Laboratorio de quimica general

Sala de reactivos solidos

Sala de reactivos liquidos

Laboratorio de quimica analítica

Sala de estudio

Sala de preparacion de reactivos

Laboratorio de bioquimica

### Piso 3

Laboratorio de investigación de parásitos (LIEM)

Laboratorio de análisis instrumental

Laboratorio de quimica Ambiental

Laboratorio de productos naturales

## Torre B

### Planta baja

Aulas B0001-B008

### Piso 1

Aulas B1001-B108

### Piso 2

Aulas B2001-B208

### Piso 3

Aulas B3001-B308

## Torre C

### Planta baja

Oficina Area de mecánica, estructura y resistencia de materiales

Laboratorio de materiales y ensayos

Laboratorio de topografía

Oficina de Centro de copiado

Oficina de Proveduría y papelería

Oficina de DAES-NURR Departamento de asuntos estudiantiles

### Piso 1

Oficina de Centro de estudiantes CENURR

Sala de cine 

Laboratorio de Audiovisual

Oficina de APULA Asociación de profesores ULA

Oficina de UPP Instituto de prevision de profesorado de ula

### Piso 2

Unidad de caja

Unidad de servicios generales

Unidad de apoyo administrativo

Oficina de Coordinacion de servicios generales

Oficina de Coordinacion administrativa

Oficina de Contabilidad

Oficina de Control de bienes

### Piso 3

Aulas c301-c308

## Torre D

### Torre E

### Planta baja

Oficina de Area de ingeniería, suelos y agua

Laboratorio de hidraulica

### Piso 1

Oficina de GISA Grupo de ingenieria suelos y agua

Laboratorio de Deafología

Laboratorio de servicios de análisis de suelos

Laboratorio de manejo de fertilidad de suelos

Laboratorio de reproduccion e inseminación artifical

Laboratorio de investigación de suelos

Laboratorio de nutrición animal

Laboratorio de parasitología

### Piso 2

Departamento de Ingeniería

### Piso 3

Aulas 301-308

## Torre F

### Planta baja

Oficina de Publicaciones periodicas (Emeroteca)

Sala de prestamos

Sala de derecho

### Piso 1

Oficina de Dirección biblioteca / Servicios bibliotecarios NURR

Oficina de Secretaria de los servicios bibliotecarios del NURR

Sala de referencia

Sala procesos tecnicos

### Piso 2

Laboratorio de computacion F201

Laboratorio de computacion EF-207

Laboratorio de computación EF-220

### Piso 3

Oficina de Area de historia y antropologia

Sala de investigación en lenguas extranjeras

Sala de Reading room

Sala de Biblioteca de francés

Sala de geografía
"""

# ---------------------------------------------------------
# 2. CLASE DE PROCESAMIENTO
# ---------------------------------------------------------

class GestorDependencias:
    def __init__(self):
        self.datos = []
        self.headers = ["Torre", "Piso", "Tipo", "Ext", "Coordinador", "Nombre"]

    def _detectar_tipo(self, texto):
        """Infiere el tipo de lugar basado en palabras clave priorizadas."""
        texto_lower = texto.lower()
        
        # Prioridad 1: Tipos explícitos solicitados por el usuario
        if "laboratorio" in texto_lower: return "Laboratorio"
        if "oficina" in texto_lower: return "Oficina"
        if "sala" in texto_lower: return "Sala"
        if "departamento" in texto_lower: return "Departamento"
        
        # Prioridad 2: Elementos comunes no explícitos en la lista pero presentes en el texto
        if "aula" in texto_lower: return "Aula" # Mantenemos Aula por su frecuencia
        
        # Prioridad 3: Mapeo de términos antiguos a los nuevos tipos estándar
        # Las 'Unidades' suelen ser Oficinas administrativas o Departamentos.
        # Dado el contexto, las mapeamos a Oficina para simplificar.
        if "unidad" in texto_lower: return "Oficina"
        
        return "Dependencia General"

    def _extraer_coordinador(self, texto):
        """Busca patrones como 'Cood. Nombre' y separa el nombre del coordinador."""
        # Patrón regex: busca "Cood." seguido opcionalmente por punto y espacio, capturando el resto
        patron = re.compile(r'(?:Cood\.?|Coord\.?)\s*(.*)', re.IGNORECASE)
        match = patron.search(texto)
        
        if match:
            coordinador = match.group(1).strip()
            # Quitamos la parte del coordinador del nombre original para limpiarlo
            nombre_limpio = re.sub(r'(?:Cood\.?|Coord\.?)\s*.*', '', texto, flags=re.IGNORECASE).strip(' .-,')
            return coordinador, nombre_limpio
        return "", texto

    def procesar_texto(self, markdown_text):
        lines = markdown_text.split('\n')
        current_torre = ""
        current_piso = ""
        self.datos = []

        for line in lines:
            line = line.strip()
            if not line: continue

            # Detectar Torre
            if line.startswith("## "):
                current_torre = line.replace("## ", "").strip()
                current_piso = "" # Resetear piso al cambiar de torre
                continue
            
            # Detectar Piso
            if line.startswith("### "):
                current_piso = line.replace("### ", "").strip()
                continue

            # Procesar Dependencia (Línea normal)
            if current_torre: # Solo procesamos si ya tenemos una torre definida
                
                # 1. Extraer Coordinador
                coordinador, nombre_limpio = self._extraer_coordinador(line)
                
                # 2. Detectar Tipo
                tipo = self._detectar_tipo(nombre_limpio)
                
                # 3. Crear registro
                registro = {
                    "Torre": current_torre,
                    "Piso": current_piso if current_piso else "General",
                    "Tipo": tipo,
                    "Ext": "",  # No hay datos en el texto fuente
                    "Coordinador": coordinador,
                    "Nombre": nombre_limpio
                }
                self.datos.append(registro)

    def guardar_json(self, filename="dependencias.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)
        print(f"JSON guardado en: {filename}")

    def guardar_csv(self, filename="dependencias.csv"):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.datos)
        print(f"CSV guardado en: {filename}")

    def obtener_datos(self):
        return self.datos

if __name__ == "__main__":
    # ---------------------------------------------------------
    # 3. EJECUCIÓN
    # ---------------------------------------------------------

    # Instanciar y procesar
    gestor = GestorDependencias()
    gestor.procesar_texto(RAW_MARKDOWN)

    # Guardar archivos
    gestor.guardar_json("datos_universidad.json")
    gestor.guardar_csv("datos_universidad.csv")

    # ---------------------------------------------------------
    # 4. DEMOSTRACIÓN DE USO (Iteración)
    # ---------------------------------------------------------
    print("\n--- Vista Previa de Datos Procesados (Primeros 5) ---")
    datos = gestor.obtener_datos()

    # Ejemplo de iteración filtrando datos
    for i, item in enumerate(datos):
        if i < 5:
            print(f"[{item['Torre']} - {item['Piso']}] {item['Nombre']} (Tipo: {item['Tipo']})")
            if item['Coordinador']:
                print(f"   -> Coordinador: {item['Coordinador']}")

    print(f"\nTotal de registros procesados: {len(datos)}")

    # Ejemplo: Buscar dependencias con coordinador asignado
    print("\n--- Dependencias con Coordinador Asignado ---")
    con_coord = [d for d in datos if d['Coordinador']]
    for d in con_coord:
        print(f"- {d['Nombre']}: {d['Coordinador']}")