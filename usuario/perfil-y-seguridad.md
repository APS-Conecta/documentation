---
tipo: guia
esqueleto: plataforma
audiencia: usuario
apps: [gestion]
resumen: "La cuenta propia: idioma, región y teléfono, visibilidad del perfil, sesiones, contraseña, verificación en dos pasos y accesibilidad en la suite."
---
# Perfil y seguridad

## Resumen

Cada persona gestiona su cuenta desde sus ajustes personales: el perfil, las preferencias, la verificación en dos pasos y los navegadores y dispositivos conectados. Esta página reúne esas secciones del manual de la plataforma base y, al final, lo que APS Conecta Gestión fija en cada cuenta del establecimiento.

### Gestionar sus preferencias

````{upstream} user_manual/userpreferences.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Como usuario, usted puede gestionar sus preferencias personales

Para acceder a sus preferencias o configuración personal:

1. Haga clic en su foto de perfil para abrir el menú.
2. Haga clic en **Ajustes** en el menú desplegable para abrir sus ajustes personales.

:::{note}
Si usted es un administrador, también puede gestionar usuarios y el servidor. Estos enlaces no aparecen al resto de usuarios no administradores.
:::

Las opciones que aparecen en la Página de Ajustes Personales dependen de las aplicaciones que hayan sido habilitadas por el administrador. Entre ellas se pueden encontrar las siguientes:

- Uso y cuota disponible
- Gestionar su foto de perfil
- Nombre completo (puede poner lo que quiera, ya que es independiente de su nombre de inicio de sesión de Nextcloud, que es único y no se puede cambiar)
- Dirección de correo electrónico
- Lista de los grupos a los que pertenece
- Cambiar su contraseña
- {nc-doc}`Usar la verificación en dos pasos <user_manual/user_2fa>`
- Preferencias de usuario
- Elegir el idioma de su interfaz de Nextcloud
- Elegir su primer día de la semana preferido
- Enlaces a las aplicaciones de escritorio y móviles
- Gestionar su flujo de Actividad y sus notificaciones
- Carpeta predeterminada en la que guardar los documentos nuevos
- Su ID para compartir en federación
- Enlaces para compartir en redes sociales
- Versión de Nextcloud

:::{note}
Las opciones y los ajustes disponibles dependen de la configuración de su administrador. Si no puede cambiar la contraseña o el nombre mostrado en sus ajustes personales, contacte a su administrador para obtener ayuda.
:::

#### Compartir sus datos en la libreta de direcciones global

Algunos administradores comparten su libreta de direcciones global con otras instancias de Nextcloud (los llamados *Servidores de confianza*) o incluso con todo el mundo. Esto es útil cuando dos instancias quieren trabajar en estrecha colaboración, o cuando las personas quieren usar Nextcloud como una guía telefónica virtual que otros puedan consultar. También permite buscar contactos, crear recursos compartidos y mucho más.

Puede cambiar qué datos personales se comparten estableciendo el alcance de sus datos. Haga clic en el icono del candado para abrir el siguiente desplegable junto a cada entrada. La pantalla muestra el desplegable de alcance de visibilidad de un campo de información personal, con las opciones Privado, Local, Federado y Publicado.

Si establece sus datos como **Privados**, nadie salvo Ud. podrá verla.

Si establece sus datos como **Local**, todos los usuarios con sesión iniciada en su instancia de Nextcloud podrán ver la información, pero nadie fuera de ella.

Si establece sus datos como **Federado**, los servidores de confianza agregados por su administrador podrán ver estos datos, además de todos los usuarios con sesión iniciada.

Si establece sus datos como **Publicado**, cualquiera puede ver sus datos. Esto es útil en algunos casos. Alguien con un rol de cara al público, como marketing o ventas, podría querer compartir sus datos de contacto con una gran variedad de contactos que quizá no usen Nextcloud.

#### Restringir quién puede ver los datos de su perfil

Si su administrador ha habilitado el perfil, otros usuarios e invitados pueden leer los datos de su perfil. Para controlar quién puede ver qué información, ajuste los alcances mencionados arriba:

- **Privado** solo permitirá verlos a usted y a los usuarios que haya agregado a su agenda telefónica.
- **Local** y superiores también permitirán que los invitados vean sus datos.

Para restringir aún más la visibilidad, puede impedir que los invitados vean los datos de su perfil cambiando la visibilidad del perfil a usuarios con sesión iniciada. En sus ajustes personales, busque el botón de visibilidad del perfil.

