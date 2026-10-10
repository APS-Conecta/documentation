---
tipo: guia
audiencia: usuario
apps: [gestion]
resumen: "Editar documentos, hojas de cálculo y presentaciones en el navegador con Euro-Office, entre varias personas y sobre una sola copia."
---
# Oficina

## Objetivo

Editar un documento, una hoja de cálculo o una presentación del establecimiento directamente en el navegador con Euro-Office, el editor de la suite, y trabajar en él con otras personas a la vez sobre una sola copia guardada en el servidor.

Euro-Office corre como servidor de documentos dentro de la propia instalación del establecimiento: el contenido de los documentos no pasa por servicios de oficina externos. Es el único editor de oficina que la suite admite. No tiene un ícono propio entre las aplicaciones: se abre al hacer clic en un documento en **Archivos**.

## Requisitos

- Una cuenta con permiso de gestión sobre la carpeta del documento. {doc}`/usuario/archivos/index` muestra quién gestiona cada carpeta.
- Un navegador de escritorio actualizado.
- Ventanas emergentes permitidas para la dirección de la plataforma: el editor se abre en una pestaña nueva del navegador.

Euro-Office edita estos formatos:

| Formato | Extensiones | Edición |
|---|---|---|
| OOXML | `.docx`, `.xlsx`, `.pptx` | Nativa, con coautoría en tiempo real |
| ODF | `.odt`, `.ods`, `.odp` | Por conversión a OOXML: el documento puede perder formato al guardarse |

## Pasos

Para editar un documento existente:

1. Abrir la aplicación **Archivos**.
2. Abrir la carpeta del área donde está el documento.
3. Hacer clic en el documento.
4. Editar el documento en la pestaña nueva que abre Euro-Office.
5. Cerrar la pestaña del editor al terminar.

Varias personas pueden editar el mismo documento a la vez: un cursor de color marca la posición y la identidad de cada una. Los comentarios admiten respuestas y se pueden marcar como resueltos. El control de cambios marca cada cambio con el nombre de quien lo hizo, de modo que una jefatura puede aceptar o rechazar cada cambio antes de publicar un protocolo.

El editor se muestra siempre claro, aunque el sistema operativo use el modo oscuro. En el modo **Escritorio**, el documento se abre dentro de la ventana del escritorio, no en una pestaña nueva del navegador.

## Verificación

1. Comprobar que el documento se abrió en una pestaña nueva, o en la ventana del escritorio en el modo **Escritorio**, y que **Archivos** sigue abierta.
2. Volver a abrir el documento desde **Archivos**.
3. Comprobar que el documento muestra los cambios.
4. Abrir **Detalles** del documento.
5. Revisar **Versiones**: el historial guarda las versiones anteriores, como explica {doc}`/usuario/archivos/version-control`.

## Problemas frecuentes

**El documento no se abre.** El navegador bloqueó la ventana emergente del editor. Permitir las ventanas emergentes para la dirección de la plataforma y volver a hacer clic en el documento.

**El documento no se puede editar.** La carpeta da solo lectura a la cuenta, como **Transversal** a quien no pertenece a las Jefaturas. Pedir el cambio de permisos a la administración del centro.

**Aparece «Se ha producido un error en el servicio de documentos».** El mensaje viene del servidor de documentos. Avisar a la administración del centro.

**Un mensaje nombra «Nextcloud Office».** Es el mismo editor: la suite cambia el nombre de la aplicación a Euro-Office, pero algunos mensajes del conector conservan su nombre de origen.
