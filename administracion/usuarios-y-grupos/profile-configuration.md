---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Perfiles de usuario: activarlos o desactivarlos, la visibilidad de sus campos, los ámbitos de cada propiedad y sus valores predeterminados en config.php."
---
# Perfiles

## Resumen

Esta página explica cómo se activan y desactivan los perfiles de usuario, cómo se combinan la visibilidad de cada campo y el ámbito de cada propiedad, cuáles son los ámbitos predeterminados y cómo sustituirlos o restringirlos. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_user/profile_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
El perfil de usuario muestra información sobre una cuenta. Los perfiles están activados de forma predeterminada.

Los usuarios pueden activar o desactivar su propio perfil en **Ajustes personales**, en **Información personal**.

Los administradores pueden:

- establecer el estado predeterminado del perfil para los usuarios nuevos, y
- desactivar los perfiles de forma global.

Los datos del perfil también pueden usarlos otras funciones (por ejemplo, la {nc-ref}`libreta de direcciones del sistema <system-address-book>`), pero lo que se expone depende de los controles de privacidad.

:::{note}
La visibilidad del perfil funciona por capas.

- **La activación del perfil** determina si la función de perfil está activa o no.
- **Los ajustes de visibilidad de los campos del perfil** controlan si un campo se muestra.
- **Los ámbitos de las propiedades de la cuenta** (por ejemplo `private`, `local`, `federated`,
  `published`) definen el público previsto de cada propiedad.
- **Las restricciones de descubrimiento** (por ejemplo, las reglas de enumeración al compartir y al autocompletar)
  pueden reducir aún más lo que otras cuentas pueden encontrar o ver.

En resumen: la visibilidad efectiva es el resultado más restrictivo de todos los controles aplicables.
:::

### Configuración

#### Establecer el valor predeterminado del perfil para los usuarios nuevos

En **Configuraciones de administración** -> **Ajustes básicos**, usar el interruptor del valor predeterminado del perfil.

También puede establecerse con `occ`:

```
occ config:app:set settings profile_enabled_by_default --value="0"
```

Usar `--value="1"` para volver a activarlo de forma predeterminada.

Consultar {nc-doc}`admin_manual/occ_command` para más detalles sobre el uso de `occ`.

#### Desactivar los perfiles de forma global

Para desactivar la funcionalidad de perfil para todos los usuarios, añadir esto a `config.php`:

```
'profile.enabled' => false,
```

### Ajustes de visibilidad de los campos del perfil

Cada campo del perfil tiene su propio ajuste de **visibilidad del perfil** (guardado por usuario en la configuración del perfil):

- **Mostrar a todos** (`show`): visible para cualquiera, incluidos los visitantes no autenticados,
  *sujeto al ámbito de propiedad del campo*.
- **Mostrar únicamente a usuarios con sesión iniciada** (`show_users_only`): visible solo para usuarios
  autenticados, *sujeto al ámbito de propiedad del campo*.
- **Ocultar** (`hide`): nunca se muestra en las superficies del perfil, sea cual sea el ámbito de propiedad.

Corresponden a las opciones de visibilidad de **Ajustes personales** -> **Información personal**
-> **Editar la visibilidad de su perfil**.

:::{important}
La visibilidad efectiva es el resultado más restrictivo de **ambos** controles: el ajuste de visibilidad del perfil y el ámbito de la propiedad.
:::

#### Valores predeterminados

De forma predeterminada, la mayoría de los campos del perfil están configurados como **Mostrar a todos**, mientras que algunos
campos relacionados con el contacto tienen como valor predeterminado **Mostrar únicamente a usuarios con sesión iniciada**.

Los administradores deben tener en cuenta que estos valores predeterminados son independientes de los
*ámbitos de propiedad* predeterminados que se describen más abajo.

(nc-profile-property-scopes)=
### Ámbitos de visibilidad de las propiedades

Las propiedades del usuario (Nombre mostrado, Dirección, Sitio web, Cargo, etc.) tienen ámbitos de visibilidad: Privado, Local, Federado, Publicado.

Estos ámbitos se evalúan por atributo. Que un perfil sea accesible no implica
que todos sus atributos sean visibles.

Los ámbitos de visibilidad son:

- Privado: el nivel más restrictivo. Los datos se ocultan en los perfiles públicos, en la federación y en la
  búsqueda pública. En el servidor local solo se muestran en funciones concretas y,
  normalmente, solo a usuarios autenticados que tienen una relación reconocida con el
  titular de la cuenta (por ejemplo, como contacto conocido).
