---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Mecanismos de autenticación del almacenamiento externo: especiales, por contraseña y de clave pública, y qué implican para compartir almacenamiento."
---
# Mecanismos de autenticación del almacenamiento externo

## Resumen

Esta página describe los mecanismos de autenticación que aceptan los backends de almacenamiento externo (especiales, basados en contraseña y de clave pública) y sus consecuencias cuando el almacenamiento se usa de forma compartida. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/auth_mechanisms.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los backends de almacenamiento de Nextcloud aceptan uno o más esquemas de autenticación, como contraseñas, OAuth o basados en tokens, por citar algunos ejemplos. Cada esquema de autenticación puede implementarse combinando varios mecanismos de autenticación. Los distintos mecanismos requieren distintos parámetros de configuración, según su comportamiento.

### Mecanismos especiales

El mecanismo de autenticación **Ninguno** no requiere parámetros de configuración y se usa cuando un backend no requiere autenticación.

El mecanismo de autenticación **Incorporado** no requiere por sí mismo parámetros de configuración, pero se usa como marcador de posición para los almacenamientos heredados que no se han migrado al nuevo sistema y no aprovechan los mecanismos de autenticación genéricos. Los parámetros de autenticación los proporciona directamente el backend.

### Mecanismos basados en contraseña

El mecanismo **Nombre de usuario y contraseña** requiere un nombre de usuario y una contraseña definidos manualmente. Se pasan directamente al backend y se especifican durante la configuración del punto de montaje.

El mecanismo **Credenciales de login, guardar en la sesión** usa las credenciales de inicio de sesión de Nextcloud del usuario para conectarse al almacenamiento. No se guardan en ningún lugar del servidor, sino en la sesión del usuario, lo que aumenta la seguridad. Este método tiene algunos inconvenientes importantes, ya que Nextcloud no tiene acceso a las credenciales del almacenamiento y, por lo tanto, no puede realizar ninguna tarea en segundo plano sobre el almacenamiento:

- La compartición está desactivada
- El análisis de archivos en segundo plano no funciona
- La caducidad de versiones en segundo plano no funciona
- Los clientes de escritorio y móviles que usan tokens para autenticarse no pueden acceder a esos recursos compartidos
- Otros servicios que podrían solicitar el archivo mediante una solicitud distinta, como Collabora Online u OnlyOffice, no podrán abrir archivos de ese almacenamiento
- El método no puede usarse con autenticación SAML/SSO, porque Nextcloud no obtiene ninguna credencial en absoluto

El mecanismo **Credenciales de inicio de sesión, salvar en la base de datos** usa las credenciales de inicio de sesión de Nextcloud del usuario para conectarse al almacenamiento. Se guardan en la base de datos, cifradas con el secreto compartido. Esto permite compartir archivos desde dentro de este punto de montaje.

- El método no puede usarse con autenticación SAML/SSO, porque Nextcloud no obtiene ninguna credencial en absoluto

El mecanismo **Introducido por el usuario, almacenar en la base de datos** funciona igual que el mecanismo «Nombre de usuario y contraseña», pero cada usuario debe especificar las credenciales de forma individual. Antes del primer acceso a ese punto de montaje, se pedirá al usuario que introduzca las credenciales.

El mecanismo **Credenciales globales** usa el campo de entrada general «Credenciales globales» de la sección de ajustes del almacenamiento externo como fuente de las credenciales, en lugar de credenciales individuales para un punto de montaje.

{nc-ref}`Consideraciones para el almacenamiento compartido <considerations_for_shared_storage_label>`

### Mecanismos de clave pública

Actualmente solo está implementado el mecanismo RSA, en el que Nextcloud genera un par de claves pública/privada y muestra la mitad pública en la interfaz gráfica. Las claves se generan en formato SSH y actualmente tienen una longitud de 1024 bits. Las claves pueden regenerarse con un botón de la interfaz gráfica.

Después de generar las claves, hay que copiar la nueva clave pública al servidor de destino, en `.ssh/authorized_keys`.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage/sftp` para obtener más información sobre cómo configurar la autenticación basada en certificados en SFTP.

(nc-considerations_for_shared_storage_label)=
### Consideraciones para el almacenamiento compartido

Cada almacenamiento externo que usa autenticación específica de usuario se conecta de forma individual. Nextcloud no puede reconocer bloqueos de archivos compartidos entre conexiones individuales, aunque se acceda al mismo archivo.

Esto influye, por ejemplo, en el bloqueo de archivos: un archivo individual bloqueado no se muestra como bloqueado a otros usuarios, o los usuarios no pueden editar documentos de forma colaborativa.

Si se requiere trabajo colaborativo sobre almacenamiento externo, hay que usar la autenticación «Credenciales globales».
````
