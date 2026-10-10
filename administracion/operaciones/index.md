---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion, AIO]
resumen: "Mantenimiento de la plataforma base y su forma en APS Conecta Gestión: copias de borg, actualización por conjunto, re-provisión semanal y verificaciones."
---
# Operaciones

## Resumen

Esta sección reúne, para quienes administran el servidor, las páginas de la plataforma base sobre mantenimiento: copia de seguridad y restauración, actualización por sus distintas vías y migración a otro servidor. La sección «En APS Conecta Gestión», al final, describe cómo se mantiene una instalación de la suite en un centro.

````{upstream} admin_manual/maintenance/index.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
- {nc-doc}`admin_manual/maintenance/backup`
- {nc-doc}`admin_manual/maintenance/restore`
- {nc-doc}`admin_manual/maintenance/upgrade`
- {nc-doc}`admin_manual/maintenance/update`
- {nc-doc}`admin_manual/maintenance/manual_upgrade`
- {nc-doc}`admin_manual/maintenance/package_upgrade`
- {nc-doc}`admin_manual/maintenance/migrating`
- {nc-doc}`admin_manual/maintenance/migrating_owncloud`
````

## En APS Conecta Gestión

Un centro corre la suite sobre APS Conecta Gestión AIO. El asistente de instalación es dueño de los contenedores, un conjunto de 20 imágenes que avanza junto, y el paquete del servidor, `aps-conecta`, ejecuta las fases de provisión sobre la instancia en marcha. Por eso el mantenimiento que describen las páginas de esta sección toma en la suite la forma que sigue.

### Calendario

Estas son las tareas periódicas que la suite programa o configura; las horas son de Santiago salvo donde se indica.

| Tarea | Cuándo | Dueño |
|---|---|---|
| Copia de seguridad de la instancia | Todos los días a las 04:00 | El asistente de AIO (borg) |
| Trabajos diarios pesados de la plataforma | Sin ventana efectiva: la fase 06 fija las 5 UTC (01:00 en hora estándar de Chile), pero el valor dura solo hasta la copia diaria siguiente | La fase 06 y el entrypoint de AIO |
| Re-provisión | Domingos a las 03:00, con hasta 30 minutos de retraso aleatorio | El temporizador `aps-conecta.timer` de systemd |
| Refresco del mapa base | Día 4 de cada mes a las 05:00, con hasta 2 horas de retraso aleatorio | El temporizador `aps-conecta-tiles.timer` de systemd |

Los dos temporizadores son persistentes: un servidor apagado a la hora programada ejecuta la tarea pendiente al arrancar. Los trabajos en segundo plano corren por cron, no por ajax, porque con ajax solo corren cuando alguien carga una página; {doc}`/administracion/servidor/background-jobs-configuration` describe ambos modos. La ventana de los trabajos diarios tiene dos escritores: la fase 06 la fija en las 5 UTC, y el entrypoint de AIO escribe la misma clave, `maintenance_window_start`, con el valor 100, que equivale a no tener ventana, en cada arranque del contenedor. La copia diaria detiene los contenedores y los vuelve a arrancar, así que el valor de la fase rige solo desde la re-provisión del domingo hasta la copia siguiente; el resto de la semana, los trabajos pesados corren a cualquier hora, y cada re-provisión semanal vuelve a escribir esa clave.

### Copias de seguridad

La copia de la instancia es la de borg que trae el asistente; {doc}`backup` y {doc}`restore` describen la copia manual de la plataforma base, que la suite no usa.

