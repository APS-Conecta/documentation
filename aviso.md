---
tipo: explicacion
---
# Aviso legal

Esta página resume la postura legal del sitio de documentación de APS Conecta y de la distribución que documenta. Cada afirmación procede de una fuente verificada; el texto normativo de cada licencia vive, sin traducir, en los archivos citados.

(origen)=
## Origen: distribución derivada de Nextcloud

### El problema y el objetivo

En un centro de salud familiar (CESFAM) los documentos no tienen una versión confiable. Las copias se multiplican (`_final`, `_final2`, `_ESTE_SI`), los archivos quedan en descargas personales en vez de un lugar compartido, el acceso depende de las personas y no de sus roles, y cada establecimiento ordena sus archivos a su manera. A eso se suma la instalación: una instalación estándar de Nextcloud entrega una plataforma vacía que un administrador de sistemas debe configurar, y la mayoría de los centros de atención primaria no tiene esa persona.

APS Conecta Gestión existe para **simplificar la instalación de una plataforma de colaboración en un centro de atención primaria de Chile, con código propio**. Un instalador en español de Chile y un conjunto de fases de aprovisionamiento dejan configurado el establecimiento completo —árbol documental, roles, permisos, suite ofimática, tema, intranet y aplicaciones del sector— a partir de su identidad en el registro de establecimientos del DEIS y de una planilla con el personal. La instalación no exige administrar Nextcloud a mano. APS Conecta Gestión no es un sistema de registro clínico: no guarda datos de pacientes.

### Base sin modificar

APS Conecta Gestión es una distribución derivada de Nextcloud 34. El servidor es la imagen oficial `nextcloud:34-apache`, fijada por su digest y sin modificar: el proyecto no bifurca el núcleo. PostgreSQL, Redis y el servidor de documentos Euro-Office corren también como imágenes oficiales sin modificar. Las aplicaciones Nextcloud de terceros se instalan desde sus paquetes publicados, guardados en el repositorio de la suite; la tabla de componentes indica cuáles se usan tal cual.

### Lo que APS Conecta modifica

| Componente | Cómo se modifica | Dónde vive el cambio |
|---|---|---|
| Nextcloud All-in-One (instalador) | Fork con una cola numerada de parches que se reaplica sobre cada versión upstream | `APS-Conecta/AIO`, carpeta `patches/` |
| IntraVox (portada de la intranet, «Inicio») | Fork con funciones locales | `APS-Conecta/IntraVox`, ADR-0001 del fork |
| Conector de Euro-Office y Escritorio (`desktop_workspace`) | Parches que el aprovisionamiento aplica sobre el paquete oficial durante la instalación; la imagen del servidor no se reconstruye | `APS-Conecta/gestion`, `provisioning/apps/<aplicación>/` |
| Tipografías Fraunces y Nunito Sans | Un subconjunto de cada una va incrustado en los logotipos SVG, una versión modificada que la OFL permite | `APS-Conecta/gestion`, `themes/apsconecta/core/` |

La tabla de componentes, al final de esta sección, cuenta los parches de cada componente en cada compilación del sitio y describe qué cambia en cada uno.

### Adaptaciones al sector de atención primaria

