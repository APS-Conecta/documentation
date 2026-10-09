---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cifrado en el servidor (SSE): alcance y límites, modos de clave, activación, comandos occ, descifrado, claves de recuperación y solución de problemas."
---
# Cifrado en el servidor

## Resumen

Esta página explica el cifrado en el servidor (SSE) integrado: en qué se diferencia de otros métodos de cifrado, sus límites, los modos de gestión de claves, cómo activarlo, cifrar y descifrar todos los archivos con `occ`, las claves de recuperación y la solución de problemas habituales. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/encryption_configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Visión general

Nextcloud ofrece varios métodos de cifrado para proteger los datos. Actúan en distintas capas del sistema y responden a distintas necesidades de seguridad. Esta guía se centra en el cifrado en el servidor (SSE) integrado en Nextcloud.

:::{note}
El cifrado y la gestión de riesgos son un tema complejo y lleno de matices. Salvo que ya se tenga experiencia en la materia, se recomienda consultar a un profesional o estudiarlo a fondo para asegurarse de que el enfoque elegido responde a las preocupaciones concretas. También puede resultar útil esta entrada del blog de {vendor}`Nextcloud`: [Métodos de cifrado de datos en Nextcloud](https://nextcloud.com/blog/encryption-in-nextcloud/). Ofrece una buena visión general de alto nivel de los distintos enfoques que suelen considerarse al usar Nextcloud.
:::

### Definiciones

- **Cifrado en el servidor (SSE):** lo realiza el servidor Nextcloud y protege los archivos en reposo en el almacenamiento local y externo. Las claves de cifrado se guardan en el servidor.
- **Cifrado de extremo a extremo (E2EE):** lo realizan los clientes de escritorio o móviles de Nextcloud antes de subir los archivos. Solo el cliente puede descifrarlos, lo que hace que los datos sean inaccesibles para los administradores del servidor y los proveedores de almacenamiento externo.
- **Clave maestra:** una clave central controlada por el servidor que se usa para cifrar todos los archivos.
- **Claves de usuario:** cada usuario tiene su propia clave, protegida por su contraseña, para cifrar sus archivos.
- **Clave de recuperación:** una clave definida por el administrador para recuperar archivos si los usuarios pierden sus contraseñas.
- **Cifrado de disco/dispositivo de bloques:** un método para proteger todos los datos guardados en un dispositivo de almacenamiento físico cifrándolos a nivel de hardware o de sistema de archivos (normalmente con herramientas como LUKS en Linux), de modo que los datos solo son accesibles después de desbloquear el dispositivo con la clave o la contraseña correctas.

### Comparación de métodos de cifrado

| Método | Dónde se cifra | ¿Quién puede descifrar? | Protege frente a |
|---|---|---|---|
| SSE (clave maestra) | Servidor | Administradores y usuarios | Proveedores de almacenamiento externo |
| SSE (claves de usuario) | Servidor | Usuarios y administradores malintencionados | Proveedores de almacenamiento externo |
| SSE (claves de usuario con recuperación) | Servidor | Usuarios y administradores con la clave de recuperación | Proveedores de almacenamiento externo |
| E2EE | Cliente | Solo los usuarios | Administradores, proveedores de almacenamiento externo |
| Cifrado de disco/bloques | Servidor | Administrador del sistema operativo | Manipulación física, robo |

### Puntos clave y limitaciones

- Los métodos de cifrado no son intercambiables; cada uno está pensado para riesgos concretos.
- El **cifrado en el servidor (SSE)** sirve principalmente para proteger archivos en almacenamiento externo de terceros.
- El **cifrado de extremo a extremo (E2EE)** es para los casos en que los administradores del servidor no deben acceder a los datos.
- SSE **no** cifra los nombres de archivo ni las estructuras de carpetas, solo el contenido de los archivos.
- SSE no protege los datos frente a un servidor Nextcloud comprometido o un administrador malintencionado. Para esa amenaza, usar E2EE.
- SSE no puede revertirse desde la interfaz web de Nextcloud.
- Resolver problemas de SSE suele requerir acceso al comando `occ`. ¡Asegurarse de tenerlo antes de activar SSE!
- Perder las claves de cifrado o el secreto de la instancia provoca la pérdida permanente de los datos.
- Las cuotas de Nextcloud se basan en el tamaño de los archivos sin cifrar; los archivos cifrados con SSE pueden ser ~1 % más grandes (era un 35 % antes de Nextcloud 25).
- SSL/TLS (HTTPS) termina antes de que se cifren los archivos, por lo que estos pueden quedar expuestos en memoria entre SSL/TLS y el código de cifrado SSE de Nextcloud.
- Cuando los archivos de un almacenamiento externo están cifrados con SSE, no pueden compartirse directamente desde el proveedor de almacenamiento externo; solo pueden compartirse a través de Nextcloud, ya que la clave de descifrado nunca sale del servidor Nextcloud.
- Para el almacenamiento local, puede ser mejor usar otras herramientas de cifrado, como el cifrado de disco/dispositivo de bloques (p. ej., LUKS) que ofrece el sistema operativo. Protege frente a otras preocupaciones, como el robo del servidor físico, que no es el objetivo de SSE.

:::{warning}
SSE **no** cifra los nombres de archivo ni las estructuras de carpetas, solo el contenido de los archivos.
:::

:::{note}
No confundir el SSE de Nextcloud con SSE-C de S3 (también compatible).
:::

:::{versionchanged} 9.0.0
Nextcloud (desde la v9.0.0) admite el cifrado autenticado en todos los archivos cifrados nuevos. Consultar <https://hackerone.com/reports/108082> para los detalles técnicos.
:::

:::{tip}
Para una seguridad máxima, configurar el almacenamiento externo con «Comprobar si hay cambios: Nunca». Así Nextcloud ignora los archivos nuevos que no se añadieron a través de Nextcloud, lo que impide adiciones no autorizadas por parte de los administradores del almacenamiento externo. No usarlo si el almacenamiento está sujeto a cambios externos legítimos.
:::

### Antes de activar el cifrado

1. Leer esta guía completa y comprender los riesgos.
2. Hacer una copia de seguridad de la configuración de la instancia y de todas las claves de cifrado en un lugar seguro antes de continuar.
3. Decidir qué modo de gestión de claves se ajusta a las necesidades (ver más abajo).

(nc-encryption_configuration_key_management_modes)=
### Modos de gestión de claves

**Clave maestra (predeterminado):**

- Todos los archivos se cifran con una clave central controlada por el servidor.
- Los administradores pueden descifrar los archivos de cualquier usuario.
- **Las claves de recuperación no están disponibles en el modo de clave maestra.** Los archivos siguen siendo accesibles si un usuario olvida su contraseña, ya que están cifrados con la clave maestra, no con la contraseña del usuario.
- Recomendado para la mayoría de las implantaciones.

**Claves de usuario:**

- Los archivos de cada usuario se cifran con una clave protegida por contraseña.
- Los administradores no pueden descifrar (fácilmente) los archivos sin la contraseña del usuario, salvo que se haya definido una clave de recuperación.
- Si un usuario olvida su contraseña y no existe ninguna clave de recuperación, sus archivos se pierden.
- Este modo no funciona con todos los métodos de autenticación (p. ej., contraseñas de aplicación, inicio de sesión único) y solo se recomienda por compatibilidad con configuraciones antiguas.

**Cómo elegir:**

- Si se confía en los administradores del servidor, usar el modo de clave maestra.
- Si es necesario impedir que los administradores accedan a los archivos, usar E2EE.
- El modo de claves de usuario ofrece cierta protección frente a administradores del servidor malintencionados, pero tiene limitaciones.

**Para seleccionar el modo de claves de usuario:**

Ejecutar:

```bash
occ encryption:disable-master-key
```

antes de activar el cifrado.

### Activar el cifrado (paso a paso)

1. Ir a la sección **Cifrado en el servidor** de la página de administración.
2. Marcar **Habilitar cifrado en el servidor**.
3. Aparecerá un mensaje: «No se ha cargado el modulo de cifrado». Ir a la página de Apps y activar el módulo de cifrado predeterminado de Nextcloud.
4. Volver a la página de administración. El módulo aparecerá y quedará seleccionado automáticamente.
5. Cerrar sesión y volver a iniciarla para inicializar las claves de cifrado.
6. Opcional: desmarcar la casilla de cifrado del almacenamiento personal si se quieren mantener sin cifrar los archivos locales.

### Copias de seguridad

Las claves de cifrado se guardan en:

- `data/<user>/files_encryption` (claves por usuario)
- `data/files_encryption` (claves de todo el sistema y del almacenamiento externo)

### Cifrar puntos de montaje externos y carpetas de equipo

- Los administradores y sus usuarios pueden cifrar los puntos de montaje externos.

  - Establecer las opciones de cifrado en la configuración de montaje de cada almacenamiento externo.
  - Consultar {nc-ref}`Opciones de montaje <external_storage_mount_options_label>` en {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui`.

- Para cifrar las carpetas de equipo, ejecutar:

```bash
occ config:app:set groupfolders enable_encryption --value=true
```

:::{note}
Solo se cifrarán los archivos nuevos o actualizados de las carpetas de equipo.
:::

### Gestionar el cifrado con comandos occ

Esta es una tabla de referencia de los comandos occ habituales:

| Comando | Descripción |
|---|---|
| occ encryption:status | Mostrar el estado del cifrado y el módulo |
| occ encryption:enable | Activar el cifrado en el servidor |
| occ encryption:list-modules | Listar los módulos de cifrado disponibles |
| occ encryption:set-default-module [Module ID] | Seleccionar el módulo de cifrado predeterminado |
| occ encryption:encrypt-all | Cifrar todos los archivos de todos los usuarios |
| occ encryption:decrypt-all [user] | Descifrar todos los archivos (o los de un usuario) |
| occ encryption:show-key-storage-root | Mostrar la ubicación del almacenamiento de claves |
| occ encryption:change-key-storage-root [dir] | Mover el directorio de almacenamiento de claves |
| occ encryption:enable-master-key | Activar el modo de clave maestra |
| occ encryption:disable-master-key | Desactivar el modo de clave maestra |
| occ encryption:fix-encrypted-version | Corregir errores de firma incorrecta |
| occ encryption:fix-key-location [user] | Corregir errores de clave no encontrada |

:::{tip}
Consultar la sección {nc-ref}`Comandos de cifrado <encryption_label>` de la guía de referencia de `occ` para ver más ejemplos y detalles de los comandos `encryption`.
:::

**Ejemplo: mover las claves a un directorio nuevo (Ubuntu Linux):**

```bash
cd /your/nextcloud/data
mkdir keys
chown -R root:www-data keys
chmod -R 0770 keys
occ encryption:change-key-storage-root keys
```

### Cifrar todos los archivos

De forma predeterminada, al activar SSE solo se cifran los archivos nuevos y modificados. Para cifrar todos los archivos de todos los usuarios, ejecutar:

```bash
occ encryption:encrypt-all
```

- **Asegurarse de tener copias de seguridad antes de ejecutarlo.**
- El comando crea un par de claves para cada usuario y cifra sus archivos.
- Se muestra el progreso hasta que todos los archivos están cifrados.
- **Asegurarse de que ningún usuario accede a los archivos durante este proceso.**

(nc-occ_disable_encryption_label)=
### Descifrar archivos / desactivar el cifrado

- Solo es posible mediante occ.
- Primero, descifrar todos los archivos:

```bash
occ encryption:decrypt-all
```

- **Asegurarse de tener copias de seguridad antes de ejecutarlo.**
- El servidor entra en modo de mantenimiento. Si se interrumpe, volver a ejecutarlo hasta que termine.
- Si algunos archivos siguen cifrados, volver a ejecutar el comando después de resolver los problemas.
- **Advertencia:** desactivar el cifrado sin descifrar todos los archivos provocará errores impredecibles.

Se puede descifrar por usuarios individuales:

```bash
occ encryption:decrypt-all <user-id>
```

### Datos que no se cifran

Solo se cifra el contenido de los archivos. Lo siguiente **no** se cifra:

| No cifrado |
|---|
| Nombres de archivo y estructuras de carpetas |
| Archivos existentes en la papelera |
| Versiones históricas existentes de los archivos |
| Miniaturas de imágenes |
| Vistas previas de imágenes |
| Índice de búsqueda de texto completo |
| Datos de aplicaciones que no se basan en archivos (p. ej., Deck, Tables) |

### Claves de usuario: compartición y recuperación

**Compartir archivos cifrados:**

- Después de activar el modo de claves de usuario, los usuarios deben cerrar sesión e iniciarla de nuevo para generar sus claves.
- Los usuarios que vean «La aplicación de cifrado esta activada, pero sus credenciales no han sido iniciadas...» deben cerrar sesión y volver a iniciarla.
- Puede que haya que volver a compartir los archivos compartidos después de activar el cifrado.
  - Para recursos compartidos individuales: dejar de compartir el archivo y volver a compartirlo.
  - Para recursos compartidos con grupos: compartir con cada persona que no pueda acceder al recurso compartido y después eliminar esas comparticiones individuales.

**Activar las claves de recuperación de archivos:**

Las claves de recuperación solo están disponibles en el modo de claves por usuario (no en el modo predeterminado de clave maestra).

- Quien pierde su contraseña de Nextcloud pierde el acceso a sus archivos cifrados.
- Si un usuario pierde su contraseña, sus archivos no pueden recuperarse salvo que esté activada una clave de recuperación (solo en el modo de claves por usuario).
- Para activar la recuperación (en el modo de claves por usuario), ir a Cifrado en la página de administración y establecer una contraseña de la clave de recuperación.
- Los usuarios deben activar la recuperación de contraseña en sus ajustes personales para que la clave de recuperación funcione.
- En el caso de los usuarios que han activado la recuperación de contraseña, los administradores pueden restablecer las contraseñas y recuperar los archivos con la clave de recuperación.

:::{warning}
El proceso de recuperación puede ser lento y consumir muchos recursos, sobre todo en instancias con grandes cantidades de datos cifrados. Probar los procedimientos de recuperación antes de confiar en ellos en producción.
:::

### LDAP y otros backends de usuarios externos

- Si se usa LDAP/Samba y se cambian las contraseñas en el backend, los usuarios necesitarán tanto la contraseña antigua como la nueva en su siguiente inicio de sesión.
- Si la clave de recuperación está activada, los administradores pueden restablecer la contraseña a través de Nextcloud y avisar a los usuarios.

### Solución de problemas

#### ¿Por qué no aparece la opción de clave de recuperación en los ajustes de cifrado?

Las claves de recuperación solo están disponibles en el modo de claves por usuario. Desde Nextcloud 13, el modo de cifrado predeterminado usa claves maestras (cifrado de todo el sistema). El modo de clave maestra no muestra las opciones de clave de recuperación en los ajustes de administración porque las claves de recuperación no son necesarias: los administradores pueden restablecer las contraseñas de los usuarios y los archivos siguen siendo accesibles.

Si se usa el modo de clave maestra (el modo predeterminado y recomendado), no se necesitan claves de recuperación. Las claves de recuperación solo son relevantes en configuraciones con claves por usuario, que se mantienen por compatibilidad con implantaciones antiguas.

Consultar {nc-ref}`Modos de gestión de claves <encryption_configuration_key_management_modes>` para orientarse sobre las diferencias entre los modos de clave maestra y de claves por usuario, y la [incidencia n.º 8283 de GitHub](https://github.com/nextcloud/server/issues/8283) para el contexto técnico de esta decisión de diseño.

#### Clave privada no válida para la app de cifrado

Consultar la [incidencia n.º 8546 de GitHub](https://github.com/nextcloud/server/issues/8546) y la [solución provisional](https://github.com/nextcloud/server/issues/8546#issuecomment-514139714).

#### Error de firma incorrecta

En algunos casos poco frecuentes, los archivos cifrados no pueden descargarse y devuelven un «500 Internal Server Error». Si el registro de Nextcloud contiene un error sobre «Bad Signature», ejecutar el siguiente comando para reparar los archivos afectados:

```
occ encryption:fix-encrypted-version userId --path=/path/to/broken/file.txt
```

Sustituir «userId» y la ruta según corresponda. El comando realizará un descifrado de prueba de todos los archivos y reparará automáticamente los que tengan un error de firma.

(nc-troubleshooting_encryption_key_not_found)=
#### No se encuentra la clave de cifrado

Si los registros contienen un error que indica que no se encuentra la clave de cifrado, puede buscarse manualmente en el directorio de datos una carpeta con el mismo nombre que el archivo. Por ejemplo, si no puede descifrarse un archivo «example.md», ejecutar:

```
find path/to/datadir -name example.md -type d
```

Después, revisar los resultados situados en la carpeta `files_encryption`. Si la carpeta de claves está en una ubicación incorrecta, moverla a la carpeta correcta y volver a intentarlo.

La carpeta `data/files_encryption` contiene las claves de cifrado de las carpetas de grupo y de los almacenamientos externos de todo el sistema, mientras que `data/$userid/files_encryption` contiene las claves de los archivos del almacenamiento de un usuario concreto.

:::{note}
Esto puede ocurrir si el cifrado se desactivó en algún momento pero no se ejecutó el {nc-ref}`comando occ de decrypt-all <occ_disable_encryption_label>`. Si después alguien movió los archivos a otra ubicación, las claves no se movieron con ellos.
:::

#### No se encuentra la clave de cifrado con almacenamiento externo o carpetas de grupo

Para resolver este problema, ejecutar el siguiente comando:

```
sudo -E -u www-data php occ encryption:fix-key-location <user-id>
```

Esto intentará recuperar las claves que no se movieron correctamente.

Si así no se resuelve el problema, consultar la sección {nc-ref}`No se encuentra la clave de cifrado <troubleshooting_encryption_key_not_found>` para un procedimiento manual.

:::{note}
Había dos problemas conocidos por los que:

- mover archivos entre un almacenamiento cifrado y uno sin cifrar, como un almacenamiento externo o una carpeta de grupo, [no movía las claves junto con los archivos](https://github.com/nextcloud/groupfolders/issues/1896).
- colocar archivos en un almacenamiento externo de todo el sistema guardaba las claves en la [ubicación incorrecta](https://github.com/nextcloud/server/pull/32690).
:::

### Lecturas adicionales

- {nc-ref}`Referencia de comandos occ: cifrado <encryption_label>`
- [Cómo usa Nextcloud el cifrado para proteger los datos](https://nextcloud.com/blog/encryption-in-nextcloud/)
- [Impacto técnico del cifrado autenticado](https://hackerone.com/reports/108082)
- {nc-doc}`Detalles de la implementación de SSE de Nextcloud <admin_manual/configuration_files/encryption_details>`
- [Herramientas de recuperación del cifrado de Nextcloud (SSE y E2EE)](https://github.com/nextcloud/encryption-recovery-tools)
- [App Nextcloud E2EE Server API (necesaria para usar E2EE)](https://github.com/nextcloud/end_to_end_encryption/)
````
