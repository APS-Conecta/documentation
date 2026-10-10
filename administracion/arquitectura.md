---
tipo: explicacion
audiencia: administracion
apps: [gestion]
resumen: "Las dos formas de la instalación, la pila de desarrollo y la de un centro: contenedores, datos, red, dominios de fallo y dimensionamiento."
---
# Arquitectura

## Contexto

La plataforma corre sobre la imagen oficial publicada por {vendor}`Nextcloud`, sin bifurcación del código fuente ni parches al núcleo.
El repositorio gestion agrega solo personalización declarativa: configuración, el tema del servidor y el aprovisionamiento de grupos, carpetas y permisos.
Las aplicaciones de terceros que la suite modifica reciben parches versionados en el repositorio, que el {doc}`aprovisionamiento </administracion/aprovisionamiento>` vuelve a aplicar en cada siembra; el núcleo nunca se parchea.
Las aplicaciones propias se instalan desde tarballs construidos a partir de etiquetas de su propio repositorio y llegan a la plataforma solo por las interfaces públicas `OCP\…`.
La instancia en ejecución es una proyección de esa receta sobre la imagen oficial: reproducible y desechable.

Cada instalación sirve a un solo establecimiento, y el repositorio no contiene datos de pacientes.
La plataforma no está pensada para guardarlos, pero nada impide que el personal suba archivos clínicos, así que cada cuenta, cada enlace compartido y cada respaldo se protegen como si los tuvieran.

La instalación existe en dos formas que ejecutan las mismas fases de aprovisionamiento:

- **La pila de desarrollo**: una pila de Docker Compose descrita en `compose.yaml`, desechable, que `make install` reconstruye en el equipo de quien desarrolla.
- **La instalación de un centro**: el instalador {doc}`AIO </administracion/aio>` es dueño del conjunto de contenedores, y el paquete de host de gestion ejecuta las fases contra él por `docker exec`.

Todavía no existe una instancia de producción: ningún centro corre una versión publicada.

## Diseño

### La pila de desarrollo

| Servicio | Imagen | Función |
|---|---|---|
| `nextcloud` | `nextcloud:34-apache` | Servidor de aplicaciones, interfaz web, archivos, cuentas y grupos. Publica `127.0.0.1:${HTTP_PORT}`. |
| `db` | `postgres:18-alpine` | Metadatos: cuentas, grupos, carpetas de grupo, permisos e índice de archivos. |
| `redis` | `redis:8-alpine` | Caché y bloqueo de archivos y transacciones. |
| `cron` | La misma imagen y los mismos volúmenes que `nextcloud`, por un ancla de Compose | Ejecuta `cron.php` según un horario y no según las visitas a páginas. |
| `eurooffice` | `ghcr.io/euro-office/documentserver:latest` | Servidor de documentos de la oficina, con JWT. Publica `127.0.0.1:${OFFICE_PORT}`. |

Cada imagen está fijada por su resumen `@sha256:`; la etiqueta queda solo para leerla.
`make images` renueva los resúmenes y el flujo semanal `image-digests` informa cuando una etiqueta avanzó más allá de su resumen fijado.
`nextcloud` y `cron` comparten imagen y volúmenes por construcción, porque `cron.php` carga las aplicaciones y necesita `custom_apps` y `themes`.
El servidor de documentos trae su propio PostgreSQL, Redis y RabbitMQ, y no se conecta a la base de datos ni a la caché del núcleo.
`apps/` y `themes/` se montan desde el repositorio sobre `custom_apps` y `themes`, para editar sin reconstruir.
Todos los servicios usan `restart: unless-stopped`: la pila vuelve sola después de un reinicio del host, y una pila detenida a propósito sigue detenida.

### La instalación de un centro

Un centro corre en un solo host Ubuntu o Debian x86-64, con Docker de API 1.44 o superior.
El contenedor `nextcloud-aio-mastercontainer` sirve el asistente en el puerto 8080 y administra los demás como un conjunto de 20 imágenes bajo `ghcr.io/aps-conecta/*` que se actualiza completo, nunca por partes.
Los contenedores de la suite se llaman `aps-conecta-*`.

| Contenedor | Función que gestion usa |
|---|---|
| `aps-conecta-apache` | Publica la suite en el puerto 443 y termina TLS; sirve el mapa base en `/tiles/` antes de pasar la petición al servidor de aplicaciones. |
| `aps-conecta-nextcloud` | Servidor de aplicaciones; el aprovisionamiento ejecuta `occ` dentro de él. `cron.php` corre aquí, en un ciclo de cinco minutos, porque la instalación AIO no tiene contenedor `cron`. |
| `aps-conecta-database` | PostgreSQL. |
| `aps-conecta-redis` | Redis, con contraseña. |
| `aps-conecta-eurooffice` | Servidor de documentos. |
| `aps-conecta-notify-push` | Servidor de push de la aplicación `notify_push`, que la pila de desarrollo no ejecuta. Sin el binario de la aplicación el contenedor termina con error, por eso gestion incluye su tarball para la imagen. |

El respaldo diario lo hace el contenedor de borg del propio instalador.
Las aplicaciones y el tema vienen incorporados en la imagen del servidor, con la tienda de aplicaciones apagada desde la imagen.

### Datos y su único dueño

