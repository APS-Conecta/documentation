---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Ajustes de la app Correo: alertas de abuso, adjuntos, sincronización, TLS, OAuth de Google y Microsoft, tiempos de espera, delegación y funciones con LLM."
---
# Correo

## Resumen

Esta página reúne las opciones de configuración de la app Correo: alertas contra el abuso, límite de adjuntos, sincronización en segundo plano, verificación TLS, OAuth de Google, servidores locales, tiempos de espera, delegación de cuentas, autenticación XOAUTH2 con Microsoft Azure AD, preferencias predeterminadas y funciones con LLM. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/groupware/mail.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Configuración

#### Alertas contra el abuso

La app puede escribir alertas en los registros cuando los usuarios envían mensajes a un número elevado de destinatarios o envían un número elevado de mensajes en un periodo corto de tiempo. Estos eventos podrían indicar que la cuenta se está usando de forma abusiva para enviar mensajes de spam.

Para activar las alertas contra el abuso, hay que establecer algunas opciones de configuración {nc-doc}`mediante occ <admin_manual/occ_command>`.

```
# Turn alerts on
occ config:app:set mail abuse_detection --value=on
# Turn alerts off
occ config:app:set mail abuse_detection --value=off

# Alert when 50 or more recipients are used for one single message
occ config:app:set mail abuse_number_of_recipients_per_message_threshold --value=50

# Alerts can be configured for three intervals: 15m, 1h and 1d
# Alert when more than 10 messages are sent in 15 minutes
occ config:app:set mail abuse_number_of_messages_per_15m --value=10
# Alert when more than 30 messages are sent in one hour
occ config:app:set mail abuse_number_of_messages_per_1h --value=30
# Alert when more than 100 messages are sent in one day
occ config:app:set mail abuse_number_of_messages_per_1d --value=100
```

#### Límite de tamaño de los adjuntos

La administración puede impedir que los usuarios adjunten archivos grandes a sus correos. En su lugar, se pedirá a los usuarios que usen enlaces compartidos.

```
'app.mail.attachment-size-limit' => 3*1024*1024,
```

La unidad son bytes. El ejemplo anterior limita los adjuntos a 3 MB. El valor predeterminado es 0 bytes, lo que significa que no hay límite de subida.

#### Intervalo de sincronización en segundo plano

Configurar con qué frecuencia, en segundos, Correo mantiene actualizados en segundo plano los buzones de los usuarios. El valor predeterminado es 3600 y el mínimo, 300.

```
'app.mail.background-sync-interval' => 7200,
```

#### Desactivar la verificación TLS para IMAP/SMTP

Desactivar la verificación TLS para IMAP/SMTP. Esto se aplica de forma global a todas las cuentas y solo es necesario en casos extremos, como con servidores de correo que tienen un certificado autofirmado.

```
'app.mail.verify-tls-peer' => false
```

#### Google OAuth

Esta app puede permitir a los usuarios conectar sus cuentas de Google con OAuth. Esto hace posible usar cuentas sin 2FA ni contraseña de aplicación.

