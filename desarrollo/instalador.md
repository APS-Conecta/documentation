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

### Mensajes de operación

El Provisionador informa la ruta absoluta que utiliza para leer un sitio o una planilla. Una coincidencia de usuario incluye una sola lista completa de cuentas reservadas, obtenida de la declaración del establecimiento. El resumen del entorno de ensayo muestra cada archivo de contraseña cuando existe.

El arranque, la revisión del paquete y la resolución de aplicaciones priorizan `signify-openbsd`. Las autopruebas existentes cubren su selección, las instrucciones de instalación, los archivos de credenciales y los errores del Provisionador. Las rutas de datos y del registro se comprobaron en la suite en ejecución y se describen en {doc}`/administracion/aio`.

### Desarrollo y verificación

Trabaje en una rama por tarea. Ejecute las verificaciones en un árbol de trabajo aislado y registre los resultados en el pull request. Los cambios de imágenes se validan con un conjunto reconstruido y una instalación limpia.

`Containers/network-prefix.sh` calcula el prefijo IPv4 desde la dirección del servicio y su interfaz. Las imágenes de Nextcloud y Apache incluyen el mismo archivo y usan el contexto de construcción del repositorio. La compuerta local verifica prefijos e información ausente o ambigua; Clean boot comprueba una red `/20`, un cliente de la LAN con cabecera simulada y un proxy interno con una dirección reenviada válida.

Los trabajos de comprobación declaran permisos de lectura. El workflow reutilizable de imágenes admite `packages: write` para publicar y reduce los trabajos de comprobación a lectura. Los checkouts usan `persist-credentials: false`.

El plan vigente está en [gestion #175](https://github.com/APS-Conecta/gestion/issues/175). La documentación acompaña cada entrega en sus manuales de uso, administración y desarrollo.

El flujo de inicio termina con un resultado explícito dentro de su respuesta HTML. La consola valida ese resultado y comparte el mismo inicio con la actualización. Los avances de capas y bytes se distinguen de las señales periódicas de conexión; los estados repetidos y los reinicios cíclicos conservan el límite de 20 minutos de inactividad, medido con reloj monotónico.

Las autopruebas del anfitrión simulan errores con HTTP 200, una descarga de 70 minutos con avances, una descarga detenida y la recuperación de sesión. Una respuesta de autenticación permite un reingreso; una interrupción ambigua exige revisar el estado antes de repetir el inicio.

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

El creador elimina únicamente la conversación del ensayo. Cada escritura se ejecuta una vez y un fallo de limpieza conserva el fallo original. Las credenciales permanecen en el registro privado y en memoria; el cliente verifica el certificado de la suite y rechaza redirecciones. La política de grabación se mide por separado en [#189](https://github.com/APS-Conecta/gestion/issues/189).

### Confianza del grabador

El grabador oficial recibe la CA pública de la suite mediante un montaje de solo lectura. `Containers/talk-recording/prepare-trust.py` valida los certificados y prepara el conjunto de confianza de Python y la política nativa `Certificates.Install` de Firefox. Las notificaciones HTTP usan ese conjunto a través de `certifi`; el código oficial del grabador conserva la verificación TLS.

Clean boot por IP comprueba las notificaciones Python y el navegador del grabador con la CA y sin ella. La compuerta local cubre la rotación, el nombre IP y los certificados desconocidos. Redis y la tienda tienen esperas acotadas; una demora del grabador conserva Talk y deja pendiente la configuración de grabación. Su activación por recursos continúa en [#189](https://github.com/APS-Conecta/gestion/issues/189) y [#190](https://github.com/APS-Conecta/gestion/issues/190).

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

### Pisos de recursos

La revisión previa informa recursos mínimos y recomendados.

La preparación de [#189](https://github.com/APS-Conecta/gestion/issues/189) incorpora `scripts/usage.py` en ambos trabajos de Clean boot. Conserva series JSONL acotadas de memoria, CPU, intercambio y OOM del anfitrión, junto con métricas de los contenedores. Cada muestra identifica su arranque y sus unidades; el cierre vincula el PID y la cantidad de muestras. Las métricas de Docker ausentes se registran como no disponibles. Una captura incompleta o una interrupción durante la carga estable invalida esa repetición.

El [protocolo de medición](https://github.com/APS-Conecta/gestion/blob/072f3a9a929b4b8b15fe9589320612d09e022616/aps/RESOURCE-MEASUREMENTS.md) establece procedencia, carga y límites de interpretación. Los umbrales compartidos del instalador y del Provisionador se fijan después de medir operaciones reales de Office, Talk, cargas y búsqueda, con la grabación evaluada por separado. Los mínimos y recomendaciones deben incluir la referencia oficial de Nextcloud y la evidencia del ensayo. Los valores de memoria por proceso se interpretan dentro de ese alcance.

### Instalaciones previas

El instalador sirve instalaciones limpias. El procedimiento de actualización y los límites de instalaciones anteriores están en {doc}`/administracion/aio`.

(deuda-tecnica-y-limites)=
### Límites

Las integraciones pendientes y la versión que las incorpora se registran en {doc}`/proyecto/novedades/instalador`.