- Local: datos de contacto visibles en la instancia local y en algunos contextos públicos en los que se necesitan
  atributos del perfil o de la cuenta (por ejemplo, metadatos del propietario o de quien sube un archivo).
  No se comparten con servidores federados ni se publican en el servidor público de búsqueda.
- Federado: datos de contacto visibles en la instancia local, en los contextos públicos pertinentes
  y en los servidores federados de confianza.
- Publicado: datos de contacto visibles en la instancia local, en los contextos públicos pertinentes,
  en los servidores federados de confianza, y publicados en el servidor público de búsqueda.

:::{note}
**Servidor público de búsqueda**: un directorio público que se usa para encontrar usuarios entre instancias de Nextcloud.
Solo pueden exponerse allí los campos del perfil marcados como Publicado.
:::

:::{note}
No todos los campos pueden publicarse en el servidor de búsqueda, aunque su ámbito sea
`Published`. Algunos campos no se publican nunca, de forma intencionada (por ejemplo Biografía,
Título, Organización, Cargo, Fecha de nacimiento).

Dicho de otro modo: `Published` es necesario, pero no siempre suficiente, para publicarse en el servidor de búsqueda.
:::

:::{important}
Un perfil accesible no significa que todos sus atributos sean públicos. Cada atributo se
filtra por su propio ámbito, y la visibilidad efectiva también puede depender de la
función que lo consume.
:::

:::{important}
En las superficies del perfil, la visibilidad efectiva es la más restrictiva entre los
ajustes de visibilidad del perfil y el ámbito de la propiedad.
:::

#### Matriz de visibilidad por ámbito

| Ámbito | El propio usuario [1] | Otros usuarios de la misma instancia local | Contextos públicos (según la función) | Federación de confianza | Servidor público de búsqueda |
|---|---|---|---|---|---|
| Privado | Sí | Limitado en las superficies del perfil: requiere estar autenticado y una relación de usuario conocido [3] | No | No | No |
| Local | Sí | Sí | Sí (donde corresponda) [2] | No | No |
| Federado | Sí | Sí | Sí (donde corresponda) [2] | Sí | No |
| Publicado | Sí | Sí | Sí (donde corresponda) [2] | Sí | Sí |

Notas:

1. El ámbito rige sobre todo la exposición a otros; el acceso del titular sigue el comportamiento de la cuenta o del endpoint.
2. La visibilidad en contextos públicos depende de la ruta de la función; el ámbito por sí solo no garantiza que se muestre.
3. Algunas superficies ajenas al perfil pueden excluir por completo las propiedades con ámbito Privado (por ejemplo,
   las tarjetas generadas de la libreta de direcciones del sistema), incluso para usuarios autenticados.

:::{note}
La matriz describe el **comportamiento de la visibilidad del perfil**. Otras funciones que consumen estos datos pueden aplicar
filtros adicionales y pueden no exponer en absoluto las propiedades con ámbito Privado.
:::

#### Regla de usuario conocido para el ámbito `Private`

Para las propiedades `Private`, Nextcloud puede permitir la visibilidad en rutas concretas de funciones locales
solo cuando quien hace la petición se considera un *usuario conocido* del usuario de destino.

En la práctica, esta relación se obtiene mediante la *coincidencia de contactos conocidos* del lado del servidor.
En las versiones actuales de Nextcloud, esta coincidencia se establece principalmente mediante la **coincidencia de
números de teléfono** (por ejemplo, a través de la integración de contactos de la app móvil de Talk), y es direccional
(por ejemplo, Alice puede ser conocida para Bob, pero Bob no es necesariamente conocido para Alice).
Los usuarios siempre son conocidos para sí mismos.

#### Qué pueden ver los usuarios locales

Una pregunta habitual es qué puede ver un usuario sobre otro usuario de la misma instancia.

En general, la visibilidad del perfil la controla el ámbito de cada propiedad, pero la
superficie exacta de la interfaz o de la API depende de la función que consume los datos (por ejemplo, la página de perfil,
los diálogos de compartir, la búsqueda, las menciones, Contactos y otras integraciones).

Para los usuarios locales de la misma instancia:

- `Private`: no es visible en general para todos los usuarios locales; en las rutas aplicables, la visibilidad
  se restringe a los usuarios autenticados que cumplen la relación de usuario conocido
  y otras restricciones de la función.
- `Local`: visible en la instancia local.
- `Federated`: visible en la instancia local (y también compartido con los servidores federados de confianza).
- `Published`: visible en la instancia local (y también en la federación y en el servidor público de búsqueda).