| Adaptación | Problema que resuelve | Dónde vive |
|---|---|---|
| Instalación simplificada: asistente en español de Chile, establecimiento elegido del registro DEIS y confirmado en el mapa, personal cargado desde una planilla CSV, configuración completa por fases | Una instalación estándar exige un administrador de sistemas que el centro no tiene | `APS-Conecta/AIO` `patches/`; `APS-Conecta/gestion` `provisioning/phases/` |
| Árbol documental de cuatro áreas: Transversal, Programas, Unidades y Sectores, en carpetas de grupo propias de cada establecimiento | Cada centro archiva a su manera y nadie sabe dónde va un documento | `APS-Conecta/gestion` `provisioning/phases/30-folders.sh` |
| Acceso por rol: 22 roles comunes a todos los establecimientos, según las familias de la Ley 19.378, más 4 categorías y los equipos propios de cada centro | El acceso ligado a personas se rompe con cada rotación de personal | `APS-Conecta/gestion` `provisioning/phases/20-groups.sh` |
| Permisos que solo amplían, sin reglas de denegación; administrar incluye eliminar, con recuperación desde la papelera de la carpeta | Carpetas donde un archivo subido por error nunca se puede quitar | `APS-Conecta/gestion` `provisioning/phases/40-acl.sh` |
| Una sola copia viva: edición simultánea en Euro-Office e historial de versiones | «No hay una versión confiable»: copias `_final2` | `APS-Conecta/gestion` `provisioning/phases/14-office.sh`, `docs/CONVENTIONS.md` |
| Convenciones de organización instaladas dentro de la intranet («LÉEME — Convenciones.md», en Transversal) | Reglas que nadie lee porque viven fuera de la herramienta | `APS-Conecta/gestion` `provisioning/phases/30-folders.sh` |
| Portada de intranet (Inicio) como página de entrada, con bienvenida administrada | El personal entra a una lista de archivos en vez de la información institucional | `APS-Conecta/gestion` `provisioning/phases/41-intravox.sh` |
| Idioma es-CL y nombre del producto en toda la interfaz | Una plataforma genérica, pensada primero en inglés | `APS-Conecta/gestion` `provisioning/phases/10-locale.sh`, `15-branding.sh` |
| Aplicaciones del sector: farmacia (vademécum y arsenal), estadística (REM), epidemiología (alertas por sector) y territorio (sectores en el mapa) | Trabajo que hoy vive en planillas fuera de la intranet | Un repositorio por aplicación; ver el catálogo |

### Código propio

Las aplicaciones epidemiologia, farmacia, territorio y estadistica, el fork de IntraVox, el tema visual de la suite y la configuración como código del aprovisionamiento son trabajo de APS Conecta bajo la licencia AGPL-3.0-or-later. El [catálogo de repositorios](_generated/catalogo) los enumera uno a uno.

### Texto de los manuales

Las páginas de la plataforma base derivan de la documentación oficial de Nextcloud (`nextcloud/documentation`, rama de la versión que corre la suite), publicada bajo CC BY 3.0. Donde la traducción oficial al español todavía coincide con el texto vigente, se usa tal cual; el resto lo traduce un flujo con inteligencia artificial, solo en la prosa: el código, los comandos y las claves de configuración quedan como en el original. Ese texto se teje en los capítulos de APS Conecta Gestión, y una regla de compilación reemplaza «Nextcloud» por «APS Conecta Gestión» en todo el sitio, salvo en esta página, en el código, en las direcciones web y en los nombres legales. Cada sección derivada nombra su fuente, la versión exacta de la que proviene y su licencia.

### Tabla de componentes

```{include} _generated/componentes.md
```

## Marcas

- Este proyecto no es producido por, ni está afiliado con, patrocinado o respaldado por Nextcloud GmbH, titular de la marca «Nextcloud».
- El logotipo de Nextcloud es asimismo marca de Nextcloud GmbH.
- La marca y el logotipo de APS Conecta quedan reservados por su titular conforme a la sección 7(e) de la Licencia Pública General Affero de GNU, versión 3; esa reserva de marca no añade restricción alguna a los derechos que la licencia concede sobre el código.
- Las demás marcas citadas en este sitio pertenecen a sus respectivos titulares y se usan de forma meramente nominativa.

## Licencias

- El texto de este sitio y sus capturas de pantalla se publican bajo la licencia Creative Commons Atribución 3.0 Unported (CC BY 3.0); el texto legal completo, en inglés y sin traducir, está en el archivo `COPYING` del repositorio.
- El código de compilación del sitio (configuración, herramientas y plantillas) está disponible bajo la Licencia Pública General Affero de GNU, versión 3 o posterior (AGPL, «AGPL-3.0-or-later»); el texto de la licencia está en `LICENSES/AGPL-3.0-or-later.txt`.
- El titular del copyright del propio código es Daniel Espinoza Charrier, que actúa a título personal porque APS Conecta todavía no constituye una persona jurídica.
- Las fuentes tipográficas Fraunces y Nunito Sans están bajo la SIL Open Font License 1.1 (OFL-1.1); el sitio las obtiene en compilación desde el tema de la suite y no las versiona en este repositorio.

## Registro de IP en GitHub Pages

Este sitio se publica mediante GitHub Pages. La documentación pública de GitHub declara que Pages registra y almacena la dirección IP de cada visitante con fines de seguridad, haya iniciado sesión en GitHub o no (docs.github.com, «What is GitHub Pages»). Ese registro es ajeno a este proyecto, que no lo controla ni accede a él.
