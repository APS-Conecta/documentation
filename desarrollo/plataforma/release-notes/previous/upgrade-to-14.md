---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cambios de la versión 14 para las apps: soporte de PHP, frontend, API de backend modificadas, obsoletas y eliminadas, comportamiento, configuración y OCS."
---
# Actualización a Nextcloud 14

## Resumen

Esta página enumera los cambios de la versión 14 que afectan a las apps: soporte de PHP, cambios de frontend, API de backend modificadas, obsoletas y eliminadas, y cambios de comportamiento, de configuración, de OCS e internos. Está dirigida a quienes desarrollan o mantienen apps.

````{upstream} developer_manual/release_notes/previous/upgrade_to_14.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:::{note}
Los cambios críticos se recopilaron [en GitHub](https://github.com/nextcloud/server/issues/7827). Consultar el ticket original para ver los enlaces a las pull requests y a los tickets.
:::

### General

- Se añadió compatibilidad con PHP 7.0 y PHP 7.1.
- Introducción de declaraciones de tipo para tipos escalares en las API públicas, de acuerdo con el PHPDoc existente.

### Cambios de frontend

- `OCA.Search` ahora es `OCA.Search.Core`.
- La estructura general cambió.
- `.with-app-sidebar` ya no es necesario para abrir la barra lateral; solo hay que usar *disappear* en la barra lateral
- `.svg` ya no es necesario
- `.with-settings` ya no es necesario
- `.with-icon` ya no es necesario

### Cambios de backend

#### API modificadas

- `AppFramework\Http\Request::getHeader` siempre devuelve una cadena (y no null).
- `Security\ICrypto::decrypt` solo acepta cadenas.
- `\OCP\AppFramework\Utility\ITimeFactory` tiene tipado estricto.
- `\OCP\IL10N` tiene tipado estricto.
- `\OCP\Mail` y las plantillas de correo electrónico recibieron declaraciones de tipo.
- `\OCP\Authentication\TwoFactorAuth` recibió declaraciones de tipo y declaraciones de tipo de retorno.
- `\OCP\Migration\IMigrationStep` tiene dos métodos nuevos.
- Las clases hijas de `EMailTemplate` deben usar la notación *%$1s* para los reemplazos, para ser compatibles a futuro y poder reutilizar parámetros.

#### API obsoletas

- `OCP\Files`
- Definir URL de cliente personalizadas en una clase `\OC_Theme` personalizada. Deben usarse los ajustes de config.php.
- Los niveles de registro de `OCP\Util`. Se trasladaron a la interfaz `\OCP\ILogger`
- `OCP\AppFramework\Db\Mapper`. Migrar a `\OCP\AppFramework\Db\QBMapper`

#### API eliminadas

- varias funciones obsoletas de `\OCP\AppFramework/IAppContainer`
- `\OCP\BackgroundJob::registerJob`
- `\OCP\Config`
- `\OCP\Contacts`
- `\OCP\DB`
- `\OCP\Files::tmpFile`
- `\OCP\Files::tmpFolder`
- `\OCP\IHelper`
- `\OCP\ISearch\search`
- `\OCP\JSON`
- `\OCP\Response`
- `\OCP\Share::resolveReshare`
- `\OCP\User::getDisplayNames`
- `\OCP\Util\formatDate`
- `\OCP\Util::generateRandomBytes`
- `\OCP\Util::sendMail`
- `\OCP\Util::encryptedFiles`
- `\OCP\Util::getServerProtocol`
- `\OCP\Util::getServerHost`
- `\OCP\Util::getServerProtocol`
- `\OCP\Util::getRequestUri`
- `\OCP\Util::getScriptName`
- `\OCP\Util::urlgenerator`
- Constantes *OCP* obsoletas
- Funciones de plantilla obsoletas de OCP
- Algunos métodos obsoletos de `\OCP\Response`
- HTTPHelper

### Cambios de comportamiento

- Se eliminó `--no-app-disable` del comando `occ upgrade`.
- El contenedor de inyección de dependencias ya no inyectará `$fromMailAddress`.
- Las apps habilitadas para grupos ahora pueden ofrecer páginas públicas, disponibles incluso si no hay un usuario con la sesión iniciada.
- El método *AddUser* *POST:/users* de la API OCS ahora permite una contraseña vacía si y solo si el correo electrónico está definido y es válido.
- Los textos de los correos electrónicos ya no se escapan automáticamente en todos los casos.

### Cambios de configuración

- Al usar Swift Objectstore como almacenamiento personal, asegurarse de definir el parámetro `bucket/container`.
- `mail_smtpmode` ya no puede establecerse en `php`, ya que esta opción se pierde con la actualización de phpmailer.

### Cambios de OCS

#### API añadidas

- Endpoint de detalles para la lista de usuarios
- Endpoint de detalles para la lista de grupos

#### API modificadas

- El método *getGroup* de la API OCS se sustituyó por *getGroupUsers* #8904

### Cambios internos

:::{note}
Solo es relevante si se usaron API no públicas. No deben usarse.
:::

- limpieza del espacio de nombres `OC_*`: se eliminaron bastantes clases, métodos y constantes del espacio de nombres interno.
- Se eliminó `OC_Group_Backend`
- Se eliminaron `OC_Response::setStatus` y las constantes de los códigos de estado
````
