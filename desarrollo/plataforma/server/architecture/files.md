---
tipo: explicacion
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Cómo se organiza el sistema de archivos de Nextcloud: APIs Node y View, almacenamientos, caché, escáner, envoltorios y mapa del código."
---
# API del sistema de archivos de Nextcloud

## Resumen

Esta página explica cómo está construido el sistema de archivos de Nextcloud: la capa del sistema de archivos con sus API `Node` y `View`, la capa de almacenamiento con su caché y su escáner, los envoltorios de almacenamiento y de caché, y un mapa aproximado del código. Está dirigida a quienes desarrollan el servidor o sus apps.

````{upstream} developer_manual/server/architecture/files.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
### Visión general de alto nivel

El sistema de archivos de Nextcloud se basa, a grandes rasgos, en el sistema de archivos de unix: consta de varios almacenamientos montados en distintas ubicaciones.

```text
     ┌──────────────────────────────────┐
     │Code wanting to use the filesystem│
     └─────────┬─────────────────────┬──┘
               │                     │
               │                     │
┌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐
╎Filesystem    │                     │         ╎
╎layer         │new                  │legacy   ╎
╎              │                     │         ╎
╎              ▼                     ▼         ╎
╎      ┌────────┐ Partly build on  ┌─┴──────┐  ╎
╎      │Node API├─────────────────►│View API│  ╎
╎      └───────┬┘                  └─┬──────┘  ╎
╎              │                     │         ╎
└╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘
               │                     │
┌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐
╎Storage layer │                     │         ╎
╎              ├─────────────────────┤         ╎
╎              │                     │         ╎
╎              ▼                     ▼         ╎
╎        ┌───────┐    ┌───────┐    ┌──────┐    ╎
╎        │Storage│═══>│Scanner│═══>│Cache │    ╎
╎        └───────┘    └───────┘    └──────┘    ╎
╎                                              ╎
╎                                              ╎
└╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘
```

#### Capa del sistema de archivos

Todo código que quiera usar el sistema de archivos tiene dos opciones de API: la nueva API `Node` y la antigua API `View`. El código nuevo debería usar preferentemente la API `Node`, ya que permite construir sistemas con menos sobrecarga que la API antigua.

Además de las API del sistema de archivos, esta capa también gestiona los montajes disponibles: contiene la lógica que permite a las apps configurar sus montajes y la que traduce las rutas del sistema de archivos a un punto de montaje + una ruta «interna».

#### Capa de almacenamiento

La implementación del almacenamiento se encarga de los detalles de la comunicación con el sistema de archivos o con la API del almacenamiento remoto, y proporciona una API uniforme para que Nextcloud use el almacenamiento.

Para cada almacenamiento se mantiene una caché/índice de metadatos, que permite leer los metadatos del almacenamiento sin tener que comunicarse con el backend de almacenamiento (potencialmente) lento. El escáner se encarga de actualizar la caché con información del backend de almacenamiento.

### Envoltorios de almacenamiento/caché

Para que las apps puedan personalizar el comportamiento de un almacenamiento sin tener que implementarlo para cada backend de almacenamiento posible, se usa un sistema de `Wrapper`.

Un `Wrapper` encapsula un almacenamiento interno y permite sobrescribir cualquier método para personalizar su comportamiento; todos los demás métodos se pasan directamente al almacenamiento interno.

Por lo general, cada envoltorio de almacenamiento tiene un envoltorio de caché equivalente que encapsula la caché del almacenamiento interno, para aplicar las mismas modificaciones de comportamiento al leer metadatos desde la caché.

Los envoltorios pueden superponerse en capas para apilar sus comportamientos; por ejemplo, la app `groupfolders` funciona apilando un envoltorio que da acceso a una sola carpeta del almacenamiento raíz con un envoltorio que limita los permisos del almacenamiento.

```text
┌───────────────┐      ┌────────────────────┐
│PermissionsMask├─────►│CachePermissionsMask│  PermissionsMask applies a mask to the permissions of a storage
└───────┬───────┘      └─────────┬──────────┘  to provide less-privileged access to a storage
        │                        │
        ▼                        ▼
┌───────────────┐      ┌────────────────────┐
│Jail           ├─────►│CacheJail           │  Jail restricts access to a file or folder of a storage providing
└───────┬───────┘      └─────────┬──────────┘  a limited view into the storage (think unix chroot or bind mount)
        │                        │
        ▼                        ▼
┌───────────────┐      ┌────────────────────┐
│Base Storage   ├─────►│Base Cache          │
└───────────────┘      └────────────────────┘
```

### Mapa del código

Visión general aproximada del código relevante del sistema de archivos.

#### AppData

API de alto nivel para acceder a las carpetas «appdata», basada en la API `Node/SimpleFS`.

#### Cache

- Implementación de `Cache`
- Envoltorios de caché
- Escáner y lógica de actualización de la caché
- Infraestructura de búsqueda

#### Mount

Gestión y configuración de los puntos de montaje.

#### Node

Implementación de la API `Node` del sistema de archivos.

#### ObjectStorage

Implementación de los distintos backends de almacenamiento de objetos compatibles.

#### SimpleFS

Versión simplificada de la API Node, que ofrece una API más limitada para algunas partes del sistema de archivos.

#### Storage

Implementación de diversos backends de almacenamiento y envoltorios.

#### Streams

Diversos envoltorios de flujos de PHP de bajo nivel que se usan en las implementaciones de almacenamiento.

#### Type

Gestión y detección de tipos MIME.

#### View.php

API View heredada.
````