:::{note}
La exposición en la libreta de direcciones del sistema tiene en cuenta el ámbito y el contexto: las propiedades con ámbito privado o vacío se excluyen de las tarjetas generadas, y
las lecturas federadas eliminan las propiedades con ámbito local.
:::

#### Cómo verificar el comportamiento de los ámbitos

Como la visibilidad efectiva puede variar según la ruta de la función, los administradores deberían verificar
el comportamiento de los ámbitos en su propio despliegue.

Procedimiento de prueba recomendado:

1. Crear usuarios de prueba:

   - `alice` (titular del perfil de destino)
   - `bob` (usuario local autenticado)
   - `charlie` (segundo usuario local, de control)

2. Como `alice`, establecer valores de prueba distintos en los campos del perfil y asignar ámbitos
   diferentes donde sea posible (por ejemplo, Privado frente a Local desde la interfaz, y Federado/Publicado
   mediante la API o herramientas administrativas, si el despliegue lo admite).

3. Verificar como `alice`:

   - Confirmar que los valores visibles para el titular son los esperados.

4. Verificar como `bob` (usuario local autenticado):

   - Revisar las rutas de funciones que se usan en la instancia (por ejemplo, la página de perfil,
     la tarjeta de usuario, el diálogo de compartir, la búsqueda, las menciones, las integraciones de Contactos).
   - Confirmar que los campos `Local/Federated/Published` son visibles donde se espera.
   - Confirmar que los campos `Private` solo son visibles en las rutas que cumplen la relación de usuario conocido
     y otras restricciones de la función.

5. Verificar como usuario no autenticado (sesión privada del navegador):

   - Confirmar que solo son visibles los campos adecuados para el público.

6. Verificar el comportamiento de la federación y la publicación (si están activadas):

   - Desde un servidor federado de confianza, confirmar el comportamiento de Federado/Publicado.
   - Confirmar que solo los campos Publicado se exponen al servidor público de búsqueda.

7. Repetir la prueba con un usuario recién creado después de cambiar
   `account_manager.default_property_scope`:

   - Confirmar que los nuevos valores predeterminados solo se aplican a las cuentas recién inicializadas.
   - Confirmar que los usuarios existentes conservan los ámbitos guardados salvo que se cambien explícitamente.

#### Valores predeterminados de los ámbitos y precedencia

La visibilidad se determina por propiedad en este orden:

1. **Valores predeterminados del servidor**, de `OC\Accounts\AccountManager::DEFAULT_SCOPES`.
2. **Sustitución de los valores predeterminados por el administrador**, mediante `account_manager.default_property_scope`.
3. **Valor establecido por el usuario** en los ajustes personales o del perfil (sujeto a las restricciones del servidor).

Consecuencias prácticas:

- Las sustituciones del administrador en `account_manager.default_property_scope` se aplican al
  inicializar la cuenta y, por tanto, afectan a los **usuarios nuevos**.
- Los usuarios existentes conservan los ámbitos ya guardados salvo que se cambien explícitamente.
- `PROPERTY_DISPLAYNAME` y `PROPERTY_EMAIL` no pueden ser `Private`; la validación y la
  aplicación del lado del servidor exigen al menos `Local`.

#### Valores de ámbito predeterminados (referencia)

