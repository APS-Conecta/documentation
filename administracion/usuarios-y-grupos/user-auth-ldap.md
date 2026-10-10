---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "La app LDAP: pestañas de configuración, ajustes avanzados y expertos, opciones de occ, avatares, resolución de problemas y funcionamiento interno."
---
# Autenticación de usuarios con LDAP

## Resumen

Esta página describe la app LDAP, que permite a los usuarios de LDAP y Active Directory iniciar sesión con sus credenciales: cada campo de las pestañas de configuración, los ajustes avanzados y expertos, las opciones que solo se fijan con `occ`, los avatares, la resolución de problemas y su funcionamiento interno. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/user_auth_ldap.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Nextcloud incluye una aplicación LDAP que permite que los usuarios de LDAP (incluido Active
Directory) aparezcan en las listas de usuarios de Nextcloud. Estos usuarios se autentican en
Nextcloud con sus credenciales de LDAP, así que no hace falta crearles cuentas de usuario de
Nextcloud aparte. Sus pertenencias a grupos de Nextcloud, sus cuotas y sus permisos para compartir
se gestionan igual que los de cualquier otro usuario de Nextcloud.

:::{note}
Se necesita el módulo LDAP de PHP; en la mayoría de las distribuciones lo proporciona `php-ldap`.
:::

La aplicación LDAP admite:

- Compatibilidad con grupos de LDAP
- Compartir archivos con usuarios y grupos de Nextcloud
- Acceso mediante WebDAV y el cliente de escritorio de {vendor}`Nextcloud`
- Control de versiones, almacenamiento externo y todas las demás funciones de Nextcloud
- Conexión transparente con Active Directory, sin necesidad de configuración adicional
- Compatibilidad con los grupos primarios de Active Directory
- Detección automática de atributos de LDAP como el DN base, el correo electrónico y el número de
  puerto del servidor LDAP
- Solo acceso de lectura al LDAP (no se admite editar ni eliminar usuarios en el LDAP)
- Opcional: permitir que los usuarios cambien su contraseña de LDAP desde Nextcloud

:::{note}
El backend LDAP necesita una configuración de SELinux que no lo bloquee o que esté correctamente
configurada. Consultar {nc-ref}`Configuración de SELinux <selinux-config-label>`.
:::

### Configuración

Primero, activar la app {guilabel}`Motor de usuarios y grupos LDAP` en la página Apps de Nextcloud. Después, ir a la
página de administración para configurarla.

El panel de configuración de LDAP tiene cuatro pestañas. Para acceder a las demás pestañas es obligatorio
completar correctamente la primera («Servidor»). Un indicador verde se enciende cuando la configuración es
correcta. Al pasar el cursor sobre los campos aparecen descripciones emergentes.

#### Pestaña Servidor

Empezar por la pestaña Servidor. Si hay varios servidores, pueden configurarse todos.

:::{note}
No configurar aquí ningún host LDAP de conmutación por error. Para ello, consultar las instrucciones de {nc-ref}`Ajustes avanzados <advanced_settings_label>`.
:::

Como mínimo hay que indicar el nombre de host del servidor LDAP. Si el servidor requiere autenticación,
introducir las credenciales en esta pestaña. Nextcloud intentará entonces detectar automáticamente el
puerto y el DN base del servidor. El DN base y el puerto son obligatorios, así que, si Nextcloud no puede
detectarlos, hay que introducirlos manualmente.

- Configuración del servidor: configurar uno o varios servidores LDAP. Hacer clic en el botón
  **Eliminar configuración** para quitar la configuración activa.

- Host: el nombre de host o la dirección IP del servidor LDAP. También puede ser un URI **ldaps://**.
  Indicar el número de puerto acelera la detección del servidor.

  Ejemplos:

  - *directory.my-company.com*
  - *ldaps://directory.my-company.com*
  - *directory.my-company.com:9876*

- Puerto: el puerto por el que conectarse al servidor LDAP. El campo está desactivado al principio de
  una configuración nueva. Si el servidor LDAP funciona en un puerto estándar, el puerto se detecta
  automáticamente. Si se usa un puerto no estándar, Nextcloud intentará detectarlo. Si no lo consigue,
  hay que introducir el número de puerto manualmente.

  Ejemplo:

  - *389*

- DN de usuario: el nombre, en forma de DN, de un usuario con permisos para hacer búsquedas en el
  directorio LDAP. Dejarlo vacío para el acceso anónimo. Se recomienda tener un usuario de sistema LDAP
  específico para esto.

  Ejemplo:

  - *uid=nextcloudsystemuser,cn=sysusers,dc=my-company,dc=com*

- Contraseña: la contraseña del usuario indicado arriba. Vacía para el acceso anónimo.

- DN base: el DN base de LDAP, desde el que se puede llegar a todos los usuarios y grupos. Pueden
  introducirse varios DN base, uno por línea. (Los DN base de usuarios y de grupos pueden establecerse en
  la pestaña Avanzado.) Este campo es obligatorio. Nextcloud intenta determinar el DN base a partir del DN
  de usuario o del host indicados, y hay que introducirlo manualmente si Nextcloud no lo detecta.

  Ejemplo:

  - *dc=my-company,dc=com*

#### Pestaña Usuarios