Esto le permite configurar la visibilidad de cada atributo del perfil.
````

### Usar la verificación en dos pasos

````{upstream} user_manual/user_2fa.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La verificación en dos pasos es una manera de proteger su cuenta de Nextcloud contra el acceso no autorizado. Su funcionamiento requiere dos 'pruebas' de su identidad. Por ejemplo, *algo que usted conoce* (como una contraseña) y *algo que usted tiene* (como una llave física). Normalmente, el primer paso es una contraseña como la que ya tiene y el segundo paso puede ser un mensaje de texto recibido o un código generado en un teléfono u otro dispositivo (*algo que usted tiene*). Nextcloud soporta varios segundos pasos, y se pueden agregar más.

Una vez que su administrador haya habilitado una aplicación de verificación en dos pasos, puede habilitarla y configurarla en sus {nc-doc}`preferencias <user_manual/userpreferences>`.

#### Configurar la verificación en dos pasos

En sus ajustes personales, busque el ajuste **Autenticación de segundo factor**. En este ejemplo se trata de TOTP, un código basado en el tiempo compatible con Google Authenticator. La pantalla muestra la configuración de TOTP.

A continuación verá su código secreto y un código QR que puede ser escaneado por la aplicación TOTP en su teléfono (u otro dispositivo). En función de la aplicación o herramienta, tendrá que copiar el código o escanear el QR, y su dispositivo le mostrará un código de inicio de sesión que cambia cada 30 segundos.

#### Códigos de recuperación si pierde su segundo factor

Siempre debería generar códigos de respaldo para la verificación en dos pasos. Si le roban el dispositivo de su segundo factor o deja de funcionar, puede usar uno de estos códigos para desbloquear su cuenta. En la práctica, funciona como un segundo factor de respaldo. Para obtener los códigos de respaldo, vaya a sus ajustes personales y busque en los ajustes de **Autenticación de segundo factor**. Elija *Generar códigos de respaldo*.

Luego verá una lista de códigos de respaldo de un solo uso.

Guarde estos códigos en un lugar seguro donde pueda encontrarlos. No los guarde junto con su segundo factor (como su teléfono móvil), sino por separado, de modo que perder uno no signifique perder el otro.

#### Iniciar sesión con la verificación en dos pasos

Después de cerrar sesión y volver a iniciarla, verá una solicitud para introducir el código TOTP en su navegador. Si ha habilitado más de un segundo factor, verá una pantalla de selección en la que puede elegir qué método usar para este inicio de sesión. Seleccione TOTP.

Simplemente introduzca su código.

Si el código es correcto, será redirigido a su cuenta de Nextcloud.

:::{note}
Como el código está basado en el tiempo, es importante que los relojes de su servidor y de su teléfono inteligente estén casi sincronizados. Un desfase de unos pocos segundos no será un problema.
:::

#### Usar la verificación en dos pasos con llaves físicas

Puede utilizar la verificación en dos pasos basada en llaves físicas. Los siguientes dispositivos sabemos que funcionan:

