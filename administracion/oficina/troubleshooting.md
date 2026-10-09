---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Conexiones que Nextcloud Office necesita, cómo verificarlas y respuestas a los errores frecuentes con Collabora Online."
---
# Solución de problemas

## Resumen

Esta página enumera las conexiones que deben estar permitidas entre el navegador, Nextcloud y el servidor de Collabora Online, los comandos para verificarlas y las preguntas frecuentes sobre errores de conexión. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/office/troubleshooting.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

En caso de problemas de conectividad, asegurarse de que las siguientes conexiones necesarias son posibles y de que ningún cortafuegos las bloquea:

- El navegador de los usuarios puede llegar tanto al servidor de Nextcloud como al servidor de Collabora Online mediante HTTP(S)
- Nextcloud y el servidor de Collabora Online usan el mismo protocolo
- El servidor de Nextcloud puede llegar al servidor de Collabora Online mediante HTTP(S)
- El servidor de Collabora Online puede llegar al servidor de Nextcloud mediante HTTP(S)

Tanto el registro de Nextcloud como el registro del servidor de Collabora Online pueden mostrar mensajes de error más detallados en caso de problemas de conexión.

- Verificar la conectividad desde el navegador:
  - <https://office.example.com/hosting/capabilities>
  - <https://office.example.com/hosting/discovery>
- Verificar la conectividad desde Nextcloud
  - `curl https://office.example.com/hosting/capabilities`
  - `curl https://office.example.com/hosting/discovery`
- Verificar la conexión desde el servidor de Collabora
  - `curl https://nextcloud.example.com/status.php`

### Preguntas frecuentes

- Problema: aparecen errores de conexión al intentar abrir documentos: Revisar el registro de errores de docker con `docker logs container-id`. Si los registros indican algo como:
  `No acceptable WOPI hosts found matching the target host [YOUR NEXTCLOUD DOMAIN] in config.`
  «Unauthorized WOPI host. Please try again later and report to your administrator if the issue persists.» Puede que el contenedor docker se haya iniciado con la URL equivocada. Comprobar tres veces que se inicia con la URL del servidor de Nextcloud, no con la del servidor en el que se ejecuta Collabora Online.

- Problema: errores «Connection is not allowed»: Es posible que el cortafuegos esté bloqueando las conexiones. Intentar iniciar docker después de haber iniciado el cortafuegos; realiza cambios en las iptables para que Collabora Online pueda funcionar.

- Problema: error «We are sorry, this is an unexpected connection error. Please try again.»: Por el momento, la app Collabora Online no funciona si se activa solo para ciertos grupos. Quitar el filtro de grupos en la sección de apps.

- Problema: Collabora Online no puede con mis 100 usuarios: Esta imagen de docker está diseñada para uso doméstico. Si se necesita una solución más escalable, considerar una suscripción de soporte para disponer de una experiencia de oficina en línea fiable y preparada para empresas.

- Problema: Collabora Online no funciona con el cifrado: Sí, por ahora no está soportado.

- Problema: Nextcloud Office no pudo conectarse al Collabora Online integrado - Servidor CODE integrado: Asegurarse de que la instancia de Nextcloud puede llegar a sí misma usando el mismo nombre de host con el que se accede desde el navegador.

  Para garantizar la conectividad si la resolución DNS no funciona para esto, puede convenir añadir el dominio de Nextcloud a /etc/hosts:
  `` ` 127.0.0.1 cloud.yourdomain.com ` ``

  Si sigue apareciendo una advertencia sobre la lista de permitidos de WOPI, asegurarse de añadir también la IP a la lista de permitidos en Ajustes/Administración/Office.
````
