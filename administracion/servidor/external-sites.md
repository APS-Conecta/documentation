---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Incrustar sitios web o documentos externos en Nextcloud con la app External sites, y por qué algunos sitios no permiten que se los incruste."
---
# Enlazar sitios externos

## Resumen

Esta página explica, para quienes administran el servidor, cómo incrustar o enlazar sitios web y documentos externos en Nextcloud con la app External sites, y qué configuraciones de los sitios o de los navegadores impiden incrustarlos.

````{upstream} admin_manual/configuration_server/external_sites.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Con la app **External sites** pueden incrustarse sitios web o documentos externos dentro de las páginas de Nextcloud, como muestra esta captura de pantalla.

Esto es útil para acceder rápidamente a páginas importantes, como los manuales de Nextcloud y las páginas informativas de la empresa, y para presentar páginas externas dentro de la imagen de marca personalizada de Nextcloud, si se usan temas personalizados propios.

La app External sites se instala fácilmente desde la tienda de apps. Ir a {guilabel}`Ajustes` → {guilabel}`Apps` → **Customization** para activarla. Después, ir en Nextcloud a {guilabel}`Ajustes` → {guilabel}`Administración` → **External sites** para crear los enlaces, que se guardan automáticamente.

Cada enlace puede tener su propio icono, que puede subirse en los ajustes de administración. Si se selecciona un idioma, el enlace solo se mostrará a los usuarios con el idioma seleccionado. Esto permite tener distintos enlaces de documentación para los usuarios según su idioma.

También es posible añadir enlaces para un dispositivo concreto (reconocido por el agente de usuario). Actualmente están disponibles las siguientes opciones: todos los dispositivos, app de Android, app de iOS, cliente de escritorio y todos los demás (navegadores).

También es posible añadir enlaces solo para los miembros de un grupo determinado.

Los enlaces aparecen en el menú superior de Nextcloud o en el menú de ajustes, después de recargar la página.

### Configuraciones que impiden incrustar

Los enlaces pueden funcionar correctamente o no, debido a las distintas formas en que los navegadores y los sitios web gestionan las URL HTTP y HTTPS, y a que la app External Sites incrusta los enlaces externos en IFrames. Los navegadores modernos se esfuerzan mucho por proteger a quienes navegan de los enlaces peligrosos, y las apps de seguridad como [Privacy Badger](https://www.eff.org/privacybadger) y los bloqueadores de anuncios pueden bloquear las páginas incrustadas. Se recomienda encarecidamente forzar HTTPS en el servidor Nextcloud; no debilitarlo, ni debilitar ninguna de las herramientas de seguridad, solo para que funcionen las páginas web incrustadas. Al fin y al cabo, pueden visitarse libremente fuera de Nextcloud.

La mayoría de los sitios web que ofrecen funciones de inicio de sesión usan la cabecera HTTP `X-Frame-Options` o `Content-Security-Policy`, que indica a los navegadores que no permitan incrustar sus páginas por motivos de seguridad (p. ej., «Clickjacking»). Normalmente, el motivo por el que no es posible incrustar el sitio web puede verificarse con la consola del navegador. Por ejemplo, esta página tiene un certificado SSL no válido.

En esta página, X-Frame-Options impide la incrustación.

También hay una opción de redirección, que permite añadir igualmente esos sitios web para un acceso rápido. En lugar de incrustar el sitio web, se redirige al usuario a él.
````