- Basadas en TOTP:

  - [Nitrokey Pro](https://shop.nitrokey.com/shop/product/nitrokey-pro-2-3)
  - [Nitrokey Storage](https://shop.nitrokey.com/shop)

- Basadas en FIDO2:

  - [Nitrokey FIDO2](https://shop.nitrokey.com/shop/product/nkfi2-nitrokey-fido2-55)
  - [Nitrokey FIDO U2F](https://shop.nitrokey.com/shop/product/nitrokey-fido-u2f-20)

#### Usar aplicaciones clientes con la verificación en dos pasos

Una vez que haya habilitado la verificación en dos pasos, sus clientes ya no podrán conectarse solo con su contraseña, a menos que también sean compatibles con la verificación en dos pasos. Para resolverlo, debería generar contraseñas específicas de dispositivo para ellos. Consulte {nc-doc}`Gestionar los navegadores y dispositivos conectados <user_manual/session_management>` para obtener más información sobre cómo hacerlo.

#### Consideraciones

Si usa WebAuthn para iniciar sesión en su Nextcloud, asegúrese de no usar el mismo token para la verificación en dos pasos, ya que eso significaría que de nuevo solo está usando un único factor.
````

### Gestionar los navegadores y dispositivos conectados

````{upstream} user_manual/session_management.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
La página de ajustes personales le ofrece una vista general de los navegadores y dispositivos conectados.

#### Gestionar los navegadores conectados

La lista de navegadores conectados muestra qué navegadores se han conectado recientemente a su cuenta.

Puede usar el icono de la papelera para desconectar cualquiera de los navegadores de la lista.

(nc-managing_devices)=
#### Gestionar dispositivos

La lista de dispositivos conectados muestra todos los dispositivos y clientes para los que generó una contraseña de dispositivo, y su última actividad.

Puede usar el icono de la papelera para desconectar cualquiera de los dispositivos de la lista.

Al final de la lista, puede crear una nueva contraseña específica de dispositivo. Puede elegir un nombre para identificar el token más adelante. La contraseña generada se usa para configurar el nuevo cliente. Lo ideal es generar tokens individuales para cada dispositivo que conecte a su cuenta, de modo que pueda desconectarlos individualmente si es necesario.

:::{note}
Solo tiene acceso a la contraseña del dispositivo al crearla. Nextcloud no guarda la contraseña en texto plano, así que introduzca la contraseña en el nuevo cliente de inmediato.
:::

:::{note}
Si usa la {nc-doc}`verificación en dos pasos <user_manual/user_2fa>` en su cuenta, las contraseñas específicas de dispositivo son la única forma de configurar los clientes. El servidor rechazará entonces las conexiones de los clientes que usen su contraseña de inicio de sesión.
:::

#### Contraseñas de dispositivo y cambios de contraseña

Cuando una contraseña cambia en un backend de usuarios externo, todas las contraseñas específicas de dispositivo se marcan como no válidas. Una vez que inicie sesión con la contraseña principal, todas las contraseñas específicas de dispositivo se actualizan y vuelven a funcionar.
````

## En APS Conecta Gestión

### Idioma, región y teléfono

- **Idioma**: la suite fija el español para todas las cuentas, así que el idioma no se cambia en **Información personal**.
- **Región**: parte en Chile (`es_CL`), con fechas y números en el formato de Chile. Cada persona la puede cambiar en **Información personal**.
- **Número de teléfono**: la región telefónica predeterminada es Chile, así que un número chileno se puede escribir sin el código de país.

### Visibilidad del perfil

La suite deja la instalación sin servidor público de búsqueda: ningún dato del perfil se envía a ese servidor, ni siquiera con el alcance **Publicado** que describe «Compartir sus datos en la libreta de direcciones global». Los alcances deciden quién ve cada dato dentro del establecimiento, por ejemplo en el directorio de {doc}`/usuario/contactos`.

### Sesiones

El inicio de sesión no ofrece **Recordarme**: la sesión del navegador termina al cerrar la ventana del navegador. En un computador compartido, cerrar la sesión al terminar:

1. Abrir el menú de la foto de perfil.
2. Elegir **Cerrar sesión**.

Algunos navegadores restauran la sesión anterior al volver a abrirse, con la opción de continuar donde se quedó o con la restauración de sesión. Evitarlo requiere una política en el computador.

Los clientes de escritorio y móviles conservan su propia sesión, que aparece en **Dispositivos y sesiones**, dentro de **Seguridad**.

### Contraseña

Para cambiar la contraseña:

1. Abrir el menú de la foto de perfil.
2. Elegir **Ajustes**.
3. Abrir **Seguridad** en la barra lateral.
4. Escribir la contraseña vigente en **Contraseña actual**.
5. Escribir la contraseña nueva en **Nueva contraseña**.
6. Hacer clic en **Cambiar contraseña**.

La suite no envía ninguna parte de las contraseñas a servicios externos, así que el servidor no comprueba si una contraseña nueva aparece en filtraciones conocidas. Elegir una contraseña propia que no se use en otros servicios. El largo mínimo y las demás reglas de contraseña son las de la plataforma base.

### Verificación en dos pasos

La suite todavía no habilita ningún proveedor de verificación en dos pasos ni la exige; la hoja de ruta deja la exigencia de la verificación en dos pasos para la puesta en producción. Mientras la administración no habilite un proveedor, la sección «Usar la verificación en dos pasos» no se aplica.

### Accesibilidad

La suite fija el tema claro, como explica {doc}`/usuario/interfaz-web`, así que los temas de alto contraste y la fuente para dislexia no están disponibles. Su ajuste de contraste responde a la preferencia del sistema operativo: con la preferencia de aumentar el contraste activada, el texto secundario, los bordes y el contorno del foco se ven más marcados. Con la preferencia de reducir el movimiento activada, la interfaz quita las animaciones.
