---
tipo: guia
audiencia: usuario
apps: [gestion]
resumen: "Crear desde Archivos un documento, una hoja de cálculo o una presentación con Euro-Office, en formato OOXML y con un nombre según la convención."
---
# Crear un documento con Euro-Office

## Objetivo

Crear un documento, una hoja de cálculo o una presentación en una carpeta del establecimiento y abrirlo en Euro-Office, el editor de oficina de la suite que describe {doc}`/usuario/oficina`.

Euro-Office crea los archivos nuevos en formato OOXML: `.docx` para un documento, `.xlsx` para una hoja de cálculo y `.pptx` para una presentación, el formato que edita de forma nativa según la tabla de {doc}`/usuario/oficina`.

## Requisitos

- Una cuenta con permiso de gestión sobre la carpeta donde va el archivo: en una carpeta de solo lectura, el botón **+** no aparece. La página {doc}`/usuario/archivos/index` muestra quién gestiona cada carpeta.
- Ventanas emergentes permitidas para la dirección de la plataforma: Euro-Office abre el archivo nuevo en una pestaña nueva del navegador.

## Pasos

1. Abrir la aplicación **Archivos**.
2. Abrir la carpeta del área donde va el archivo.
3. Hacer clic en el botón **+** sobre la lista de archivos.
4. Hacer clic en {guilabel}`Nuevo documento`, {guilabel}`Nueva hoja de cálculo` o {guilabel}`Nueva presentación`.
5. Escribir el nombre del archivo en el campo {guilabel}`Nombre de archivo`.
6. Hacer clic en {guilabel}`Crear`.
7. Editar el archivo en la pestaña nueva que abre Euro-Office.

El campo {guilabel}`Nombre de archivo` trae un nombre de partida, como «Nuevo documento.docx», con la parte anterior a la extensión ya seleccionada: lo que se escribe reemplaza esa parte y conserva la extensión. Si el nombre queda sin extensión, **Archivos** agrega la que corresponde.

El nombre de partida no sigue la convención de nombres de la suite, `AAAA-MM-DD_area_tema_vN.ext`. Reemplazarlo por un nombre como `2026-07-19_protocolos_triage-urgencias_v2.docx`. La sección «Nombres de archivo» de {doc}`/usuario/archivos/index` explica cada parte del patrón. **Archivos** no comprueba la convención: el nombre se ajusta a mano.

Si hay plantillas disponibles, antes de crear el archivo aparece la ventana «Elija una plantilla para …». En ella, hacer clic en {guilabel}`Vacío` o en una plantilla y después en {guilabel}`Crear`. La suite no instala plantillas, así que, mientras nadie las agregue, el archivo se crea vacío sin pasar por esa ventana.

## Verificación

1. Volver a la pestaña de **Archivos**.
2. Comprobar que el archivo aparece en la carpeta con el nombre elegido y la extensión `.docx`, `.xlsx` o `.pptx`.

## Problemas frecuentes

**No aparece el botón + o el menú no ofrece «Nuevo documento».** Si falta el botón **+**, la cuenta tiene solo lectura en la carpeta, como **Transversal** para quien no pertenece a las Jefaturas: abrir una carpeta que la cuenta gestiona o pedir el cambio de permisos a la administración del centro. Si el botón **+** aparece pero el menú no ofrece las opciones de Euro-Office, Euro-Office no tiene una conexión válida con su servidor de documentos: avisar a la administración del centro.

**Aparece «Este nombre ya está en uso.»** La carpeta ya tiene un archivo con ese nombre y el botón {guilabel}`Crear` queda desactivado. Escribir otro nombre.

**El archivo se creó, pero el editor no se abrió.** El navegador bloqueó la ventana emergente del editor. Permitir las ventanas emergentes para la dirección de la plataforma y hacer clic en el archivo en **Archivos**.

**Aparece «No se ha podido crear un nuevo archivo desde la plantilla».** **Archivos** no pudo crear el archivo. Avisar a la administración del centro.