Esta pestaña controla qué usuarios de LDAP aparecen como usuarios de Nextcloud en el servidor
Nextcloud. Para controlar qué usuarios de LDAP pueden iniciar sesión en el servidor Nextcloud, usar la
pestaña **Atributos de inicio de sesión**. Los usuarios de LDAP que tengan acceso pero no aparezcan como
usuarios (si los hay) serán usuarios ocultos. Si se prefiere, pueden omitirse los campos del formulario e
introducir directamente un filtro LDAP.

- Sólo estas clases de objetos: Nextcloud determina las clases de objeto que suelen estar disponibles para
  los objetos de usuario en el LDAP. Nextcloud selecciona automáticamente la clase de objeto que devuelve
  más usuarios. Pueden seleccionarse varias clases de objeto.

- Sólo desde estos grupos: si el servidor LDAP admite el `member-of-overlay` en los filtros LDAP, puede
  definirse que solo los usuarios de uno o varios grupos concretos puedan aparecer en las listas de
  usuarios de Nextcloud. De forma predeterminada no hay ningún valor seleccionado. Pueden seleccionarse
  varios grupos.

  Si el servidor LDAP no admite el `member-of-overlay` en los filtros LDAP, el campo de entrada está
  desactivado. En ese caso, contactar con el administrador de LDAP.

- Editar consulta LDAP: al hacer clic en este texto se cambia el modo de filtro y puede introducirse
  directamente el filtro LDAP. Ejemplo:

  ```
  (&(objectClass=inetOrgPerson)(memberOf=cn=nextcloudusers,ou=groups,
  dc=example,dc=com))
  ```

- x usuarios encontrados: este indicador muestra aproximadamente cuántos usuarios aparecerán en
  Nextcloud. El número se actualiza automáticamente tras cualquier cambio.

#### Pestaña Atributos de inicio de sesión

Los ajustes de la pestaña Atributos de inicio de sesión determinan qué usuarios de LDAP pueden iniciar
sesión en el sistema Nextcloud y con qué atributo o atributos se compara el nombre de inicio de sesión
proporcionado (por ejemplo, el nombre de usuario de LDAP/AD o la dirección de correo electrónico). Pueden
seleccionarse varios datos del usuario. (Si se prefiere, pueden omitirse los campos del formulario e
introducir directamente un filtro LDAP.)

Los ajustes del filtro de usuarios de la pestaña Usuarios pueden sustituirse usando directamente un
filtro LDAP.

- Nombre de usuario LDAP: si este valor está marcado, el valor de inicio de sesión se compara con el
  nombre de usuario del directorio LDAP. Nextcloud detecta automáticamente el atributo correspondiente,
  normalmente *uid* o *samaccountname*.

- Dirección de correo electrónico LDAP: si este valor está marcado, el valor de inicio de sesión se
  compara con una dirección de correo electrónico del directorio LDAP; en concreto, con los atributos
  *mailPrimaryAddress* y *mail*.

- Otros atributos: esta lista de selección múltiple permite elegir otros atributos para la comparación.
  La lista se genera automáticamente a partir de los atributos de los objetos de usuario del servidor
  LDAP.

- Editar consulta LDAP: al hacer clic en este texto se cambia el modo de filtro y puede introducirse
  directamente el filtro LDAP.

  El marcador **%uid** se sustituye por el nombre de inicio de sesión que el usuario introduce al
  iniciar sesión.

  Ejemplos:

  - solo el nombre de usuario:

    ```
    (&(objectClass=inetOrgPerson)(memberOf=cn=nextcloudusers,ou=groups,
    dc=example,dc=com)(uid=%uid)
    ```

  - nombre de usuario o dirección de correo electrónico:

    ```
    ((&(objectClass=inetOrgPerson)(memberOf=cn=nextcloudusers,ou=groups,
    dc=example,dc=com)(|(uid=%uid)(mail=%uid)))
    ```

#### Pestaña Grupos

De forma predeterminada, ningún grupo de LDAP estará disponible en Nextcloud. Los ajustes de la pestaña
Grupos determinan qué grupos estarán disponibles en Nextcloud. También puede optarse por introducir
directamente un filtro LDAP.

- Sólo estas clases de objetos: Nextcloud determina las clases de objeto que suelen estar disponibles para
  los objetos de grupo en el servidor LDAP. Nextcloud solo muestra las clases de objeto que devuelven al
  menos un objeto de grupo. Pueden seleccionarse varias clases de objeto. Una clase de objeto habitual es
  *group* o *posixGroup*.

- Sólo desde estos grupos: Nextcloud genera una lista de los grupos disponibles en el servidor LDAP.
  Después se seleccionan el grupo o los grupos que obtienen acceso al servidor Nextcloud.

- Editar consulta LDAP: al hacer clic en este texto se cambia el modo de filtro y puede introducirse
  directamente el filtro LDAP.

  Ejemplo:

  - *objectClass=group*
  - *objectClass=posixGroup*

- y grupos encontrados: indica aproximadamente cuántos grupos estarán disponibles en Nextcloud. El número
  se actualiza automáticamente tras cualquier cambio.

(nc-advanced_settings_label)=
### Ajustes avanzados

La sección de ajustes avanzados de LDAP contiene opciones que no son necesarias para que la conexión
funcione. Ofrece controles para desactivar la configuración actual, configurar hosts réplica y varias
opciones que mejoran el rendimiento.

Los ajustes avanzados se dividen en cuatro partes:

- Ajustes de conexión
- Ajustes de directorio
- Atributos especiales
- Atributos del perfil de usuario

#### Ajustes de conexión

- Configuración activa: activa o desactiva la configuración actual. De forma predeterminada está
  desactivada. Cuando Nextcloud hace una conexión de prueba correcta, se activa automáticamente.

