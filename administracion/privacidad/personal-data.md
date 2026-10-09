---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Categorías de datos personales que almacena el servidor: cuenta, perfil, archivos, registros, groupware, Talk, sesiones y servicios de terceros."
---
(nc-gdpr_personal_data)=
# Datos personales almacenados

## Resumen

Esta página resume las categorías de datos personales que almacena el servidor, desde la cuenta y el perfil hasta los registros, las sesiones y los datos que se transmiten a servicios de terceros, como apoyo para preparar el registro de actividades de tratamiento y los avisos de privacidad. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/gdpr/personal_data.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Esta página ofrece una visión general de las categorías de datos personales que almacena Nextcloud, para ayudar a preparar los registros de actividades de tratamiento (RoPA) y los avisos de privacidad que exige el artículo 30 del RGPD.

### Datos de la cuenta

Cada cuenta de usuario contiene los siguientes datos:

- **Nombre de usuario**: el identificador único que se usa para iniciar sesión.
- **Nombre mostrado**: el nombre que ven los demás usuarios.
- **Dirección de correo electrónico**: se usa para notificaciones, restablecimientos de contraseña e invitaciones para compartir.
- **Hash de la contraseña**: se almacena mediante un hash unidireccional; la contraseña en texto plano nunca se almacena.
- **Marca de tiempo del último inicio de sesión**: la fecha y la hora del inicio de sesión más reciente del usuario.
- **Marca de tiempo de creación de la cuenta**: cuándo se creó la cuenta.
- **Tokens de autenticación**: tokens de larga duración creados para clientes y contraseñas de aplicación.

### Datos del perfil

Nextcloud almacena campos de perfil adicionales que los usuarios pueden rellenar:

- Número de teléfono
- Dirección
- URL del sitio web
- Identificador del Fediverso, identificador de Bluesky
- Biografía
- Foto de perfil (avatar)

Cada campo tiene un **ámbito** configurable que controla quién puede verlo: privado, local (visible para los demás usuarios de la misma instancia), federado (compartido con socios de federación de confianza) o publicado (compartido con el servidor de búsqueda público). Los administradores pueden restringir o imponer estos ámbitos en todo el servidor. Consultar {nc-doc}`admin_manual/configuration_user/profile_configuration` para más detalles.

### Archivos y metadatos

- **Contenido de los archivos**: todos los archivos que almacenan los usuarios, incluidos los archivos de puntos de montaje de almacenamiento externo.
- **Metadatos de los archivos**: nombre de archivo, ruta, tamaño, tipo MIME, fecha de creación, fecha de modificación y propietario.
- **Registros de recursos compartidos**: quién ha compartido qué con quién, incluidos los tokens y las contraseñas de los recursos compartidos públicos.
- **Papelera**: los archivos eliminados y sus rutas originales, conservados según la política de conservación configurada.
- **Versiones de archivos**: versiones anteriores de los archivos modificados, conservadas según la política de conservación configurada.

### Registros de actividad y de auditoría

- **Registro de actividad**: un registro por usuario de los eventos de archivos y de uso compartido (subidas, descargas, recursos compartidos, ediciones). Se conserva durante el número de días configurado mediante `activity_expire_days` (predeterminado: 365 días).
- **Registro de auditoría del sistema**: si la app `admin_audit` está activada, se escribe en el archivo de registro de Nextcloud un registro de todo el servidor con las acciones administrativas y los eventos de inicio de sesión.

### Datos de groupware

Cuando las apps de groupware están activadas:

- **Contactos**: vCards con nombres, direcciones de correo electrónico, números de teléfono, direcciones postales, fotos y cualquier otro campo que añadan los usuarios.
- **Eventos de calendario**: títulos, horas, ubicaciones, descripciones y listas de asistentes de los eventos.
- **Tareas**: títulos, descripciones, fechas de vencimiento y estado de finalización de las tareas.

### Talk (chat y llamadas)

Cuando la app Talk está activada:

- **Mensajes de chat**: mensajes de texto y reacciones en conversaciones individuales y de grupo.
- **Metadatos de las llamadas**: participantes y marcas de tiempo de las llamadas (las grabaciones de llamadas, si están activadas, se almacenan como archivos en el almacenamiento del usuario que inicia la llamada).
- **Pertenencia a conversaciones**: qué cuentas pertenecen a qué conversaciones.

### Registros del servidor y del servidor web

Los datos personales también están presentes en los registros del servidor, con independencia de lo que los usuarios almacenen de forma intencionada:

- **Registros de acceso del servidor web**: el servidor web (Apache, nginx) registra la dirección IP, la marca de tiempo y la URL de cada solicitud. Las direcciones IP son datos personales según el RGPD.
- **Registro de la aplicación Nextcloud**: registra errores, advertencias y (en niveles de registro más altos) acciones de los usuarios, incluidas las direcciones IP.
- **Lista de la protección contra ataques de fuerza bruta**: Nextcloud almacena temporalmente la dirección IP de los intentos de inicio de sesión fallidos. Se eliminan automáticamente al cabo de 24 horas o tras un inicio de sesión correcto.

Almacenar los registros indefinidamente no se considera un uso legítimo según el RGPD. Rotar los registros con una frecuencia razonable y considerar cifrarlos, ya que contienen datos personales que se tiene la responsabilidad de proteger. Consultar {nc-doc}`admin_manual/gdpr/data_retention` para obtener orientación sobre la rotación de registros.

### Datos de sesión

Nextcloud almacena los siguientes datos en el cliente como cookies (consultar {nc-doc}`admin_manual/gdpr/cookies` para ver la lista completa) y en el servidor, en el almacén de sesiones:

- Datos de sesión de PHP: un identificador de sesión aleatorio y una frase de contraseña de sesión cifrada.
- Tokens de «Recordarme»: se almacenan si el usuario seleccionó «Recordarme» al iniciar sesión. Su duración la controla `remember_login_cookie_lifetime` (predeterminado: 15 días).

### Datos en manos de servicios de terceros

Algunas funciones opcionales transmiten datos personales fuera del servidor:

- **Servidor de búsqueda público**: los campos del perfil con el ámbito «Publicado» se envían a `lookup.nextcloud.com` (o a un servidor personalizado configurado mediante `lookup_server`) para permitir descubrir usuarios entre instancias. Puede desactivarse estableciendo `lookup_server` en una cadena vacía.
- **Notificaciones push**: Talk y otras apps pueden enviar el contenido de las notificaciones a través del proxy de notificaciones push de {vendor}`Nextcloud`. El contenido contiene el nombre de la cuenta y un mensaje de notificación.
- **Compartición federada**: al compartir archivos con usuarios de otras instancias de Nextcloud, el nombre mostrado y el correo electrónico de quien comparte se transmiten al servidor remoto.
````