1. [Crear credenciales de autorización](https://developers.google.com/identity/protocols/oauth2/web-server#prerequisites). Se obtendrán un ID de cliente y un secreto de cliente.
2. Abrir la página de ajustes de Nextcloud. Ir a *Groupware* y desplazarse hasta *Integración con Gmail*. Introducir y guardar el ID de cliente y el secreto de cliente.

#### Servidores IMAP y SMTP locales

De forma predeterminada, Nextcloud no permite nombres de host ni direcciones IP locales como servidores remotos. Esto incluye servidores IMAP, SMTP y Sieve como `localhost`, `mx.local` y `10.0.0.3`. Esta comprobación puede desactivarse mediante `config/config.php`.

```
'allow_local_remote_servers' => true,
```

#### Tiempos de espera

Según el proveedor de correo, puede ser necesario aumentar el umbral de tiempo de espera de IMAP, de SMTP o de ambos. Actualmente, el de IMAP es de 5 segundos de forma predeterminada y el de SMTP, de 20 segundos. Pueden cambiarse de la siguiente manera:

##### Tiempo de espera de IMAP

```
'app.mail.imap.timeout' => 5
```

##### Tiempo de espera de SMTP

```
'app.mail.smtp.timeout' => 20
```

##### Tiempo de espera de Sieve

```
'app.mail.sieve.timeout' => 5
```

#### Usar php-mail para enviar correo

:::{warning}
¡La compatibilidad con php-mail se eliminó en la versión 4.4 de la app Correo!
:::

Se puede usar la función php-mail para enviar correos. Esto es necesario con algunos proveedores de alojamiento web (1&1 (1und1)).

```
'app.mail.transport' => 'php-mail'
```

### Delegación de cuentas

La app Correo admite la delegación de cuentas si la gestiona el servidor de correo. Es decir, el servidor de correo tiene que aceptar correos enviados desde una dirección de alias.

En mailcow, por ejemplo, el ajuste se llama *«Also allowed to send as user»*.

:::{warning}
Salvo que se combine con buzones *Enviados* compartidos o que el servidor de correo lo gestione de otro modo, los mensajes enviados se guardarán en el buzón *Enviados* personal del remitente.
:::

### Posponer y envío programado

:::{note}
Si en las configuraciones de administración se selecciona AJAX para la ejecución de los trabajos cron, las funciones de posponer y de envío programado se desactivan, porque su ejecución no es fiable.
:::

### Autenticación XOAUTH2 con Microsoft Azure AD

:::{versionadded} 3.0.0
:::

La app Correo admite la autenticación XOAUTH2 con cuentas alojadas de Microsoft Outlook. Hay que registrar una app en la interfaz web de Microsoft Azure y proporcionar sus credenciales a la instancia de Nextcloud. Los ajustes correspondientes están en la sección Groupware de las configuraciones de administración.

**Paso 1: Abrir el panel de Azure AD**

Visitar el [portal de Azure](https://portal.azure.com) e ir al panel de Azure AD.

**Paso 2: Crear un nuevo registro de app**

Elegir un nombre y permitir cuentas de Microsoft organizativas y personales. Configurar una app web y copiar el URI de redirección de los ajustes de groupware de la instancia de Nextcloud. Consultar el paso 8 para saber dónde encontrar el URI de redirección. Por último, hacer clic en registrar para continuar.

**Paso 3: Copiar el ID de cliente**

Este ID será necesario más adelante para los ajustes de Nextcloud.

**Paso 4: Crear un nuevo secreto de cliente**

Elegir un nombre descriptivo para el secreto y establecer una fecha de caducidad adecuada. Hacer clic en agregar para crear el secreto.

**Paso 5: Copiar el secreto de cliente**

Copiar el secreto de cliente manualmente o haciendo clic en el botón de copiar. Se encuentra en la columna de valor. El secreto también será necesario más adelante para los ajustes de Nextcloud.

**Paso 6: Configurar Nextcloud**

Abrir los ajustes de groupware en las configuraciones de administración de Nextcloud y rellenar el ID de cliente y el secreto de cliente. Dejar el ID de inquilino tal como está (common). Aquí también se encuentra el URI de redirección. Hacer clic en guardar para continuar.

:::{warning}
Esta guía no cubre el uso de un ID de inquilino personalizado. Configurarlo solo si se tiene experiencia avanzada y se cambiaron los tipos de cuenta admitidos en el paso 2.
:::

**Paso 7: Conectar cuentas de Microsoft Outlook**

¡Enhorabuena! Ya pueden usarse cuentas alojadas de Microsoft Outlook en la app Correo. Al añadir la cuenta, usar el correo electrónico de la cuenta de Microsoft y cualquier contraseña. La contraseña se descartará y aparecerá una ventana emergente de consentimiento de Microsoft para iniciar sesión en la cuenta.

### Compartir buzones

Los usuarios pueden compartir buzones entre sí. Por ahora no hay interfaz para que los usuarios cambien la ACL en la app Correo, pero si se desea usar, hay que activarla en el servidor IMAP y configurar allí los recursos compartidos.

(nc-mail_ui_defaults)=
### Valores predeterminados de las preferencias de la interfaz de usuario

:::{versionadded} 5.2 Nextcloud 30 o posterior
:::

La app Correo permite a la administración establecer preferencias predeterminadas de la interfaz de usuario para todos los usuarios; los usuarios pueden cambiar estas preferencias después. Esto puede ser útil para garantizar una experiencia homogénea en toda la aplicación.

(nc-mail_llm_processing)=
### Procesamiento con LLM

La app Correo puede usar opcionalmente modelos de lenguaje grandes para procesar correos y ofrecer funciones de asistencia como resúmenes de hilos, respuestas inteligentes, agendas de eventos y recordatorios de seguimiento.

:::{note}
Los idiomas admitidos dependen del modelo de lenguaje grande que se use.
:::

:::{note}
Para obtener los mejores resultados, se necesita una integración de procesamiento de texto rápida como <https://apps.nextcloud.com/apps/integration_openai>.
:::

La función puede activarse en las configuraciones de administración de Correo.

Configuraciones de administración > Groupware > App correo electrónico > Habilitar el procesamiento de texto a través de LLMs

(nc-mail_thread_summary)=
### Resumen de hilos

:::{versionchanged} 3.6.0 Nextcloud 26 o posterior
Esta opción de configuración se fusionó en {nc-ref}`mail_llm_processing`
:::

La app de correo admite resumir hilos de mensajes que contienen 3 o más mensajes.

:::{warning}
Para activar esta función, ya debe haber [una integración de IA de generación de texto](https://apps.nextcloud.com/apps/integration_openai) disponible.
:::

La función es opcional: está desactivada de forma predeterminada y puede activarse en las configuraciones de administración de correo.

Configuraciones de administración > Groupware > App correo electrónico > «Enable thread summary»

### Recordatorios de seguimiento

:::{versionadded} 4.0 Nextcloud 30 o posterior
:::

La app Correo recordará automáticamente a los usuarios cuando sus correos salientes sigan sin respuesta durante varios días. Una IA analizará cada correo enviado para comprobar si se espera una respuesta.

La función puede activarse mediante el ajuste global {nc-ref}`mail_llm_processing`.

### Traducción

:::{versionadded} 4.2 Nextcloud 30 o posterior
:::

La app de correo puede ofrecer opcionalmente traducciones de los mensajes si la {nc-ref}`API de traducción <machine_translation>` está activada.
````