| Dato | Dónde vive |
|---|---|
| Documentos del establecimiento | El volumen de datos de la plataforma; nunca en git. |
| Cuentas, grupos, carpetas de grupo, permisos, índice de archivos | PostgreSQL. |
| Caché y bloqueos | Redis, efímero. |
| Receta del estado deseado, tema, configuración | El repositorio gestion, sin datos de producto ni secretos. |
| Secretos de la pila de desarrollo | `.env`, generado con modo 600 y fuera de git. |
| Identidad, equipos, carpetas y matriz del establecimiento | `sites/<slug>/site.sh`, fuera de git. |
| Hoja de credenciales sellada y registro del sitio de un centro | `/opt/aps-conecta`, dentro del alcance del respaldo. |
| Mapa base | `/srv/aps-conecta/tiles/chile.pmtiles`, fuera del respaldo a propósito: se regenera. |

### Red

```text
Navegador ──▶ aps-conecta-apache :443 ──┬─ /tiles/  ──▶ /aps-tiles (solo lectura)
                                        └─ resto    ──▶ aps-conecta-nextcloud
aps-conecta-nextcloud ◀──▶ aps-conecta-database · aps-conecta-redis · aps-conecta-eurooffice
```

Entre contenedores, el tráfico va por nombre de servicio y nunca por `localhost` ni por un puerto publicado en el host.
En Compose, el conector usa `http://eurooffice/` para llegar al servidor de documentos, y el servidor de documentos usa `http://nextcloud/` para descargar el archivo; por eso `14-office` agrega `nextcloud` a `trusted_domains`, ya que la plataforma responde HTTP 400 a un host no confiable.
`host.docker.internal` queda reservado para el sentido contenedor a host, y en Linux requiere la asociación `host-gateway`.
La pila de desarrollo publica sus dos puertos solo en `127.0.0.1` y no se expone a la red local; cuando un proxy los publica hacia afuera, `OFFICE_PUBLIC_URL` lleva la URL pública del editor.
En un centro, el puerto interno 23973 de `aps-conecta-apache` es el tramo que usan, dentro de la red de la suite, la revisión del mapa base y, en una instalación por IP, el servidor de documentos.
El navegador recorre dos tramos propios: la URL pública del editor (`DocumentServerUrl`) y el archivo del mapa base, en el mismo origen que la página.

### Dominios de fallo

- **Una fase de aprovisionamiento**: detiene la siembra con su nombre, sin ejecutar las fases siguientes; la misma orden la reintenta y salta lo ya aplicado.
- **Base de datos o caché**: en Compose, `nextcloud` y `cron` no arrancan hasta que `db` y `redis` responden sanos.
- **Servidor de documentos**: su caída deja sin edición de documentos y no toca el resto; `make office-down` lo detiene solo, a propósito, en la pila de desarrollo.
- **Mapa base**: sin el archivo, `/tiles/` responde 404 sin llegar al servidor de aplicaciones, y la suite sigue sana: nada depende del archivo.
- **Programador de tareas**: sin `cron`, las tareas vuelven a depender de las visitas y la limpieza se detiene cuando nadie navega.
- **Red externa**: al arrancar con una imagen nueva, un centro sin conexión espera en la consulta a la tienda de aplicaciones hasta que esa consulta vence o la red vuelve.
- **Deriva**: la re-provisión semanal falla como unidad de systemd, notifica al grupo `admin` en su siguiente inicio de sesión y deja el veredicto en `aps-conecta estado`.

### Dimensionamiento

- El servidor de documentos ocupa unos 2,5 GB y recomienda cerca de 8 GB de RAM para uso multiusuario; como forma parte de la pila, ese piso rige para todo host de centro y todo equipo de desarrollo.
- La revisión del host antes de instalar exige 8 GiB de RAM y 40 GB de disco libre.
- La integración continua mide la suite en reposo en cerca de 1,1 GiB.
- El archivo del mapa base ocupa 1,04 GB.
- El instalador ajusta Talk a la memoria y los núcleos del servidor.

## Compromisos y límites

- **El repositorio no tiene respaldo propio.** El de un centro es el borg del instalador: el paso 7 lo programa diario a las 04:00 de Santiago, pero el asistente guarda la hora en UTC, así que después de cada cambio de horario corre a las 03:00 o a las 05:00; vive en `/srv/aps-conecta/respaldos`, en el mismo disco, y hay que copiarlo fuera del servidor. Los directorios adicionales se respaldan, pero no se restauran con la instancia.
- **Quedan diferidos**, hasta que exista un host de destino: el proxy inverso con TLS y lista de acceso para el servidor de documentos, los objetivos de recuperación, el dimensionamiento y la alta disponibilidad, y la observabilidad de producción (#75).
- **El servidor de documentos usa un secreto JWT compartido** con el conector.
- **En la pila de desarrollo, Talk** consulta un servidor STUN externo por defecto, y como esa pila no ejecuta un servidor de señalización de alto rendimiento, las llamadas grupales dejan de ser usables con unas cuatro personas.
- **El tema del servidor** se apoya en un mecanismo sin documentación oficial y se vuelve a verificar en cada versión mayor.
- **El servidor de documentos no publica etiquetas de versión**: su imagen se fija por resumen sobre `latest`.
- **El flujo de actividad** puede mostrar nombres de elementos ocultos por permisos; los nombres sensibles no van en subcarpetas restringidas.
- **En Compose, el registro** está en `data/nextcloud.log`, dentro del volumen `nextcloud_data`, y rota a los 100 MiB por el valor heredado de la imagen.