- Servidor de copia de seguridad (Réplica): si hay un servidor LDAP de respaldo, introducir aquí sus ajustes de
  conexión. Nextcloud se conectará automáticamente al de respaldo cuando no pueda alcanzar el servidor
  principal. El servidor de respaldo debe ser una réplica del principal para que los UUID de los objetos
  coincidan.

  Ejemplo:

  - *directory2.my-company.com*

- Puerto para copias de seguridad (Replica): el puerto de conexión del servidor LDAP de respaldo. Si no se indica
  ningún puerto, sino solo un host, se usa el puerto principal (el indicado arriba).

  Ejemplo:

  - *389*

- Deshabilitar servidor principal: permite anular manualmente el servidor principal y hacer que Nextcloud
  solo se conecte al servidor de respaldo. Es útil para paradas planificadas.

- Desactivar la validación por certificado SSL: desactiva la comprobación de certificados SSL. ¡Usarlo
  solo para pruebas!
  *Nota*: el efecto de este ajuste depende de la configuración de PHP del sistema. Por ejemplo, no
  funciona con la
  [imagen oficial del contenedor de {vendor}`Nextcloud`](https://github.com/nextcloud/docker).
  Para desactivar la verificación de certificados en un uso concreto, añadir la siguiente línea de
  configuración a */etc/ldap/ldap.conf*:

  `` ` TLS_REQCERT ALLOW ` ``

- Cache TTL: se introduce una caché para evitar tráfico LDAP innecesario, por ejemplo
  guardando en caché los nombres de usuario para no tener que buscarlos en cada página, y acelerando la
  carga de la página Usuarios. Guardar la configuración vacía la caché. El tiempo se indica en segundos.

  Hay que tener en cuenta que casi todas las peticiones PHP requieren una nueva conexión con el servidor
  LDAP. Si se necesitan peticiones PHP con datos recientes, se recomienda definir un tiempo de vida mínimo
  de unos 15 s, en lugar de eliminar por completo la caché.

  Ejemplos:

  - diez minutos: *600*
  - una hora: *3600*

La sección Caché, más abajo, explica en detalle cómo funciona la caché.

(nc-ldap_directory_settings)=
#### Ajustes de directorio

- Campo de nombre de usuario a mostrar: el atributo que debe usarse como nombre mostrado en Nextcloud.

  - Ejemplo: *displayName*

- 2do Campo de Nombre a Mostrar por el Usuario: un segundo atributo opcional que se muestra entre
  paréntesis después del nombre mostrado; por ejemplo, con el atributo `mail` se muestra como `Molly Foo
  (molly@example.com)`.

- Árbol base de usuario: el DN base de LDAP desde el que se puede llegar a todos los usuarios. Debe ser
  un DN completo, independientemente de lo que se haya introducido como DN base en los ajustes básicos.
  Pueden indicarse varios árboles base, uno por línea.

  - Ejemplo:

    *cn=programmers,dc=my-company,dc=com*\
    *cn=designers,dc=my-company,dc=com*

- Atributos de la busqueda de usuario: estos atributos se usan al buscar usuarios, por ejemplo en el
  diálogo de compartir. El atributo de nombre mostrado del usuario es el predeterminado. Pueden indicarse
  varios atributos, uno por línea.

  Si un atributo no está disponible en un objeto de usuario, el usuario no aparecerá en la lista y no
  podrá iniciar sesión. Esto también afecta al atributo de nombre mostrado. Si se sustituye el valor
  predeterminado, hay que indicar aquí el atributo de nombre mostrado.

  - Ejemplo:

    *displayName*\
    *mail*

- Desactivar los usuarios ausentes en LDAP: si se activa, los usuarios que faltan en LDAP, también
  llamados remanentes, se comportan como si estuvieran desactivados en Nextcloud. Esto significa, por
  ejemplo, que los recursos compartidos públicos de estos usuarios dejan de funcionar. Ver también
  {nc-doc}`admin_manual/configuration_user/user_auth_ldap_cleanup`.

- Campo de nombre de grupo a mostrar: el atributo que debe usarse como nombre de grupo en Nextcloud.
  Nextcloud admite un conjunto limitado de caracteres (a-zA-Z0-9.-_@). Una vez asignado un nombre de
  grupo, no se puede cambiar.

  - Ejemplo: *cn*

- Árbol base de grupo: el DN base de LDAP desde el que se puede llegar a todos los grupos. Debe ser un
  DN completo, independientemente de lo que se haya introducido como DN base en los ajustes básicos.
  Pueden indicarse varios árboles base, uno en cada línea.

  - Ejemplo:

    *cn=barcelona,dc=my-company,dc=com*\
    *cn=madrid,dc=my-company,dc=com*

- Atributos de búsqueda de grupo: estos atributos se usan al buscar grupos, por ejemplo en el diálogo
  de compartir. De forma predeterminada se usa el atributo de nombre mostrado del grupo indicado arriba.
  Pueden indicarse varios atributos, uno en cada línea.

  Si se sustituye el valor predeterminado, el atributo de nombre mostrado del grupo no se tendrá en
  cuenta, salvo que también se indique.

  - Ejemplo:

    *cn*\
    *description*

- Asociación Grupo-Miembro: el atributo que indica la pertenencia a grupos, es decir, el atributo
  que usan los grupos de LDAP para referirse a sus usuarios.

  Nextcloud detecta el valor automáticamente. Solo debe cambiarse si hay una razón muy justificada y se
  sabe lo que se hace.

  - Ejemplo: *uniquemember*

- Grupos anidados: activa la obtención de miembros de grupo desde los subgrupos.

  Para permitir el listado de usuarios y el inicio de sesión desde grupos anidados, consultar **Listado
  de usuarios e inicio de sesión por grupos anidados** en la sección **Resolución de problemas, consejos
  y trucos**.

- Permitir cambios de contraseñas LDAP por usuario: permite que los usuarios de LDAP cambien su
  contraseña y que los superadministradores y los administradores de grupo cambien la contraseña de sus
  usuarios de LDAP.

  Para activar esta función deben cumplirse los siguientes requisitos:

  - Requisitos generales:

    - Deben configurarse en el servidor LDAP políticas de control de acceso que concedan permisos para cambiar contraseñas. El DN de usuario configurado en *Ajustes del servidor* necesita permisos de escritura para actualizar el atributo userPassword.
    - Las contraseñas se envían en texto plano al servidor LDAP. Por eso, la comunicación entre Nextcloud y el servidor LDAP debe usar cifrado de transporte, por ejemplo LDAPS.
    - Se recomienda encarecidamente activar el hash de contraseñas en el servidor LDAP. Mientras que Active Directory guarda de forma predeterminada las contraseñas en un formato unidireccional, los usuarios de OpenLDAP pueden configurar la directiva `ppolicy_hash_cleartext` del overlay ppolicy que incluye OpenLDAP.

  - Requisitos adicionales para Active Directory:

    - La comunicación entre Nextcloud y el servidor LDAP debe usar un cifrado de transporte de al menos 128 bits.
    - Asegurarse de que el carácter `fUserPwdSupport` de dSHeuristics esté configurado para usar el atributo `userPassword` como alias de `unicodePwd`. Aunque en AD LDS esto viene configurado así de forma predeterminada, no ocurre lo mismo en AD DS.

- Política de contraseñas por defecto DN: esta función requiere OpenLDAP con ppolicy. El DN de
  una política de contraseñas predeterminada se usará para gestionar la caducidad de las contraseñas
  cuando no exista una política de contraseñas específica del usuario. La gestión de la caducidad de las
  contraseñas ofrece lo siguiente:

  - Cuando una contraseña de LDAP está a punto de caducar, mostrar al usuario un mensaje de advertencia con el número de días que faltan para que caduque. Las advertencias de caducidad de contraseña se muestran a través de la app de notificaciones de Nextcloud.

  - Pedir a los usuarios de LDAP con contraseñas caducadas que restablezcan su contraseña al iniciar sesión, siempre que aún les quede un número suficiente de inicios de sesión de gracia.

  Dejar el ajuste vacío para mantener desactivada la gestión de la caducidad de las contraseñas.

  Para que la gestión de la caducidad de las contraseñas funcione, los cambios de contraseña de LDAP por
  usuario deben estar activados y el servidor LDAP debe ejecutar OpenLDAP con su módulo ppolicy
  configurado en consecuencia.

  - Ejemplo:

    *cn=default,ou=policies,dc=my-company,dc=com*

(nc-ldap_special_attributes)=
#### Atributos especiales

- Cuota: Nextcloud puede leer un atributo de LDAP y establecer la cuota del usuario según su
  valor. Indicar aquí el atributo; devolverá valores legibles, p. ej. «2 GB».

  - Ejemplo: *NextcloudQuota*

:::{warning}
Los parámetros de cuota de LDAP prevalecen sobre los parámetros de cuota establecidos en la página de gestión de usuarios de Nextcloud.
:::

- Cuota por defecto: indica una cuota predeterminada para los usuarios de LDAP que no tienen una cuota
  establecida en el campo de cuota anterior.

  - Ejemplo: *15 GB*

:::{warning}
Los parámetros de cuota de LDAP prevalecen sobre los parámetros de cuota establecidos en la página de gestión de usuarios de Nextcloud.
:::

- E-mail: establece el correo electrónico del usuario a partir de su atributo de
  LDAP. Dejarlo vacío para el comportamiento predeterminado.

  - Ejemplo: *mail*

- Regla para la carpeta Home de usuario: de forma predeterminada, el servidor Nextcloud crea
  el directorio del usuario en el directorio de datos de Nextcloud y le da el nombre de usuario de
  Nextcloud, p. ej. `/var/www/nextcloud/data/alice`. Puede convenir sustituir este ajuste y darle el
  nombre del valor de un atributo de LDAP. El atributo también puede devolver una ruta absoluta, p. ej.
  `/mnt/storage43/alice`. Dejarlo vacío para el comportamiento predeterminado.

  - Ejemplo: *cn*

En las instalaciones nuevas de Nextcloud, la regla de la carpeta personal se impone. Esto significa que, una vez establecida una regla de nombre de la carpeta personal (obtener la carpeta personal de un atributo de LDAP), esta debe estar disponible para todos los usuarios. Si no está disponible para un usuario, ese usuario no podrá iniciar sesión. Además, no se configurará el sistema de archivos de ese usuario, así que sus recursos compartidos no estarán disponibles para los demás usuarios.

En las instalaciones de Nextcloud migradas se sigue aplicando el comportamiento anterior, que consiste en usar el nombre de usuario de Nextcloud como carpeta personal cuando no hay un atributo de LDAP establecido. Esto puede cambiarse imponiendo la regla de la carpeta personal con el comando `occ` de Nextcloud, como en este ejemplo en Ubuntu:

```
sudo -E -u www-data php occ config:app:set user_ldap enforce_home_folder_naming_rule --value=1
```

(nc-ldap_user_profile_attributes)=
#### Atributos del perfil de usuario

Tras configurar estos atributos, los datos del perfil de usuario se sobrescriben con los datos correspondientes de LDAP. La suma de comprobación de los datos de LDAP se guarda en los ajustes de usuario `user_ldap`, `lastProfileChecksum`, y la actualización del perfil se omite mientras los datos de LDAP no cambien. Si `memcache.distributed` está activado en `config.php`, la suma de comprobación se guarda en caché y la comprobación se omite mientras exista el valor en caché (caduca tras `ldapCacheTTL` segundos).

- Tener en cuenta:
  - El usuario puede cambiar los datos del perfil, pero se sobrescribirán si cambian en LDAP
  - El usuario puede cambiar el ámbito de visibilidad en el perfil
  - La visibilidad predeterminada puede ajustarse con la matriz `account_manager.default_property_scope` en `config.php`
  - Si hay varios valores de atributo, solo se usa el primer valor distribuido
  - Todas las propiedades del perfil de usuario están limitadas a 2048 caracteres
  - Tener datos con un formato incorrecto en LDAP probablemente dejará vacíos los campos del perfil de usuario
  - Establecer el ajuste global `profile.enabled => false` en `config.php` hace que se omita este código

Al ejecutar `sudo -E -u www-data php occ ldap:check-user --update <uid>` se muestran los datos del usuario en LDAP y se actualiza el perfil. Para obtener el valor `<uid>` correcto de cualquier usuario puede usarse `php occ user:list`.

:::{note}
Si aquí se quita el nombre de un atributo, los datos no se eliminan del perfil de usuario. Establecer un atributo inexistente vacía el campo correspondiente del perfil.
:::

- Campo Teléfono: el atributo de LDAP que contiene el número de teléfono, que se copia en el campo
  Teléfono del perfil. El número de teléfono debe tener formato internacional sin separadores (E.164).
  Asegurarse de dar a los números de teléfono un formato como `+4966612345678`.

  - Ejemplo: *telephoneNumber*
  - Ejemplo: *mobile*

:::{note}
Conviene establecer `default_phone_region` en `config.php`.
:::

- Campo sitio Web: el atributo de LDAP que contiene el URI del sitio web.
  El URI debe empezar por `https://` o `http://`; actualmente el perfil de usuario de Nextcloud no admite otros.
  Si se usan atributos `labeledURI`, se elimina la etiqueta (todo lo que va después del primer ESPACIO).

  - Ejemplo: *wWWHomePage*
  - Ejemplo: *labeledURI*

- Campo Dirección: el atributo de LDAP que contiene la dirección del usuario. En la página del perfil
  de usuario se llama Ubicación. Nextcloud espera un valor de una sola línea, como `city, country` o
  `somewhere under the loving sun`. El formato postalAddress de varias líneas se reformatea: el
  delimitador SIGNO DE DÓLAR se sustituye por COMA+ESPACIO.

  - Ejemplo: *postalAddress*
  - Ejemplo: *localityName*

- Campo Twitter: el atributo de LDAP que contiene el nombre de la cuenta de Twitter.

- Campo Fediverso: el atributo de LDAP que contiene la dirección del Fediverso del usuario.

- Campo Organización: el atributo de LDAP que contiene el nombre de la organización.

  - Ejemplo: *company*
  - Ejemplo: *o* u *organizationName*

- Campo Rol: el atributo de LDAP que contiene el rol organizativo, dentro de la organización, o el
  cargo.

  - Ejemplo: *title*

- Campo Título: el atributo de LDAP que contiene el título del usuario.

- Campo Biografía: el atributo de LDAP que contiene la biografía del usuario (descripción breve).
  Valor de varias líneas con final de línea LF de Unix.
  Los finales de línea CRLF de Windows y CR de Macintosh se sustituyen por el final de línea LF de Unix.

- Campo de Fecha de nacimiento: el atributo de LDAP que contiene la fecha de nacimiento del usuario.
  Formatos admitidos:

  - [GeneralizedTime de LDAP](https://ldapwiki.com/wiki/Wiki.jsp?page=GeneralizedTime)
  - `YYYY-MM-DD`
  - `YYYYMMDD`

### Ajustes expertos

En los ajustes expertos puede adaptarse el comportamiento fundamental a las necesidades de cada caso. La
configuración debe probarse bien antes de empezar a usarla en producción.

- Nombre de usuario interno: el nombre de usuario interno es el identificador de los usuarios de LDAP en
  Nextcloud. De forma predeterminada se crea a partir del atributo UUID. El atributo UUID garantiza que
  el nombre de usuario sea único y que no haya que convertir caracteres. Solo se admiten estos
  caracteres: `[a-zA-Z0-9_.@-]`. Los demás caracteres se sustituyen por sus equivalentes ASCII o
  simplemente se omiten.

  El backend LDAP garantiza que no haya nombres de usuario internos duplicados en Nextcloud, es decir,
  comprueba todos los demás backends de usuarios activados (incluidos los usuarios locales de
  Nextcloud). Si hay colisiones, se añade al valor obtenido un número aleatorio (entre 1000 y 9999). Por
  ejemplo, si «alice» existe, el siguiente nombre de usuario puede ser «alice_1337».

  El nombre de usuario interno es el nombre predeterminado de la carpeta personal del usuario en
  Nextcloud. También forma parte de las URL remotas, por ejemplo en todos los servicios \*DAV.

  Todo esto puede sustituirse con el ajuste Nombre de usuario interno. Dejarlo vacío para el
  comportamiento predeterminado. Los cambios solo afectan a los usuarios de LDAP asignados a partir de
  entonces.

  Al configurarlo, hay que tener en cuenta que el nombre de usuario en Nextcloud se considera inmutable y
  no puede cambiarse después. Esto puede causar problemas si se usa un atributo que puede cambiar, p. ej.
  la dirección de correo electrónico de un usuario, que cambiará cuando cambie su nombre.

  - Ejemplo: *uid*

- Anular la detección UUID: de forma predeterminada, Nextcloud detecta automáticamente el atributo
  UUID. El atributo UUID se usa para identificar de forma única a los usuarios y grupos de LDAP. El nombre
  de usuario interno se crea a partir del UUID, salvo que se indique otra cosa.

  Puede sustituirse este ajuste e indicar un atributo a elección. Hay que asegurarse de que el atributo
  elegido pueda obtenerse tanto para usuarios como para grupos y de que sea único. Dejarlo vacío para el
  comportamiento predeterminado. Los cambios solo tienen efecto en los usuarios y grupos de LDAP asignados
  a partir de entonces. También tienen efecto cuando cambia el DN de un usuario o grupo y había un UUID
  antiguo en caché, lo que dará lugar a un usuario nuevo. Por eso, este ajuste debe aplicarse antes de
  poner Nextcloud en producción y de borrar las vinculaciones (véase la sección `User and Group Mapping`
  más abajo).

  - Ejemplo: *cn*

- Asignación del Nombre de usuario de un usuario LDAP: Nextcloud usa los nombres de usuario como claves
  para guardar y asignar datos. Para identificar y reconocer con precisión a los usuarios, cada usuario
  de LDAP tiene un nombre de usuario interno en Nextcloud. Esto requiere una asignación del nombre de
  usuario de Nextcloud al usuario de LDAP. El nombre de usuario creado se asigna al UUID del usuario de
  LDAP. Además, el DN también se guarda en caché para reducir la interacción con LDAP, pero no se usa para
  la identificación. Si el DN cambia, Nextcloud detecta el cambio comprobando el valor del UUID.

  Lo mismo vale para los grupos.

  El nombre interno de Nextcloud se usa en todo Nextcloud. Borrar las asignaciones dejará restos por
  todas partes. No borrar nunca las asignaciones en un entorno de producción, sino solo en un servidor de
  pruebas o experimental.

:::{warning}
Borrar las asignaciones no depende de la configuración: ¡afecta a todas las configuraciones de LDAP!
:::

### Probar la configuración

El botón **Configuración de prueba** comprueba los valores tal como figuran en ese momento en los campos de
entrada. No hace falta guardar antes de probar. Al hacer clic en el botón, Nextcloud intenta vincularse
al servidor Nextcloud con los ajustes que figuran en ese momento en los campos de entrada. Si la
vinculación falla, aparece un aviso amarillo con el mensaje de error «The configuration is invalid. Please have a look at the logs for further details.»

Cuando la prueba de configuración sea correcta, guardar los ajustes y comprobar en la página Usuarios
que los usuarios y grupos se obtienen correctamente.

### Opciones de configuración adicionales mediante occ

Unos pocos ajustes de configuración solo pueden establecerse en la línea de comandos mediante `occ`.

#### Intervalo de sincronización en segundo plano

El backend LDAP actualiza los atributos de usuario (correo electrónico, cuota, avatar y otros) en cada
inicio de sesión, la primera vez que detecta un usuario nuevo y periódicamente mediante un trabajo en
segundo plano.

El trabajo en segundo plano recalcula su intervalo de ejecución tras cada ciclo. El objetivo es procesar
cada usuario de LDAP conocido aproximadamente una vez al día. El intervalo se obtiene a partir del número
total de usuarios asignados y del menor tamaño de paginación de LDAP configurado, y después se limita a
un mínimo de 30 minutos y un máximo de 12 horas.

#### Asignación del grupo de administración

Es posible promover **un** LDAP por conexión como grupo de administración, de modo que todos sus miembros
tengan también privilegios de administración en Nextcloud.

Un grupo puede promoverse mediante una llamada `occ` específica a la que se pasa un parámetro de grupo,
que puede ser un ID de grupo de nextcloud o un nombre de grupo que se buscará. Cuando se ejecuta una
búsqueda, se requiere una coincidencia exacta.

Ejemplo de uso:

```
$ sudo -E -u www-data php occ ldap:promote-group --help
Description:
  declares the specified group as admin group (only one is possible per LDAP configuration)

Usage:
  ldap:promote-group [options] [--] <group>

Arguments:
  group                 the group ID in Nextcloud or a group name

Options:
  -y, --yes             do not ask for confirmation
…

# Example
$ sudo -E -u www-data php occ ldap:promote-group  "Nextcloud Admins"
Promote Nextcloud Admins to the admin group (y|N)? y
Group Nextcloud Admins was promoted

$ sudo -E -u www-data php occ ldap:promote-group  "Paramount Court"
Promote Nextcloud Admins to the admin group and demote Nextcloud Admins (Group ID: nextcloud_admins) (y|N)? y
Group Paramount Court was promoted

$ sudo -E -u www-data php occ ldap:promote-group  "Paramount Court"
The specified group is already promoted
```

:::{note}
El ID del grupo solo se muestra cuando difiere del nombre mostrado del grupo.
:::

También es posible establecer la asignación del grupo de administración con
`occ ldap:set-config $configId ldapAdminGroup $groupId`, pero como el ID de grupo de Nextcloud puede no
conocerse (todavía), se recomienda (sobre todo en configuraciones automatizadas) usar el comando
*promote-group*, que además incorpora el grupo y determina su ID.

Para degradar o restablecer una promoción, hay que establecer una cadena vacía en el ldapAdminGroup de la
configuración de destino:

```
# Reset an admin group mapping via set-config
occ ldap:set-config $configId ldapAdminGroup ""
# Example
occ ldap:set-config s01 ldapAdminGroup ""
```

:::{tip}
Para tener más de un grupo de administración en una conexión, crear en el directorio LDAP un grupo contenedor que incluya cada grupo como miembro anidado, y promover ese grupo.
:::

### Integración de avatares de Nextcloud

Nextcloud admite imágenes de perfil de usuario, también llamadas avatares. Si un usuario tiene una foto
guardada en el atributo *jpegPhoto* o *thumbnailPhoto* del servidor LDAP, se usará como su avatar. En ese
caso, el usuario no puede modificar su avatar (en su página personal), porque debe cambiarse en LDAP.
*jpegPhoto* tiene preferencia sobre *thumbnailPhoto*.

Si el atributo *jpegPhoto* o *thumbnailPhoto* no está establecido o está vacío, los usuarios pueden subir
y gestionar sus avatares en sus páginas personales de Nextcloud. Los avatares gestionados en Nextcloud no
se guardan en LDAP.

El atributo *jpegPhoto* o *thumbnailPhoto* se obtiene una vez al día para garantizar que Nextcloud use la
foto actual de LDAP. Los avatares de LDAP prevalecen sobre los de Nextcloud, y cuando se elimina un avatar
de LDAP, lo sustituye el avatar de Nextcloud más reciente.

Las fotos servidas desde LDAP se recortan y redimensionan automáticamente en Nextcloud. Esto solo afecta
a la presentación; la imagen original no cambia.

#### Usar un atributo concreto o desactivar la carga de imágenes

Es posible desactivar la integración de avatares o indicar un único atributo distinto del que leer la
imagen. Se espera que contenga datos de imagen, igual que *jpegPhoto* o *thumbnailPhoto*.

El comportamiento solo puede cambiarse con la herramienta de línea de comandos occ. Básicamente, hay
estas opciones:

- Debe usarse el comportamiento predeterminado descrito arriba

  `occ ldap:set-config "s01" "ldapUserAvatarRule" "default"`

- No deben obtenerse de LDAP las imágenes de los usuarios

  `occ ldap:set-config "s01" "ldapUserAvatarRule" "none"`

- La imagen debe leerse del atributo «selfiePhoto»

  `occ ldap:set-config "s01" "ldapUserAvatarRule" "data:selfiePhoto"`

«s01» se refiere al ID de configuración, que puede obtenerse con `occ ldap:show-config`.

### Resolución de problemas, consejos y trucos

#### Registro

La implementación de LDAP de Nextcloud puede registrar muchos detalles adicionales sobre su actividad. Al
diagnosticar problemas, puede ser útil ajustar temporalmente `loglevel` a INFO (`1`) o DEBUG (`0`).

#### Verificación de certificados SSL (LDAPS, TLS)

Un error habitual con los certificados SSL es que PHP puede no conocerlos. Si hay problemas con la
validación de certificados, asegurarse de que

- El certificado del servidor esté instalado en el servidor Nextcloud
- El certificado esté declarado en el archivo de configuración de LDAP del sistema (normalmente
  */etc/ldap/ldap.conf*)
- Si se usa LDAPS, el puerto también esté configurado correctamente (de forma predeterminada, 636)

#### Microsoft Active Directory

A diferencia de versiones anteriores de Nextcloud, ya no hace falta ningún ajuste adicional para que
Nextcloud funcione con Active Directory. Nextcloud encuentra automáticamente la configuración correcta
durante el proceso de configuración.

#### memberOf / permisos de lectura de memberof

Para usar `memberOf` en el filtro, puede que haya que conceder al usuario que hace las consultas permisos
para usarlo. Para Microsoft Active Directory, esto se describe
[aquí](https://serverfault.com/questions/167371/what-permissions-are-required-for-enumerating-users-groups-in-active-directory/167401#167401).

#### Listado de usuarios e inicio de sesión por grupos anidados

Cuando se quiere permitir el listado de usuarios y el inicio de sesión a partir de un grupo concreto que
tiene subgrupos («grupos anidados»), no basta con marcar **Grupos anidados** en **Configuracion de
directorio**. También hay que cambiar el filtro de usuarios (y el de inicio de sesión), indicando la regla
de coincidencia `LDAP_MATCHING_RULE_IN_CHAIN`. Cambiar las partes del filtro que contienen la condición
*memberof* según este ejemplo:

- (memberof=cn=Nextcloud Users Group,ou=Groups,…)

por

- (memberof:1.2.840.113556.1.4.1941:=cn=Nextcloud Users Group,ou=Groups,…)

#### Duplicar configuraciones de servidor

Si se tiene una configuración que funciona y se quiere crear otra similar, o hacer una «instantánea» de
las configuraciones antes de modificarlas, puede hacerse lo siguiente:

1. Ir a la pestaña **Servidor**
2. En **Configuración del servidor**, elegir *Añadir configuración del servidor*
3. Responder *sí* a la pregunta «Take over settings from recent server configuration?»
4. (opcional) Pasar a la pestaña **Avanzado** y desmarcar **Configuración activa** en *Configuración de
   conexión*, para que la nueva configuración no se use al guardar
5. Hacer clic en **Guardar**

Ahora ya puede modificarse y activarse la configuración.

### Funcionamiento interno de LDAP en Nextcloud

Aquí se describen algunos aspectos del funcionamiento del backend LDAP.

#### Asignación de usuarios y grupos

En Nextcloud, el nombre de usuario o de grupo se usa para asignarle toda la información pertinente en la
base de datos. Para que funcione de forma fiable, se crea un nombre interno permanente de usuario y de
grupo, que se asigna al DN y al UUID de LDAP. Si el DN cambia en LDAP, se detectará y no habrá
conflictos.

Estas asignaciones se guardan en las tablas de base de datos `ldap_user_mapping` y
`ldap_group_mapping`. El nombre de usuario también se usa para la carpeta del usuario (salvo que se
indique otra cosa en *Regla para la carpeta Home de usuario*), que contiene archivos y
metadatos.

El nombre de usuario interno y el nombre mostrado visible están separados. Todavía no ocurre lo mismo con
los nombres de grupo, es decir, un nombre de grupo no puede modificarse.

Esto significa que la configuración de LDAP debe estar bien terminada antes de ponerla en producción.
Las tablas de asignación se rellenan pronto, pero mientras se esté probando pueden vaciarse en cualquier
momento. No hacerlo en producción.

Los atributos de los usuarios se obtienen bajo demanda (es decir, para el autocompletado al compartir o
en la gestión de usuarios) y después se guardan en la base de datos de Nextcloud para lograr un mejor
rendimiento por nuestra parte. Normalmente se vuelven a comprobar dos veces al día, por lotes, para todos
los usuarios. Además, también se actualizan cuando ese usuario inicia sesión, o pueden obtenerse
manualmente con el comando occ `occ ldap:check-user --update USERID`, donde `USERID` es el ID de usuario
de Nextcloud.

Para los grupos, se guarda en la base de datos una caché de pertenencias para poder desencadenar eventos
cuando se añade o se quita una pertenencia. Esta caché la actualiza un trabajo en segundo plano, y puede
forzarse su actualización con `occ ldap:check-group --update GROUPID`.

#### Caché

La información de LDAP se guarda en la caché de memoria de Nextcloud, y hay que instalar y configurar esa
caché de memoria (consultar {nc-doc}`admin_manual/configuration_server/caching_configuration`). La
**caché** de Nextcloud ayuda a acelerar las interacciones de los usuarios y el uso compartido. Se rellena
bajo demanda y permanece rellena hasta que caduca el **Cache TTL** de cada petición
única. Los inicios de sesión de los usuarios no se guardan en caché, así que, si hace falta mejorar los
tiempos de inicio de sesión, conviene configurar un servidor LDAP esclavo para repartir la carga.

El valor de **Cache TTL** puede ajustarse para equilibrar el rendimiento y la actualidad
de los datos de LDAP. De forma predeterminada, todas las peticiones LDAP se guardan en caché durante 10
minutos, y esto puede cambiarse con el ajuste **Cache TTL**. La caché responde a cada
petición idéntica a una anterior, dentro del tiempo de vida de la petición original, en lugar de consultar
al servidor LDAP.

El **Cache TTL** se aplica a cada petición por separado. Cuando una entrada de la caché
caduca, no hay ningún desencadenante automático que vuelva a rellenar la información, ya que la caché solo
se rellena con peticiones nuevas, por ejemplo al abrir la página de administración de usuarios o al buscar
en un diálogo de compartir.

Hay un desencadenante que se activa automáticamente mediante un trabajo en segundo plano concreto, que
mantiene `user-group-mappings` actualizado y siempre en caché.

En circunstancias normales, nunca se cargan todos los usuarios a la vez. Normalmente, los usuarios se
cargan mientras se generan los resultados de la página, en tandas de 30, hasta alcanzar el límite o hasta
que no quedan resultados. Para que esto funcione en un servidor Nextcloud y un servidor LDAP, debe
admitirse **Paged Results**.

Nextcloud recuerda a qué configuración de LDAP pertenece cada usuario. Esto significa que cada petición se
dirige siempre al servidor correcto, salvo que un usuario esté desaparecido, por ejemplo por una migración
de servidor o porque el servidor no es accesible. En ese caso, los demás servidores también reciben la
petición.

#### Gestión con servidor de respaldo

Cuando Nextcloud no puede contactar con el servidor LDAP principal, supone que está desconectado y no
intentará conectarse de nuevo durante el tiempo indicado en **Cache TTL**. Si hay un
servidor de respaldo configurado, Nextcloud se conectará a él en su lugar. Cuando haya una parada
programada, marcar **Deshabilitar servidor principal** para evitar intentos de conexión innecesarios.

### Nota

Cuando el nombre o el apellido de un objeto LDAP, es decir, el atributo de nombre mostrado (de forma
predeterminada «displayname»), se deja vacío, Nextcloud lo trata como un objeto vacío y, por tanto, no
muestra ningún resultado de ese usuario u objeto de AD, para evitar que se recopilen cuentas técnicas.
````