- **Alcance.** El paso 7 del instalador programa la copia diaria en `/srv/aps-conecta/respaldos` y suma `/opt/aps-conecta`, con las credenciales selladas y el registro del sitio, a su alcance. La copia de borg es incremental, comprimida y cifrada.
- **La clave.** El asistente muestra la clave de cifrado de las copias. Sin ella, ninguna copia se restaura: guardarla en un lugar seguro.
- **El disco.** La carpeta de las copias está en el mismo disco que la instancia. Copiarla fuera del servidor, a un disco externo u otra máquina, es lo que protege ante la falla de ese disco.
- **La restauración.** Borg restaura la instancia desde el asistente. Los directorios adicionales se respaldan pero no se restauran con ella: `/opt/aps-conecta` se recupera a mano desde el archivo de borg, con la receta de la [documentación de AIO](https://github.com/nextcloud/all-in-one#pro-tip-backup-archives-access).
- **El mapa base.** El archivo del mapa, de 1,04 GB, queda fuera de la copia a propósito: el temporizador mensual lo regenera, y un gigabyte regenerable no debe viajar en cada copia.

### Actualizaciones

La suite se actualiza como un conjunto, con cada versión publicada, y nunca un componente por separado; las imágenes de una versión publicada no cambian. {doc}`update`, {doc}`manual-upgrade` y {doc}`package-upgrade` describen vías que la suite no usa:

- AIO desactiva el actualizador web de la plataforma.
- La aplicación de avisos de actualización queda restringida al grupo `admin`, porque anuncia actualizaciones que no se pueden aplicar sobre una imagen fijada.
- El asistente de la suite no ofrece actualizar su propio contenedor, y la casilla de actualización automática de su pantalla de copias se deja sin marcar.

Cada versión nueva se instala primero en un servidor de ensayo, exactamente como lo haría un centro, y ese ensayo es el registro de aceptación. Después de actualizar un centro, la revalidación corre tres verificaciones de solo lectura —humo, oficina y divergencia— y las informa todas, aunque una falle: el resultado es el conjunto. La guía clínica, en [«Tras actualizar»](https://github.com/APS-Conecta/gestion/blob/main/docs/GUIA-CLINICA.md#7-tras-actualizar), da el comando, y su sección 10 lista ocho revisiones manuales para cada actualización mayor.

### Re-provisión y estado

La re-provisión semanal vuelve a ejecutar la provisión sin intervención. Sobre una instancia convergida no escribe nada salvo la ventana de los trabajos diarios, que el contenedor reescribe en cada arranque, y su resultado es el de la verificación de divergencia: una instancia que se apartó de su declaración aparece como una unidad fallida en `systemctl --failed`. La convergencia nunca borra carpetas de equipo, grupos, cuentas ni archivos; sí retira los permisos que el archivo del sitio ya no declara, porque retirar un permiso no pierde nada. Lo que está vivo sin estar declarado queda en el informe de divergencia, junto con la orden que lo eliminaría.

Cuando una ejecución encuentra deriva o no termina, cada integrante del grupo `admin` recibe un aviso al iniciar sesión, uno por semana que reemplaza al anterior, y `aps-conecta estado`, sin sudo, muestra el último veredicto con cada hallazgo y su arreglo. La misma ejecución semanal renueva, 30 días antes de su vencimiento, el certificado de una instalación por IP.

### Migración

{doc}`migrating` describe el traslado de una instancia a otro servidor. En la suite, un centro que corre la versión anterior, sobre Docker Compose, pasa a AIO solo con la herramienta de [MIGRATION.md](https://github.com/APS-Conecta/gestion/blob/main/docs/MIGRATION.md), ensayada antes contra un servidor desechable. Una copia hecha por un Nextcloud AIO estándar no se restaura en la suite.

### Compromisos y límites

- **Objetivos de recuperación.** No hay tiempos ni puntos de recuperación (RTO/RPO) definidos: el documento de arquitectura los mantiene diferidos, con el resto de la postura de producción, en [gestion#75](https://github.com/APS-Conecta/gestion/issues/75).
- **Hora de la copia.** El asistente corre en UTC, así que el instalador publica la hora UTC que corresponde a las 04:00 de Santiago el día de la instalación. Después del siguiente cambio de horario, la copia corre a las 03:00 o a las 05:00; para moverla, la sección de copias del asistente recibe una hora nueva en UTC.
- **Ventana de los trabajos diarios.** El entrypoint de AIO reemplaza en cada arranque la ventana que fija la fase 06 por el valor 100, y la copia diaria reinicia los contenedores: la ventana de las 5 UTC rige solo entre la re-provisión del domingo y la copia siguiente. Ningún registro de errores de la suite lo recoge todavía.
- **Centros sin conexión.** Al arrancar con una imagen nueva, un centro sin red queda esperando la consulta a la tienda de aplicaciones, que es comportamiento de la plataforma base y termina cuando la consulta vence o vuelve la red.
- **Instalaciones antiguas.** Una instalación de la versión 0.3.0 o anterior usa los nombres de contenedor de AIO original y no se actualiza: se reinstala.
- **La CA del instalador.** La CA que firma el certificado de una instalación por IP dura 3650 días y nada la renueva; si falta, la ejecución semanal se detiene hasta restaurarla desde la copia diaria.

```{toctree}
:maxdepth: 1
:glob:

*
*/index
```
