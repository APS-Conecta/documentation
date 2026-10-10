---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion, AIO]
resumen: "Nextcloud Office en la plataforma base y la oficina de APS Conecta Gestión: Euro-Office, quién escribe cada clave del conector y qué se verifica."
---
# Oficina

## Resumen

Esta sección reúne, para quienes administran el servidor, las páginas de la plataforma base sobre Nextcloud Office: instalación, configuración, proxy inverso, migración y solución de problemas. En APS Conecta Gestión la oficina es otra, como indica el aviso del texto traducido; la sección «En APS Conecta Gestión», al final, describe la que instala la suite.

````{upstream} admin_manual/office/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

Nextcloud Office permite editar los documentos en tiempo real junto con varios editores más, con una representación WYSIWYG de alta fidelidad que conserva el diseño y el formato de los documentos.

Los usuarios pueden insertar comentarios y responderlos, e invitar a otras personas sin cuenta de Nextcloud a editar archivos de forma anónima mediante una carpeta compartida con enlace público.

Nextcloud Office admite decenas de formatos de documento, entre ellos DOC, DOCX, PPT, PPTX, XLS, XLSX + ODF, importación/visualización de Visio, Publisher y muchos más...

Nextcloud Office se basa en Collabora Online Development Edition (CODE) y está disponible de forma gratuita y en pleno desarrollo, ¡con nuevas funciones y mejoras todo el tiempo! Los usuarios empresariales tienen acceso a la versión basada en Collabora Online Enterprise, más estable y escalable, mediante una [suscripción de soporte de Nextcloud](https://nextcloud.com/enterprise/).

Gracias a la asociación de {vendor}`Nextcloud` con Collabora, {vendor}`Nextcloud` puede ofrecer una solución de oficina en línea para toda la comunidad de {vendor}`Nextcloud`, con varias opciones de despliegue. Los usuarios empresariales que busquen una solución más fiable deben ponerse en contacto con el equipo de ventas de {vendor}`Nextcloud`.

- {nc-doc}`admin_manual/office/installation`
- {nc-doc}`admin_manual/office/configuration`
- {nc-doc}`admin_manual/office/migration`
- {nc-doc}`admin_manual/office/troubleshooting`
````

## En APS Conecta Gestión

La oficina de APS Conecta Gestión es Euro-Office: un servidor de documentos en su propio contenedor y la aplicación conectora `eurooffice`. Nextcloud Office no forma parte de la suite. El asistente de instalación de la suite quita las tarjetas de Collabora y OnlyOffice, rechaza cualquier oficina distinta de Euro-Office y rechaza también la petición de cambiarla o desactivarla. El asistente fija además el par certificado: DocumentServer 9.3.4 con el conector 11.0.5.

La aplicación `office` de la plataforma, una vista general que no edita documentos ni está conectada al editor, queda desactivada por la política de aplicaciones: una superficie sin función y con un nombre confuso es peor que ninguna.

### Quién escribe cada clave del conector

Bajo AIO, la conexión con el servidor de documentos tiene dos dueños, y el archivo `.env` del centro no lleva claves de oficina.

| Clave de `eurooffice` | Dueño | Valor |
|---|---|---|
| `DocumentServerUrl` | El entrypoint de AIO, en cada arranque | La dirección pública `https://<dominio o IP>/eurooffice`, desde la que el navegador carga el editor |
| `jwt_secret` | El entrypoint de AIO, en cada arranque | El secreto de su propio servidor de documentos |
| `DocumentServerInternalUrl`, `StorageUrl` | La fase 14, solo en una instalación por IP | El servidor de documentos por su contenedor y la plataforma por el listener interno de apache |
| `sameTab` | La fase 14 | `false` |
| `customizationTheme` | La fase 14 | `default-light` |
| `editFormats`, `defFormats` | La fase 14 | `odt`, `ods` y `odp` activados |

Las razones de cada valor:

- **Instalación por dominio.** Las URL internas quedan sin valor, así que las dos conexiones entre servidores recorren también la dirección pública. Por eso el servidor debe alcanzar su propio dominio: [INSTALLER §7](https://github.com/APS-Conecta/gestion/blob/main/docs/INSTALLER.md#7-dns-the-host-must-reach-its-own-domain-d10) da las tres formas de resolverlo.
- **Instalación por IP.** La suite se publica con un certificado firmado por la CA del instalador, en el que el servidor de documentos no confía, y en una dirección privada desde la que se niega a leer. La fase 14 lleva entonces las dos conexiones entre servidores por dentro de la red del asistente.
- **`sameTab`.** Cada documento se abre en una ventana nueva. Con el valor predeterminado, el editor reemplaza lo que la persona estaba mirando, incluida la carpeta desde la que lo abrió.
- **`customizationTheme`.** El valor predeterminado sigue el tema del sistema operativo de cada equipo. La suite fija el tema claro en toda la interfaz para que un ajuste personal no cambie lo que ve el personal, y el editor era la última superficie fuera de esa decisión.
- **Formatos ODF.** El conector declara ODF como edición con pérdida. Por decisión del responsable, los documentos `odt`, `ods` y `odp` se editan mediante conversión a OOXML, con la pérdida de formato que eso implica; `editFormats` activa la edición y `defFormats` hace que un clic en **Archivos** los abra en el editor.

### Verificación

La verificación de oficina, `scripts/office-smoke.sh`, forma parte de la revalidación posterior a cada actualización y falla ante el primer tramo roto:

1. El conector `eurooffice` está activado.
2. `/eurooffice/healthcheck` responde por la ruta pública, a través de apache: es el tramo que se corta con NAT de horquilla o DNS dividido mientras el contenedor sigue sano.
3. La comprobación del propio conector prueba de una vez el healthcheck, el JWT, la versión mínima y una conversión real de un documento `docx` a través de `StorageUrl`.
4. La versión del servidor de documentos está en la línea 9.3.x: la versión mínima del conector es más antigua y dejaría pasar otra generación sin aviso.
5. La imagen del servidor de documentos es la de AIO o la del canal de la suite; cualquier otra, incluidas las de Collabora y OnlyOffice, falla.

Ninguna verificación automática cubre la presentación en el navegador, la coedición, la fidelidad al abrir y guardar, ni la edición por formato. Una verificación en verde tampoco prueba que una persona en otro equipo pueda abrir un documento: esa comprobación es manual, abriendo un documento desde otro equipo de la red, y la guía clínica la pide después de la mudanza desde la suite anterior.

Un error de «token» o de seguridad al abrir un documento apunta primero a la dirección del editor y después al secreto. El editor informa una falla de token cuando no logra cargarse: en el caso registrado, los secretos coincidían y la causa era una `DocumentServerUrl` que el navegador no alcanzaba. Una URL `http://` bajo una suite servida por `https://` queda además bloqueada como contenido mixto. Bajo AIO, el primer paso es confirmar que `DocumentServerUrl` tiene la forma pública.

### Compromisos y límites

- **Memoria.** Euro-Office es pesado: el documento de arquitectura recomienda unos 8 GB de RAM para el uso con varias personas, y lo fija como piso de todo servidor de centro porque el servidor de documentos arranca con el resto de la suite.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
