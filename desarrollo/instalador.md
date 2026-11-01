---
tipo: referencia
audiencia: desarrollo
apps: [gestion, files-upload-guard, files-fulltextsearch]
resumen: "El repositorio de la suite: el fork de AIO en un solo árbol, el paquete del host, el Provisionador, el manifiesto de aplicaciones y la publicación firmada."
---
(instalador)=
# Instalador de APS Conecta Gestión

## Resumen

El repositorio [APS-Conecta/gestion](https://github.com/APS-Conecta/gestion) reúne el fork de AIO, el paquete del anfitrión, el Provisionador y el manifiesto de aplicaciones. El desarrollo avanza en un solo árbol sobre `main`.

```{note}
Los cambios del plan de actualización corresponden a la próxima versión. Consulte su estado en {doc}`/proyecto/novedades/instalador` y seleccione una versión publicada para instalar.
```

Cada versión vincula un commit, las imágenes y el paquete firmado. Las aplicaciones adicionales llegan por el canal declarado en `apps.json`: publicación firmada o instalación acotada desde la tienda.

## Tabla

| Verificación | Entrada | Resultado esperado |
|---|---|---|
| Compuerta local | `bash scripts/test.sh` | Pruebas estáticas y autopruebas completas |
| Marca y adquisición | `bash scripts/brand-gate.sh .` y `bash scripts/acquisition-gate.sh .` | Identidad, funciones admitidas y canales de instalación coherentes |
| Validadores | `bash scripts/validate.sh .` | Ortografía, Dockerfiles y definiciones válidas |
| Inventario de construcción | `python3 scripts/images.py build-matrix` | Todos los Dockerfiles de ejecución, derivados del inventario |
| Imágenes publicadas | `python3 scripts/images.py verify VERSION --sha COMMIT` | Resúmenes y etiquetas de origen correspondientes al commit fijado |
| Instalación limpia | `cleanboot.yml` | Instalación, reinicio, provisión repetida, recuperación y actualización verificadas |
| Aceptación publicada por IP | `acceptance.yml` | Instalación desde la URL pública de una versión, con veredictos y evidencias |
| Publicación | `release.yml` | Compuertas completas, procedencia, firmas y contenido comprobados |

## Notas

(el-paquete-es-el-arbol-de-la-etiqueta)=
### Construcción y procedencia

`images.yml` fija un commit y construye todas las imágenes de ejecución desde ese árbol. PostgreSQL se prueba antes de publicar; la comprobación confirma que las capas publicadas son las probadas. El manifiesto registra el origen y el resumen de cada imagen.

Una versión publicada conserva sus resúmenes. La opción `--force` corresponde a conjuntos todavía inéditos. El paquete se obtiene con `git archive` del commit fijado.

La consulta al registro admite manifiestos Docker y OCI y sus índices. La compuerta local comprueba el método nativo con ambos formatos y con un registro inaccesible.

### Aplicaciones oficiales

Euro-Office, Talk y Custom Menu utilizan sus paquetes oficiales de tienda y conservan la firma del proveedor. APS Conecta configura la integración y comprueba su funcionamiento. El proveedor de búsqueda mantiene la corrección temporal de identidad de la ADR-0023 hasta su publicación oficial. IntraVox aporta el montaje configurable y la importación que conserva el contenido del personal.

`scripts/releases.py` valida la firma y la compatibilidad de cada versión fijada (`pin`), con la versión registrada en `apps.lock.json` como mínimo. Antes de guardar o reutilizar un paquete, exige su directorio de aplicación y rechaza rutas absolutas, segmentos `..` y enlaces simbólicos o duros.

### Actualización y alcance del respaldo

`actualizar` comprueba el estado de cada lectura y operación de la fase 12 antes de continuar. Un fallo identifica la aplicación, elimina el candado candidato y conserva `apps.lock.json`. La configuración se valida como JSON antes de guardarse en memoria; el diagnóstico conserva privados sus valores.

La autoprueba del anfitrión ejecuta la aplicación real con comandos de frontera simulados. Cubre fallos de habilitación, instalación oficial, configuración de Talk y lecturas de versiones, configuración y manifiesto. El asistente envía el alcance adicional del respaldo con `APS_HOME`; esa solicitud concentra su configuración.

### Permisos para compartir documentos

`deis.write_site` genera la matriz `SITE_ACL` para la consola y el Provisionador. La fase 40 aplica las concesiones mediante el mismo módulo de carpetas. Los grupos responsables reciben gestión y compartición; las jefaturas reciben lectura y compartición en unidades con otro cargo responsable. `all-staff` conserva lectura en `Transversal`.

La autoprueba del Provisionador comprueba la matriz generada por su API. Clean boot por IP compara cada concesión con el estado nativo, comprueba la identidad de cuentas sin administración y comparte un documento existente de la biblioteca mediante la API oficial. Otra cuenta verifica la identidad del archivo adjunto en la conversación. La revalidación comprueba la divergencia de los inventarios.

### Firma y credenciales

El entorno `Release` contiene `MINISIGN_SECRET_KEY` y `MINISIGN_KEY_PASSWORD`. Cada paso recibe únicamente la credencial que consume. Conserve `installer.pub` en el repositorio como clave pública de verificación.

Nextcloud verifica la firma del paquete oficial de Talk al instalarlo. Las etiquetas de ensayo `v0.0.0-ci.N` se publican como preliminares y conservan la versión estable marcada como más reciente. El procedimiento está en [RELEASING.md](https://github.com/APS-Conecta/gestion/blob/main/aps/RELEASING.md).

### Credenciales durante la instalación

Los scripts de APS Conecta entregan las contraseñas y las claves de servicio mediante variables de entorno por nombre o por la entrada estándar. `occ-install.php` recibe las contraseñas iniciales y ejecuta el instalador nativo de Nextcloud. `configure-apps.sh` importa los ajustes modificados con `occ config:import` y conserva las claves vecinas.

Redis recibe su regla de autenticación por la entrada estándar; sus clientes usan `REDISCLI_AUTH`. PostgreSQL obtiene la contraseña con `psql` y `\getenv`. La restauración de Borg conserva la contraseña del asistente mediante el entorno. Los argumentos de estos procesos contienen las opciones públicas.

La imagen de Imaginary compila el código oficial fijado y `api_key_env.go`, que inicializa la clave desde `IMAGINARY_SECRET`. Talk calcula la credencial TURN con la API criptográfica del entorno Erlang incluido en eTURNAL. Los conectores oficiales conservan su código y firma. El inicio interno de Euro-Office conserva la implementación oficial; su revisión de argumentos continúa en [#196](https://github.com/APS-Conecta/gestion/issues/196).

La provisión usa directorios temporales privados para el certificado intermedio y la bienvenida de IntraVox, transfiere el contenido por la entrada estándar y elimina esos directorios al terminar. Administra las cuentas de personal y cargo y conserva sus documentos. La compuerta local comprueba argumentos, entrega exacta de credenciales y rutas temporales.

### Mensajes de operación

El Provisionador informa la ruta absoluta que utiliza para leer un sitio o una planilla. Una coincidencia de usuario incluye una sola lista completa de cuentas reservadas, obtenida de la declaración del establecimiento. El resumen del entorno de ensayo muestra cada archivo de contraseña cuando existe.

El arranque, la revisión del paquete y la resolución de aplicaciones priorizan `signify-openbsd`. Las autopruebas existentes cubren su selección, las instrucciones de instalación, los archivos de credenciales y los errores del Provisionador. Las rutas de datos y del registro se comprobaron en la suite en ejecución y se describen en {doc}`/administracion/aio`.

### Desarrollo y verificación

Trabaje en una rama por tarea. Ejecute las verificaciones en un árbol de trabajo aislado y registre los resultados en el pull request. Los cambios de imágenes se validan con un conjunto reconstruido y una instalación limpia.

La aceptación por IP utiliza Ubuntu 24.04 y el script existente `scripts/vm-acceptance.sh`. Seleccione una versión publicada que contenga las correcciones:

```console
gh workflow run acceptance.yml --repo APS-Conecta/gestion --ref main -f tag=vX.Y.Z
```

El valor predeterminado de `tag` es `latest`, resuelto por redirección pública. La descarga y la instalación se ejecutan sin token, con las tres aplicaciones opcionales y el respaldo diario. Una etapa fallida conserva su resultado aunque las comprobaciones posteriores sean correctas. Los fallos de arranque, preparación o certificado conservan la tabla de veredictos. El flujo adjunta los resultados y las evidencias públicas disponibles en `release-acceptance-*`. Las credenciales y la configuración permanecen en el directorio privado del ensayo. Esta aceptación verifica la instalación y el funcionamiento del paquete publicado.

`install --sin-validar-dominio` delega en el controlador `asistente-aio`, que compone la solicitud del asistente. Las autopruebas existentes verifican la aceptación de la opción, la solicitud enviada, el modo silencioso y el comando de reintento.

`APS_HOME` concentra las credenciales, el resultado de ejecución, el estado del asistente, los certificados, el registro de versiones y los paquetes verificados. El valor predeterminado es `/opt/aps-conecta`. `AIO_STATE` y las variables `APS_APPS_*` conservan prioridad para sus rutas explícitas.

La [sección de desarrollo de INSTALLER.md](https://github.com/APS-Conecta/gestion/blob/main/aps/INSTALLER.md#14-provisionar-como-usuario-de-desarrollo) indica cómo clonar el repositorio, instalar `signify` en el directorio de usuario y ejecutar el banco de pruebas y el aprovisionamiento con una cuenta habilitada para Docker. La cuenta conserva la propiedad del certificado y autoriza su lectura a Apache mediante una ACL. La aceptación exige divergencia vacía.

`Containers/network-prefix.sh` calcula el prefijo IPv4 desde la dirección del servicio y su interfaz. Las imágenes de Nextcloud y Apache incluyen el mismo archivo y usan el contexto de construcción del repositorio. La compuerta local verifica prefijos e información ausente o ambigua; Clean boot comprueba una red `/20`, un cliente de la LAN con cabecera simulada y un proxy interno con una dirección reenviada válida.

Los trabajos de comprobación declaran permisos de lectura. El workflow reutilizable de imágenes admite `packages: write` para publicar y reduce los trabajos de comprobación a lectura. Los checkouts usan `persist-credentials: false`.

El plan vigente está en [gestion #175](https://github.com/APS-Conecta/gestion/issues/175). La documentación acompaña cada entrega en sus manuales de uso, administración y desarrollo.

El flujo de inicio termina con un resultado explícito dentro de su respuesta HTML. La consola valida ese resultado y comparte el mismo inicio con la actualización. Los avances de capas y bytes se distinguen de las señales periódicas de conexión; los estados repetidos y los reinicios cíclicos conservan el límite de 20 minutos de inactividad, medido con reloj monotónico.

Las autopruebas del anfitrión simulan errores con HTTP 200, una descarga de 70 minutos con avances, una descarga detenida y la recuperación de sesión. Una respuesta de autenticación permite un reingreso; una interrupción ambigua exige revisar el estado antes de repetir el inicio.

### Restauración de la base de datos

`Containers/postgresql/start.sh` reproduce el volcado con `ON_ERROR_STOP=1` y conserva `import.failed` ante un error. La aceptación utiliza un volcado completo de la suite: verifica la restauración válida, una sentencia fallida y el rechazo del siguiente inicio.

### AppAPI y HaRP

AppAPI, incluido en Nextcloud 34, conserva la inicialización nativa de su servicio de despliegue predeterminado. El contenedor se llama `aps-conecta-harp`; su endpoint en `nextcloud-aio` recibe el alias `nextcloud-aio-harp` durante la creación. AppAPI utiliza ese nombre en su registro y el proxy institucional lo excluye de las solicitudes externas.

HaRP monta el directorio de certificados públicos de la suite en modo de solo lectura. `Containers/harp/start.sh` combina esos certificados con los del sistema en `/tmp/ca-certificates.crt` y exporta `SSL_CERT_FILE` antes de ejecutar el inicio original de HaRP.

`scripts/appapi-smoke.sh` comparte la verificación entre la instalación limpia y `aps-conecta revalidate`. Exige un servicio seleccionado, su red y URL pública, y el resultado `success` de `OCA\AppAPI\SetupChecks\DaemonCheck`. Evalúa ese resultado aunque otras comprobaciones de Nextcloud informen advertencias.

La comprobación inversa obtiene únicamente los ajustes de confianza y la URL del proceso del agente. Configura la confianza antes de importar aiohttp y exige una respuesta HTTPS válida de `status.php` con la instancia instalada. El informe conserva privadas las credenciales del servicio.

Las autopruebas cubren certificados válidos y desconocidos, argumentos y estado de salida, y configuraciones ausentes, duplicadas, malformadas o inaccesibles. Clean boot repite la verificación después del reinicio y del aprovisionamiento repetido.

### Configuración y diagnóstico de Talk

La fase 12 ejecuta `configure-apps.sh talk` después de instalar o comprobar el paquete oficial de Talk. El arranque llama a la misma rutina. Un fallo de instalación, lectura de configuración o importación detiene ese paso.

El módulo compara los ajustes nativos e importa solo las claves modificadas con `occ config:import` por la entrada estándar. Las credenciales permanecen en el entorno del contenedor y en esa entrada; la repetición conserva los valores sin escrituras adicionales.

`scripts/talk-smoke.sh` exige la URL pública de señalización, TURN y STUN en el puerto 3478, y una respuesta HTTP 200 válida de `/standalone-signaling/api/v1/welcome`, con verificación del certificado de la suite. Evalúa `talk` → `OCA\Talk\SetupCheck\HighPerformanceBackend` de `occ setupchecks --output=json`.

Admite `success` o el mensaje nativo completo cuya única característica opcional ausente sea `changed-users`, en inglés o español. Esa advertencia conserva su aviso y exige además `success` en `system` → `OCA\Settings\SetupChecks\MemcacheConfigured` y el ajuste distribuido `\OC\Memcache\Redis`. Cualquier otra advertencia o error de señalización falla. [ADR-0024](https://github.com/APS-Conecta/gestion/blob/336e57547dfb4fd553af11ead545ca51418ab2cc/docs/adr/0024-supported-talk-compatibility-warning.md) delimita esta compatibilidad con el servidor oficial y su condición de retiro.

La compuerta conserva los ajustes de conexión. El diagnóstico nativo puede inicializar claves de señalización y registrar capacidades del servicio. Clean boot comprueba el primer aprovisionamiento, el reinicio y la repetición. Su experimento TURN distingue la asignación autenticada, los permisos para cada dirección y el intercambio real de datos; una asignación aislada acredita solo esa operación.

El [experimento por IP](https://github.com/APS-Conecta/gestion/actions/runs/41211391805/job/124567070362) confirmó STUN, la asignación TURN autenticada y el intercambio bidireccional con el par privado permitido de Talk. El destino privado de LAN sin permiso recibió un rechazo 403 autenticado y ningún dato. La política de pares se conserva. Este resultado corresponde al relé; la llamada entre navegadores se valida en la aceptación de cada instalación.

Después de revalidar, Clean boot por IP repite `talk-smoke.sh` antes del ensayo de mensajes. Usa `POST v4/room` con `roomType` y `roomName`, `POST v1/chat/{token}` y `GET` del mismo historial. Una cuenta ordinaria crea y envía; otra lee el texto exacto junto con la identidad, el identificador y la conversación correspondientes. La comprobación admite los mensajes del sistema.

El creador elimina únicamente la conversación del ensayo. Cada escritura se ejecuta una vez y un fallo de limpieza conserva el fallo original. Las credenciales permanecen en el registro privado y en memoria; el cliente verifica el certificado de la suite y rechaza redirecciones.

### Confianza del grabador

El grabador oficial recibe la CA pública de la suite mediante un montaje de solo lectura. `Containers/talk-recording/prepare-trust.py` valida los certificados y prepara el conjunto de confianza de Python y la política nativa `Certificates.Install` de Firefox. Las notificaciones HTTP usan ese conjunto a través de `certifi`; el código oficial del grabador conserva la verificación TLS.

Clean boot por IP comprueba las notificaciones Python y el navegador del grabador con la CA y sin ella. La compuerta local cubre la rotación, el nombre IP y los certificados desconocidos. Redis y la tienda tienen esperas acotadas; una demora del grabador conserva Talk y deja pendiente la configuración de grabación. La grabación permanece desactivada en la configuración de la suite.

### El arranque de una línea

El activo de instalación de cada versión lleva la suma del paquete y la clave pública. Desempaca la suite en `/opt/aps-conecta/instalador` y conserva el paquete en `/opt/aps-conecta/paquete` para verificarlo sin red. El procedimiento está en {doc}`/administracion/aio`.

Antes de instalar la carpeta del paquete, ejecuta la comprobación de instalación existente del módulo del anfitrión incluido en el paquete verificado. Las comprobaciones de arquitectura, FUSE, Docker, disco y puertos se comparten entre la revisión previa, la preparación y el inicio desde el navegador. Las autopruebas del anfitrión y del arranque cubren los rechazos con comandos simulados; Clean boot instala el paquete antes de crear los contenedores.

### Análisis de cargas

La fase 12 instala `files_antivirus` desde el canal de tienda declarado en `apps.json`. La fase 14 y el inicio comparten `configure-apps.sh antivirus`, que configura la aplicación instalada antes de esperar al servicio. La aplicación permanece habilitada durante una demora del analizador.

`Containers/antivirus-limit.sh` convierte el límite de carga a bytes y lo acota a 2.147.483.645. Nextcloud y ClamAV usan el mismo cálculo. La aplicación utiliza ICAP; el contenedor de ClamAV incluye c-icap con revisiones y sumas fijadas, y entrega el archivo completo al motor existente. El análisis de archivos comprimidos activa las alertas de cifrado y límites. Los mensajes en español pertenecen al tema; el inicio actualiza sus archivos y conserva `site.css`, generado para el establecimiento.

`av_max_file_size=-1` mantiene todas las cargas elegibles para revisión: un valor positivo omite el análisis de archivos ensamblados que lo superan. El límite de aceptación se aplica en ICAP y ClamAV con la misma entrada del instalador.

La fase 12 instala `files_upload_guard` desde su publicación firmada. Esta compatibilidad de Nextcloud 34 conserva el archivo anterior si una sustitución se rechaza o carece de una ubicación temporal segura. ADR-0022 delimita la dependencia del envoltorio de almacenamiento; el núcleo y la aplicación de tienda conservan sus archivos originales. El flujo compartido admite aplicaciones PHP sin interfaz de navegador mediante `php-only: true`, con la misma firma y verificación de paquetes.

El servidor web conserva HTTP 500 y entrega orientación en español para errores de carga WebDAV. La persona revisa Archivos antes de repetir una operación cuyo resultado requiere comprobación.

La compuerta local comprueba unidades y valores inválidos. Clean boot verifica contenido limpio, EICAR, archivos ensamblados, límites, comprimidos, fallas y recuperación mediante WebDAV. También comprueba sustituciones, permisos de carpetas compartidas y respuestas del servidor web. La importación programada del DEIS se comprueba antes de los reinicios controlados. Registre los resultados junto con la procedencia de las imágenes en el pull request.

### Búsqueda de contenido

`apps.json` declara `fulltextsearch` y `fulltextsearch_elasticsearch` como aplicaciones de tienda. El proveedor `files_fulltextsearch` utiliza la publicación firmada de {doc}`/desarrollo/files-fulltextsearch`, con el mismo mecanismo de adquisición y bloqueo de versión de las aplicaciones propias. ADR-0023 registra esta excepción temporal al plan original y las condiciones para volver a la tienda.

La fase `14-fulltextsearch` ejecuta el destino `fulltextsearch` de `configure-apps.sh` después de la instalación. El arranque usa la misma rutina; una aplicación ausente queda pendiente para la fase 12. La configuración conserva las aplicaciones habilitadas durante una demora del servicio.

El módulo del anfitrión administra juntos los ajustes de memoria del núcleo. Su autoprueba comprueba el archivo persistente, la aplicación y la conservación de un límite de mapas superior. `ConfigurationManager::fulltextsearchJavaOptions` define el valor Java predeterminado y conserva las opciones del establecimiento.

La aceptación por IP carga un archivo mediante WebDAV con una cuenta sin privilegios y un identificador con punto. Indexa ese archivo una vez y comprueba que el motor guarda su identidad y una palabra exclusiva del contenido. La búsqueda dispone de 30 segundos para devolver el mismo proveedor, identificador público, ruta y tipo. Solo se repite la lectura; los errores de comando y de JSON detienen la prueba. El documento se elimina al terminar.

### Proxy de salida

El anfitrión valida y carga un perfil de variables fijo, con permisos privados y lectura literal. El arranque firmado delega su guardado al módulo del paquete verificado. Docker utiliza un archivo de entorno mediante una configuración de systemd; el comando de arranque contiene su ruta. La aplicación correcta se registra después del reinicio del servicio y una falla conserva el intento pendiente.

El asistente transmite el entorno normalizado al contenedor de la plataforma. Su configuración de proxy existente aplica las exclusiones y marca la dirección como sensible en los listados ordinarios. Las llamadas al socket Docker permanecen directas. Las autopruebas del anfitrión cubren persistencia, propagación, exclusiones y recuperación; Clean boot verifica solicitudes autenticadas al registro y GitHub mediante un proxy local.

### La corrección de red con consentimiento

La tarjeta «La red del servidor» ofrece «Sí, corregir» cuando el servidor necesita DNS dividido para alcanzar su dominio. La corrección requiere consentimiento explícito y reinicia Docker una vez.

`dnsmasq` utiliza `bind-dynamic` con escucha en loopback y la dirección LAN. El escritor JSON existente combina el DNS de Docker con los servidores obtenidos de `resolvectl dns` y `resolv.conf`; conserva las otras opciones y excluye direcciones locales que producen bucles y direcciones IPv6 que requieren la interfaz del anfitrión. Las autopruebas cubren ambas fuentes y la repetición sin cambios.

La preparación separa la instalación de herramientas requeridas y del verificador opcional. Su ausencia mantiene la firma pendiente e informa cómo habilitar universe en Ubuntu.

(pisos-de-recursos-y-datos-comunales)=
### Datos comunales

`provisioning/data/packages.json` fija el origen y la suma de cada maestro. La próxima versión conserva la captura DEIS del 2026-11-01 en el repositorio y la descarga mediante un commit completo. `scripts/comuna-package.sh` extrae el ZIP con la biblioteca estándar de Python y recorta ambos maestros por código CUT.

Clean boot por IP incluye subconjuntos publicados con su procedencia y licencia en `tests/fixtures/comuna/README.md`. El paquete de ensayo fija esos archivos locales antes de firmarse. La instalación ejecuta la importación real; una cuenta ordinaria consulta nombres y geometrías por la API OCS de Territorio. La repetición exige «0 creados» en ambos paquetes.

### Diagnóstico de recursos

La revisión previa conserva sus controles actuales. `scripts/usage.py` registra en ambos trabajos de Clean boot series acotadas de memoria, CPU, intercambio y OOM, junto con métricas de los servicios. Cada muestra identifica su arranque y sus unidades; el cierre vincula el PID y la cantidad de muestras. Las lecturas ausentes se registran como no disponibles.

El [diagnóstico de recursos](https://github.com/APS-Conecta/gestion/blob/main/aps/RESOURCE-MEASUREMENTS.md) describe la captura y sus referencias. El plan #175 conserva las comprobaciones funcionales y retira el ensayo de capacidad, los umbrales medidos y el cálculo compartido de concurrencia. La administración dimensiona el servidor según su uso; la memoria indicada por Nextcloud por proceso conserva ese alcance.

### Instalaciones previas

El instalador sirve instalaciones limpias. El procedimiento de actualización y los límites de instalaciones anteriores están en {doc}`/administracion/aio`.

(deuda-tecnica-y-limites)=
### Límites

Las integraciones pendientes y la versión que las incorpora se registran en {doc}`/proyecto/novedades/instalador`.