Los valores predeterminados se definen en el código del servidor y pueden cambiar con el tiempo. La fuente
de referencia es la constante `DEFAULT_SCOPES` de `OC\Accounts\AccountManager`: [código fuente más reciente](https://github.com/nextcloud/server/blob/master/lib/private/Accounts/AccountManager.php).

Valores predeterminados de ejemplo (verificarlos con la versión desplegada):

| Propiedad | Ámbito de visibilidad predeterminado |
|---|---|
| Nombre mostrado | Federado |
| Dirección | Local |
| Sitio web | Local |
| Correo electrónico | Federado |
| Avatar | Federado |
| Teléfono | Local |
| Twitter | Local |
| Bluesky | Local |
| Fediverso | Local |
| Organización | Local |
| Cargo | Local |
| Título | Local |
| Biografía | Local |
| Fecha de nacimiento | Local |
| Pronombres | Federado |

#### Sustituir los ámbitos predeterminados en `config.php`

Para sustituir uno o varios ámbitos de visibilidad predeterminados para los *usuarios nuevos*, usar
`account_manager.default_property_scope` (valor predeterminado: matriz vacía):

```php
'account_manager.default_property_scope' => [
  \OCP\Accounts\IAccountManager::PROPERTY_PHONE => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
  \OCP\Accounts\IAccountManager::PROPERTY_ROLE => \OCP\Accounts\IAccountManager::SCOPE_FEDERATED,
]
```

En el ejemplo anterior, el teléfono y el rol se sustituyen por `Private` y
`Federated`, respectivamente.

:::{note}
Usar las constantes de `\OCP\Accounts\IAccountManager` tanto para las claves de propiedad como para los valores de ámbito.
:::

#### Preguntas frecuentes: cómo restringir la visibilidad del perfil

Si el objetivo es la máxima privacidad:

1. Desactivar los perfiles de forma global (la opción más estricta):

   ```php
   'profile.enabled' => false,
   ```

   Efecto:

   - Se elimina la funcionalidad de perfil.
   - Las funciones de descubrimiento y de usabilidad basadas en el perfil se reducen en consecuencia.

2. Si los perfiles deben seguir activados, establecer valores predeterminados restrictivos para los usuarios nuevos:

   ```php
   'account_manager.default_property_scope' => [
     \OCP\Accounts\IAccountManager::PROPERTY_ADDRESS => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_PHONE => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_WEBSITE => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_TWITTER => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_BLUESKY => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_FEDIVERSE => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_ORGANISATION => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_ROLE => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_HEADLINE => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_BIOGRAPHY => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_BIRTHDATE => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_PRONOUNS => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
     \OCP\Accounts\IAccountManager::PROPERTY_AVATAR => \OCP\Accounts\IAccountManager::SCOPE_PRIVATE,
   ]
   ```

   Notas:

   - `PROPERTY_DISPLAYNAME` y `PROPERTY_EMAIL` no pueden establecerse en `Private`; la aplicación del lado del servidor exige al menos `Local`.
   - Los valores predeterminados se aplican a los **usuarios nuevos**. Los usuarios existentes conservan los ámbitos guardados salvo que se cambien.

##### ¿Qué queda limitado al restringirla?

Con ámbitos más restrictivos (sobre todo `Private`), cabe esperar menos visibilidad en:

- El descubrimiento de usuarios, la búsqueda y las tarjetas de usuario
- Los diálogos de compartir y el contexto de menciones y autocompletado
- Los contextos públicos o relacionados con compartir en los que pueden mostrarse metadatos de la cuenta
- La visibilidad federada de los atributos del perfil
- La publicación en el servidor público de búsqueda (allí solo aparece `Published`)

En resumen: una privacidad más estricta reduce la comodidad y la capacidad de descubrimiento basadas en el perfil.

### Ámbitos y usuarios existentes

El ajuste `account_manager.default_property_scope` solo se aplica a los usuarios **nuevos**.
Los usuarios existentes conservan sus ámbitos guardados.

Actualmente no existe ningún mecanismo de administración para cambiar en bloque los ámbitos de los usuarios
existentes. La API de aprovisionamiento OCS solo permite a los usuarios cambiar sus **propios** ámbitos: los administradores no pueden establecer ámbitos en nombre de otros usuarios.

Los usuarios pueden actualizar sus propios ámbitos en **Ajustes personales** → **Información personal** →
**Editar la visibilidad de su perfil**, o mediante la API:

```
curl -s -u alice:password -X PUT \
  "https://cloud.example.com/ocs/v2.php/cloud/users/alice" \
  -H "OCS-APIRequest: true" \
  -d "key=phoneScope&value=v2-private"
```

La clave de ámbito es el nombre de la propiedad seguido de `Scope`. Claves disponibles:

`displaynameScope`, `emailScope`, `phoneScope`, `addressScope`,
`websiteScope`, `twitterScope`, `blueskyScope`, `fediverseScope`,
`organisationScope`, `roleScope`, `headlineScope`, `biographyScope`,
`birthdateScope`, `avatarScope`, `pronounsScope`

Valores de ámbito permitidos:

- `v2-private` — Privado
- `v2-local` — Local
- `v2-federated` — Federado
- `v2-published` — Publicado

:::{note}
`displaynameScope` y `emailScope` no pueden establecerse en `v2-private`.
El servidor impone como mínimo `v2-local` para estas propiedades.
:::

### Véase también

- {nc-doc}`admin_manual/configuration_files/file_sharing_configuration` — ajustes de uso compartido y de autocompletado que interactúan con la visibilidad del perfil
- [Manual de usuario: ajustes personales](https://docs.nextcloud.com/server/latest/user_manual/en/userpreferences.html) — ajustes de perfil e información personal para los usuarios
````
