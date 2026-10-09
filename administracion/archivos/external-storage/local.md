---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Montar un directorio del propio servidor como almacenamiento externo local: riesgo de seguridad, propiedad y permisos, y campos del formulario."
---
# Local

## Resumen

Esta página explica cómo montar como almacenamiento externo local un directorio del propio servidor que esté fuera del directorio de datos: el riesgo que implica, la propiedad y los permisos que necesita, y los campos que hay que rellenar. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/configuration_files/external_storage/local.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Los almacenamientos locales dan acceso a cualquier directorio del servidor Nextcloud. Como esto supone un riesgo de seguridad importante, el almacenamiento local solo puede configurarse en los ajustes de administración de Nextcloud. Los usuarios que no son administradores no pueden crear montajes de almacenamiento local.

Sirve para montar cualquier directorio del servidor Nextcloud que esté fuera del directorio `data/` de Nextcloud. El usuario del servidor HTTP debe poder leer y escribir en este directorio. Estos ejemplos de propiedad y permisos son para Ubuntu Linux:

```
sudo chown -R www-data:www-data /path/to/localdir
sudo chmod -R 0750 /path/to/localdir
```

Importante: si se usan comandos consecutivos, asegurarse de ser el usuario `www-data`:

```
sudo -E -u www-data bash
cd /path/to/localdir
mkdir data
```

En el campo **Nombre de la carpeta**, introducir el nombre de carpeta que se quiere que aparezca en la página Archivos de Nextcloud.

En el campo **Configuración**, introducir la ruta completa del directorio que se quiere montar.

En el campo **Disponible para**, introducir los usuarios o grupos que tienen permiso para acceder al montaje. De forma predeterminada, todos los usuarios tienen acceso.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage_configuration_gui` para ver más opciones de montaje e información.

Consultar {nc-doc}`admin_manual/configuration_files/external_storage/auth_mechanisms` para obtener más información sobre los esquemas de autenticación.
````
