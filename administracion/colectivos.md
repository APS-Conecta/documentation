---
tipo: guia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Collectives en el servidor: apps necesarias, group_everyone, invitados, recursos compartidos públicos, contenido inicial, grupos e importación de Markdown."
---
# Cuadernos (Collectives)

## Resumen

Esta página reúne lo que la administración del servidor necesita para Collectives: las apps de las que depende, su uso con group_everyone, con usuarios invitados y con recursos compartidos públicos, el contenido inicial de los colectivos nuevos, los grupos en los colectivos y la importación de archivos Markdown, también desde Dokuwiki. Está dirigida a quienes administran el servidor.

````{upstream} admin_manual/collectives/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/colectivos

### Dependencias en tiempo de ejecución

Collectives requiere que estén activadas las siguientes apps. Todas se incluyen y se activan de forma predeterminada con la instalación del servidor Nextcloud:

- **Teams** (con Nextcloud >= 29) o **Circles** (con Nextcloud <= 28)
- **Text**
- **Viewer**
- **files_versions**

### Collectives y *group_everyone*

Al usar la [app group_everyone][group_everyone app], los usuarios existentes no verán los colectivos que tengan como miembro el grupo «everyone». Los miembros del grupo deben sincronizarse una vez en la app circles: `occ circles:sync --groups`

Esto solo hay que hacerlo una vez. Los usuarios nuevos que se crearon después de activar la app verán los colectivos de inmediato.

### Collectives y usuarios invitados

Para permitir que los usuarios invitados (tal como los proporciona la [app guests][guests app] accedan a los colectivos, añadir las apps Collectives y Teams a la lista de apps activadas para usuarios invitados en las configuraciones de administración.

Tener en cuenta que esto permite a los usuarios invitados crear colectivos nuevos.

### Recursos compartidos públicos

El acceso WebDAV a los recursos compartidos públicos no debe estar desactivado (es decir, debe estar activado) para que funcionen los colectivos compartidos públicamente. Comprobar que está activada la siguiente opción de administración: «Permitir a los usuarios en este servidor enviar recursos compartidos a otros servidores (esta opción también permite el acceso público vía WebDAV a los recursos compartidos públicos)» en «Compartir → Compartido en Nube Federada».

### Configuración

#### Contenido inicial para colectivos nuevos

Es posible crear contenido personalizado para los colectivos nuevos colocando archivos en el directorio de esqueleto de la app, en `data/app_<INSTANCE_ID>/collectives/skeleton`. Los colectivos nuevos empiezan con el contenido de este directorio.

Crear un archivo `Readme.md` para cambiar la página de inicio que se abre automáticamente al entrar en un colectivo.

Si el directorio de esqueleto no contiene un `Readme.md`, en su lugar se copiará en el directorio de los colectivos la página de inicio predeterminada de `apps/collectives/skeleton/Readme.md`.

### Permitir grupos en los colectivos

La app Teams puede configurarse para permitir añadir grupos a los equipos. Como la app Collectives depende de la app Teams para la gestión de usuarios, esto también permite añadir grupos completos a los colectivos.

Sin embargo, hay que tener en cuenta que, a diferencia de los equipos, los grupos solo pueden gestionarlos los administradores del servidor.

### Importar datos existentes

Es posible importar archivos Markdown existentes con el comando occ `occ collectives:import:markdown`.

El comando importa los archivos Markdown de un directorio como páginas nuevas en un colectivo. Después de importar todos los archivos, procesa los enlaces relativos y los adjuntos locales referenciados en los archivos Markdown. Intenta corregir los enlaces a otras páginas y sube los adjuntos referenciados cuando encuentra el archivo de origen en el directorio de importación.

Tener en cuenta que el comando consume mucha memoria. Al importar un directorio con muchos archivos Markdown, asegurarse de aumentar en consecuencia el límite de memoria de PHP:

```shell
php -d memory_limit=<X>G ./occ collectives:import:markdown -c <collectiveId> -u <userId> /path/to/markdown/files
```

#### Importar desde Dokuwiki

El comando de importación de directorios Markdown (ver arriba) admite importar archivos Markdown generados desde una instancia de Dokuwiki e intenta corregir los enlaces relativos a otras páginas y subir los adjuntos referenciados.

La importación está probada con archivos Markdown generados con la herramienta [Dokuwiki2Markdown][Dokuwiki2Markdown].

Este es un ejemplo de cómo importar desde una instancia de Dokuwiki:

```shell
/path/to/doku2md.py -d /path/to/dokuwiki/data/pages -T
php -d memory_limit=2G ./occ collectives:import:markdown -c 123 -u alice /path/to/dokuwiki/data/pages
```

[group_everyone app]: https://github.com/icewind1991/group_everyone/
[guests app]: https://github.com/nextcloud/guests/
[Dokuwiki2Markdown]: https://github.com/mm503/Dokuwiki2Markdown
````

## En APS Conecta Gestión

APS Conecta Gestión no instala Cuadernos (Collectives). La provisión instala un conjunto fijo de aplicaciones desde paquetes fijados y deja la tienda de aplicaciones desactivada, de modo que Cuadernos no se agrega desde la interfaz de administración. Los documentos de cada equipo viven en las carpetas de grupo de su área ([Archivos](../usuario/archivos/index.md)), y la información institucional, en la intranet ([Inicio](../usuario/inicio.md)).
