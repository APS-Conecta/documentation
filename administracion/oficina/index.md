---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
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

```{note}
Los cambios del plan de actualización corresponden a la próxima versión. Consulte su estado en {doc}`/proyecto/novedades/instalador` y seleccione una versión publicada para instalar.
```

La oficina de APS Conecta Gestión utiliza Euro-Office DocumentServer oficial 9.3.7-1 y el conector oficial `eurooffice`, identificado como «Nextcloud Office». El instalador configura este editor como servicio de oficina de la suite.


La aplicación `office` de la plataforma, una vista general que no edita documentos ni está conectada al editor, queda desactivada por la política de aplicaciones: una superficie sin función y con un nombre confuso es peor que ninguna.

### Quién escribe cada clave del conector

Bajo AIO, la conexión con el servidor de documentos tiene dos dueños, y el archivo `.env` del centro no lleva claves de oficina.

| Clave de `eurooffice` | Dueño | Valor |
|---|---|---|
| `DocumentServerUrl` | Rutina compartida del arranque y la fase 14 | La dirección pública `https://<dominio o IP>/eurooffice`, desde la que el navegador carga el editor |
| `jwt_secret` | Rutina compartida del arranque y la fase 14 | El secreto de su propio servidor de documentos |
| `DocumentServerInternalUrl`, `StorageUrl` | La fase 14, solo en una instalación por IP | El servidor de documentos por su contenedor y la plataforma por el listener interno de apache |
| `sameTab` | La fase 14 | `false` |
| `customizationTheme` | La fase 14 | `default-light` |
| `editFormats`, `defFormats` | La fase 14 | `odt`, `ods` y `odp` activados |

Las razones de cada valor:

- **Instalación por dominio.** Las URL internas quedan sin valor, así que las dos conexiones entre servidores recorren también la dirección pública. Por eso el servidor debe alcanzar su propio dominio: [INSTALLER §7](https://github.com/APS-Conecta/gestion/blob/main/aps/INSTALLER.md#7-dns-the-host-must-reach-its-own-domain-d10) da las tres formas de resolverlo.
- **Instalación por IP.** La suite se publica con un certificado firmado por la CA del instalador, en el que el servidor de documentos no confía, y en una dirección privada desde la que se niega a leer. La fase 14 lleva entonces las dos conexiones entre servidores por dentro de la red del asistente.
- **`sameTab`.** Cada documento se abre en una ventana nueva. Con el valor predeterminado, el editor reemplaza lo que la persona estaba mirando, incluida la carpeta desde la que lo abrió.
- **`customizationTheme`.** El valor predeterminado sigue el tema del sistema operativo de cada equipo. La suite fija el tema claro en toda la interfaz para que un ajuste personal no cambie lo que ve el personal, y el editor era la última superficie fuera de esa decisión.
- **Formatos ODF.** El conector declara ODF como edición con pérdida. Por decisión del responsable, los documentos `odt`, `ods` y `odp` se editan mediante conversión a OOXML, con la pérdida de formato que eso implica; `editFormats` activa la edición y `defFormats` hace que un clic en **Archivos** los abra en el editor.

### Recuperación del servicio

La aplicación permanece habilitada cuando el servidor de documentos tarda en iniciar. La configuración se aplaza para ese arranque y se aplica en el siguiente inicio, una vez disponible el servicio. La fase 14 utiliza la misma rutina después de instalar el conector.

### Verificación

La verificación de oficina, `scripts/office-smoke.sh`, forma parte de la revalidación posterior a cada actualización y falla ante el primer tramo roto:

1. El conector `eurooffice` está activado y conserva su firma oficial.
2. `occ integrity:check-app eurooffice` verifica los archivos del paquete.
3. `/eurooffice/healthcheck` responde correctamente y devuelve `true` por la ruta pública, a través de apache: es el tramo que se corta con NAT de horquilla o DNS dividido mientras el contenedor sigue sano.
4. La comprobación del propio conector prueba de una vez el healthcheck, el JWT, la versión mínima y una conversión real de un documento `docx` a través de `StorageUrl`.
5. La versión nativa coincide con la fijada en el Dockerfile de la suite, basado en DocumentServer 9.3.7-1.
6. La imagen del servidor de documentos es la de AIO o la del canal de la suite; cualquier otra, incluidas las de Collabora y OnlyOffice, falla.

La aceptación del editor incluye apertura desde el navegador, edición simultánea y lectura de los cambios guardados. La fidelidad de cada formato se comprueba con documentos representativos.

Un error de «token» o de seguridad al abrir un documento apunta primero a la dirección del editor y después al secreto. El editor informa una falla de token cuando no logra cargarse: en el caso registrado, los secretos coincidían y la causa era una `DocumentServerUrl` que el navegador no alcanzaba. Una URL `http://` bajo una suite servida por `https://` queda además bloqueada como contenido mixto. Bajo AIO, el primer paso es confirmar que `DocumentServerUrl` tiene la forma pública.

### Compromisos y límites

- **Memoria.** El dimensionamiento combina las referencias oficiales de Nextcloud 34 con la carga medida de Office y la suite completa. Los umbrales compartidos de [#189](https://github.com/APS-Conecta/gestion/issues/189) permanecen pendientes de esos resultados.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
