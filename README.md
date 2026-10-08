# documentation

Sitio de documentación de APS-Conecta: la fuente única, en español, de las guías para el personal de salud, los administradores de instalación y los desarrolladores de la organización.

## Qué es

Este repositorio contiene el sitio de documentación pública de APS-Conecta, generado con Sphinx y diseñado para publicarse mediante GitHub Pages. No contiene código de producto: las aplicaciones, la distribución, las bibliotecas y los datos viven en sus propios repositorios, y este sitio solo los documenta y enlaza. La frontera que conviene no confundir: la instalación y la operación de la plataforma se describen aquí, pero se ejecutan desde el repositorio de cada componente.

## Documentación

El sitio se organiza por audiencia:

- **usuario**: guías para el personal que usa la plataforma a diario — interfaz web, archivos, oficina, conversación, calendario, contactos, perfil y seguridad, y las aplicaciones Farmacia, Estadística, Epidemiología y Territorio, además del inicio IntraVox.
- **administración**: instalación, arquitectura, aprovisionamiento, usuarios y grupos, oficina, mapas base, seguridad y operaciones para quien mantiene una instalación.
- **desarrollo**: entorno, desarrollo de aplicaciones, tema, calidad y licencias, con una página de referencia por repositorio de la organización.
- **proyecto**: catálogo de repositorios y seguimiento público del trabajo.

Las páginas de aviso legal, distribución derivada, marcas y licencias se publican como parte del sitio.

## Estado

Estado al 2026-10-07: repositorio recién creado, en su segunda ronda de documentación. Hoy existen los archivos de gobernanza (canon repo-docs, plantillas de incidencia y de solicitud de extracción, flujo de revisión) y este README. El esqueleto de Sphinx, los árboles de contenido por audiencia y la publicación en GitHub Pages se construyen en la ronda actual de trabajo y todavía no están disponibles públicamente.

## Inicio rápido de desarrollo

Requisitos: Python 3.11 o superior.

1. Clonar el repositorio y entrar en él:

   ```console
   git clone https://github.com/APS-Conecta/documentation.git
   cd documentation
   ```

2. Instalar las dependencias de compilación:

   ```console
   pip install -r requirements.txt
   ```

3. Compilar el sitio:

   ```console
   make html
   ```

   El resultado queda en `_build/html/index.html`.

## Licencia

El texto del sitio está cubierto por Creative Commons Atribución 3.0 Unported y el código de soporte (generadores y configuración de compilación) por AGPL-3.0-or-later; los textos legales íntegros viven en `COPYING` y `LICENSE` en la raíz de este repositorio. Las marcas y el logotipo de la organización quedan fuera de esas licencias; el detalle está en la página de [aviso y marcas](https://aps-conecta.github.io/documentation/aviso.html).
