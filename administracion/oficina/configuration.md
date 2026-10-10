---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Ajustes de la app Nextcloud Office y opciones adicionales de coolwsd: servidor, grupos, OOXML, apps externas, vistas previas, fuentes, vista segura y WOPI."
---
# Configuración

## Resumen

Esta página describe los ajustes de la app Nextcloud Office (servidor de Collabora Online, restricciones por grupo, OOXML, acceso de apps externas y raíz web canónica) y las opciones adicionales del servicio coolwsd: vistas previas, fuentes personalizadas, vista segura y restricción de las peticiones WOPI. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/office/configuration.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/oficina/index

### Ajustes de la app Nextcloud Office

#### Servidor de Collabora Online

URL (y puerto) del servidor de Collabora Online que proporciona la funcionalidad de edición como cliente WOPI. Collabora Online debe usar el mismo protocolo (`http://` o `https://`) que la instalación del servidor. Naturalmente, se recomienda `https://`.

#### Restringir el uso a grupos específicos

De forma predeterminada, la app está activada para todos. Cuando este ajuste está activo, solo los miembros de los grupos indicados pueden usar Nextcloud Office.

#### Restringir la edición a grupos específicos

De forma predeterminada, todos los usuarios pueden editar documentos con Nextcloud Office. Cuando este ajuste está activo, solo los miembros de los grupos indicados pueden editar; los demás solo pueden ver los documentos.

#### Usar OOXML de forma predeterminada para los archivos nuevos

De forma predeterminada, los archivos nuevos que crean los usuarios están en formato OpenDocument (ODF). Cuando este ajuste está activo, los archivos nuevos se crean en formato Office Open XML (OOXML).

#### Activar el acceso para apps externas

Nextcloud pasa internamente a Collabora Online un token de acceso que este usa después para realizar diversas operaciones. De forma predeterminada, terceros no pueden generar este token; solo Nextcloud puede generarlo y pasárselo a Collabora Online.

En algunas aplicaciones puede ser necesario que una aplicación de terceros genere el token. Para ello, hay que añadir la aplicación de terceros (apps externas) en este ajuste. Hay que añadir un identificador de aplicación y un token
secreto. Después, la aplicación de terceros puede usar estas credenciales para hacer llamadas a *ajax/extapp/data/{fileId}* y obtener el token de acceso y la URL de origen del fileId indicado, ambos necesarios para abrir una conexión con Collabora Online.

#### Raíz web canónica

Raíz web canónica que debe usar Collabora Online, en caso de que haya varias. Indicar la que tenga menos restricciones. Por ejemplo: usar la raíz web sin Shibboleth si a esta instancia se accede tanto por raíces web con Shibboleth como sin Shibboleth. Este ajuste puede ignorarse si solo se usa una raíz web para acceder a esta instancia.

### Opciones de configuración adicionales

El servicio coolwsd admite opciones de configuración adicionales, que se encuentran en la [documentación de Collabora Online](https://sdk.collaboraonline.com/docs/installation/Configuration.html).

#### Vistas previas

Para permitir que Nextcloud use la API de conversión de coolwsd para generar vistas previas, hay que añadir la IP del host de Nextcloud a la lista de permitidos:

```bash
sudo coolconfig set net.post_allow.host 10.0.0.4
```

#### Fuentes personalizadas

Al instalar el paquete coolwsd, el script posterior a la instalación busca fuentes adicionales en el sistema y las instala en la systemplate. Si se instalan fuentes en el sistema después de instalar coolwsd, hay que actualizar la systemplate manualmente.

```bash
coolconfig update-system-template
```

:::{seealso}
<https://sdk.collaboraonline.com/docs/installation/Fonts.html>
:::

#### Ajustes de vista segura

Los ajustes de vista segura permiten que Nextcloud incruste marcas de agua en los archivos de oficina. La marca de agua puede establecerse según distintas reglas:

- **Etiquetas:** pone marca de agua en los archivos que contienen las etiquetas definidas
- **Grupos:** pone marca de agua en los archivos cuando los abren usuarios que pertenecen a los grupos definidos.
- **Todos los recursos compartidos:** pone marca de agua en los archivos a los que se accede mediante un recurso compartido.
- **Recursos compartidos de solo lectura:** pone marca de agua en los archivos si se accede a ellos mediante un recurso compartido de solo lectura.

:::{warning}
Para garantizar la confidencialidad de los archivos, es fundamental restringir la posibilidad de descargar los documentos.

Esto incluye asegurarse de que la [configuración de WOPI](#wopi-configuration) esté configurada para servir documentos solo entre Nextcloud y Collabora.
:::

(wopi-configuration)=
#### Configuración de WOPI

Se recomienda encarecidamente restringir las peticiones WOPI a las direcciones IP de los servidores de Collabora que se espera que soliciten archivos a la instalación de Nextcloud. Esto puede hacerse estableciendo la opción `Allow list for WOPI requests` en las configuraciones de administración de Office.

Del mismo modo, se aconseja configurar la [configuración de host WOPI de Collabora](https://sdk.collaboraonline.com/docs/installation/Configuration.html#multihost-configuration) para que solo sirva a las IP de los hosts esperados.
````
