---
tipo: referencia
audiencia: administracion
apps: [gestion]
resumen: "Las fases del aprovisionamiento en su orden fijo: qué escribe cada una en la instalación, por qué, y cómo converge sin borrar contenido."
---
# Aprovisionamiento

## Resumen

El ejecutor `provisioning/seed.sh` es el único escritor del estado declarado de la instancia: ningún procedimiento la modifica desde la interfaz de administración ni con comandos `occ` sueltos. Las cuentas del personal llegan aparte, con la carga de la planilla, y en AIO el entrypoint del asistente escribe en cada arranque la URL pública del editor, el secreto JWT y `trusted_domains`.
Carga los archivos de fase numerados de `provisioning/phases/` en orden fijo y ejecuta cada uno en una subshell propia con `set -e`.
Una fase que falla detiene la ejecución con `FATAL: phase <archivo> failed`, y ninguna fase traspasa variables de shell a la siguiente: el estado entre fases pasa por la instancia y las guardias lo vuelven a consultar.
Una fase ejecutada fuera del ejecutor se niega a correr, porque sin el archivo del establecimiento recorrería arreglos vacíos y terminaría en verde sin escribir nada.

El ejecutor tiene cuatro puertas de entrada:

- `make install` en la pila de desarrollo: levanta la pila, ejecuta las fases con el registro completo en `.install.log`, comprueba la salud y termina con el informe de divergencia.
- `make seed`: la misma secuencia de fases, con toda su salida en pantalla.
- El Provisionador del instalador de un centro, que ejecuta `bash provisioning/seed.sh` contra la instancia de {doc}`AIO </administracion/aio>` por `docker exec`.
- El temporizador semanal `aps-conecta.timer`, que repite la provisión sin intervención los domingos a las 03:00 hora de Santiago; en una instancia convergida no escribe nada, y una deriva aparece como unidad fallida.

Antes de la primera fase, el ejecutor exige cuatro condiciones y se detiene si falta alguna:

- `SITE`, en `.env`, nombra un archivo `sites/<slug>/site.sh` que existe.
- Ninguna clave de `.env` conserva el marcador `change-me` que `.env.example` publica.
- El archivo del establecimiento define `SITE_FOLDERS`, `SITE_TEAMS` y `SITE_WELCOME`: vacío es válido, ausente no.
- La instancia responde instalada a `occ status`.

La convergencia es aditiva: aplica todo lo reversible y nunca borra carpetas de grupo, cuentas ni archivos.
Lo que sigue vivo en la instancia sin estar declarado se informa al final de `make install` y con `make divergence`, con el objeto y el comando que lo eliminaría.

## Tabla

| Fase | Qué escribe | Por qué |
|---|---|---|
| `05-security` | `remember_login_cookie_lifetime` en `0` y `lookup_server` vacío. | En una estación clínica compartida, quien se sienta después hereda la sesión anterior: con `0`, la sesión del navegador termina con la ventana. La exclusión del servidor público de búsqueda queda como decisión declarada. Corre primero para que la instancia nunca quede en una postura más débil entre fases. |
| `06-jobs` | `backgroundjobs_mode` de `core` en `cron` y `maintenance_window_start` en `5`. | En modo `ajax` las {doc}`tareas de fondo </administracion/servidor/background-jobs-configuration>` corren solo cuando alguien carga una página, y el barrido de tokens vencidos depende de ellas. La hora 5 UTC abre la ventana de cuatro horas de las tareas diarias pesadas a la 01:00 de Chile en horario estándar, lejos del turno. |
| `07-certs` | El certificado intermedio de la autoridad que firma el sitio del Instituto de Salud Pública, y la autoridad del instalador cuando el contenedor la tiene montada (instalación por IP). | Ese sitio sirve solo su certificado hoja; un cliente del servidor no sigue el puntero AIA y sin el intermedio no recibe las 24 fuentes de alertas ANAMED que lee epidemiologia. Va antes de `12-apps`, donde epidemiologia se instala. La importación se agrega al paquete de certificados del servidor y sirve a todas las aplicaciones; nunca se desactiva la verificación. |
| `10-locale` | `default_language` y `force_language` en `es`, `default_locale` en `es_CL` y `default_phone_region` en `CL`. | `es` es un idioma que el núcleo trae; `es_419`, el valor anterior, es una configuración regional y no un idioma, y quedaba sin efecto (B-009). El {doc}`idioma </administracion/servidor/language-configuration>` se fuerza porque la cabecera del navegador se lee antes que el valor por defecto; `es_CL` da el formato chileno de fechas y números. |
| `12-apps` | Cada aplicación de `APPS` (`groupfolders side_menu eurooffice calendar contacts spreed desktop_workspace`): desempaqueta su tarball de `provisioning/apps/<id>/`, verifica el sha256 de su archivo `VENDOR`, aplica sus `*.patch` en orden de nombre, borra `appinfo/signature.json` de las parcheadas y la habilita. Las de `OWN_APPS` (epidemiologia, farmacia, territorio, intravox, estadistica) se instalan desde su tarball del mismo modo, sin parches; en una máquina de desarrollo donde existe `apps/<id>/.git`, el clon queda intacto. | Nada contacta la tienda de aplicaciones: la misma siembra produce la misma instancia, también sin red. Una versión instalada distinta de la del tarball se reimpone, y `occ upgrade` reconcilia su esquema. Talk se omite en AIO cuando el asistente lo dejó apagado, porque la imagen elimina en cada arranque las aplicaciones deshabilitadas. |
| `14-office` | En el conector `eurooffice`: `sameTab` en `false`, `customizationTheme` en `default-light`, y `editFormats` y `defFormats` con los formatos ODF. En Compose, además, las tres URL del servidor de documentos, `nextcloud` en `trusted_domains` y `jwt_secret`, sin imprimir el valor. En AIO por IP, solo las dos URL internas. | Un documento abre en ventana nueva y no reemplaza la carpeta desde la que se abrió; el editor sigue el tema claro de la instancia; ODF se edita con la pérdida de formato que implica la conversión (#45). En AIO, el entrypoint del asistente es dueño de la URL pública, del secreto y de `trusted_domains`. |
| `15-branding` | Nombre, eslogan, URL y colores de `theming`; `productName`; `enforce_theme` en `light` y `disable-user-theming`; logotipos, favicon y fondo; color de `side_menu`; `defaultapp` en `intravox`; `skeletondirectory` y `customclient_ios_appid` vacíos; `theme` en `apsconecta`; y el archivo `themes/apsconecta/core/css/site.css` con el nombre corto del establecimiento. | La {doc}`marca </administracion/servidor/theming>` es configuración como código. Sin `productName`, el nombre del fabricante aparece en `status.php` y en las capacidades OCS. El inicio cae en la pantalla de bienvenida y vuelve a `dashboard,files` si la aplicación falta. El esqueleto vacío evita archivos en inglés en cada cuenta nueva. |
| `16-app-policy` | Restringe a `admin` las aplicaciones de `POLICY_ADMIN_ONLY`; escribe los interruptores de `POLICY_CONFIG`; deshabilita `survey_client`, `nextcloud_announcements` y `office`; escribe `tile_url`, `comuna_cut` y `comuna_name` de territorio, y `deis_code`, `establishment_type` y `comuna_cut` de estadistica. | El administrador conserva todas las aplicaciones y el resto de las cuentas recibe el conjunto reducido. Los interruptores van antes de las deshabilitaciones: el de `survey_client` solo surte efecto con la aplicación habilitada. Un `comuna_cut` vacío desarma la puerta de importación de territorio y un código DEIS sin seis dígitos deja a estadistica sin establecimiento, por eso ambos detienen la fase. |
| `20-groups` | `all-staff`, las cuatro categorías `cat-*`, los 22 roles `role-*` compartidos, los roles propios de `SITE_ROLES` y los equipos `prog-*` y `sector-*` de `SITE_TEAMS`, con identificador en inglés y nombre visible en español. | El grupo es la única llave de acceso. Los roles compartidos mantienen comparable la matriz de un centro con la de otro; las categorías no se definen por sitio, y un rol local con una categoría desconocida detiene la fase. |
| `30-folders` | Una carpeta de grupo por entrada de `SITE_FOLDERS`, las subcarpetas de `Transversal` según `SITE_SUBFOLDERS` y el archivo `LÉEME — Convenciones.md`. | Las carpetas de grupo no se anidan: los puntos de montaje con barra (`Programas/…`, `Unidades/…`, `Sectores/…`) dan la forma del árbol de cuatro áreas. `groupfolders:create` no es idempotente por nombre, así que la fase consulta antes de crear. |
| `40-acl` | Cada fila de `SITE_ACL` (`montaje\|grupo\|permisos`) como permiso base de grupo; después, `gf_prune` revoca en esas carpetas toda concesión que el archivo no declara. | Las concesiones solo agregan: sin reglas de denegación, que anularían la unión de permisos de una persona con varios roles. Administrar incluye eliminar, para que un archivo subido por error pueda retirarse. Revocar una concesión no pierde archivos. |
| `41-intravox` | La carpeta de grupo del motor de IntraVox con el nombre `IV_MOUNT`, la correspondencia de grupos del registro con los del motor, el árbol de bienvenida en español renderizado desde `SITE_WELCOME` (solo las secciones que faltan) y las reglas de página de cada equipo nuevo. | La pantalla de bienvenida es estructura y no dato de prueba, por eso la fase corre en todos los centros. Converge por sección y nunca sobrescribe lo que el personal editó. |
| `50-users` | Una cuenta por cargo: `director`, `subdirector`, `jefe.farmacia`, `jefe.some`, una jefatura por cada equipo `sector-*` y una por cada rol local de `cat-jefaturas`, con sus grupos. | Son cargos, no personas. Una jefatura por sector mantiene probada la separación por sector de la matriz de acceso. La fase nunca crea grupos: si uno falta, la cuenta se crea igual y la falta queda en el registro de la ejecución. |
| `60-fixtures` | El archivo sintético `Bienvenida-APS-Conecta.md` en la carpeta personal de `director`. | Entrega el mecanismo de contenido de prueba; el texto declara que no contiene datos reales. |

## Notas

### Guardias de idempotencia

Cada paso que escribe consulta antes el estado y solo escribe la diferencia, con los ayudantes de `provisioning/lib.sh`.
`config_system_set`, `app_config_set` y `theming_set` escriben una clave solo cuando su valor difiere, y distinguen una clave ausente de una clave vacía.
`ensure_group`, `ensure_user` y `ensure_groupfolder` consultan la lista de la instancia antes de crear.
`gf_grant` compara la máscara de permisos vigente y la reescribe cuando difiere, tanto para ampliar como para restringir.
`theming_image_set` es el único ayudante que vuelve a escribir en cada ejecución.
`make seed-idempotent` ejecuta una segunda siembra y falla si su registro contiene un verbo de escritura; las imágenes de marca son la única excepción, por nombre.
La versión de gestion que produjo cada ejecución queda en la primera línea de la salida, tomada de `git describe`.

### Estructura y datos de prueba

Las fases `05` a `41` escriben estructura y las fases `50` y `60`, datos de prueba.
Con `SEED_FIXTURES=0`, el ejecutor omite toda fase de número 50 o mayor.
Los datos de prueba nunca crean estructura: la fase `50-users` agrega cuentas solo a grupos que la fase `20-groups` ya creó.
El instalador de un centro fuerza `SEED_FIXTURES=1`, porque sin la fase `50-users` el centro quedaría sin sus cuentas de cargo.
En esa instalación, cada cuenta de cargo recibe su propia contraseña inicial sellada; solo la pila de desarrollo y la integración continua les dan a todas `FIXTURE_USER_PASSWORD`.

### Datos del establecimiento

Todo lo propio de un establecimiento está en `sites/<slug>/site.sh`: identidad, equipos, carpetas, subcarpetas, matriz de acceso, roles locales y árbol de bienvenida.
`scripts/deis.py` escribe ese archivo a partir del registro DEIS que trae el repositorio y pregunta los sectores y programas, que el registro no conoce.
El archivo queda fuera del control de versiones, como `.env`, y es completo: nada se hereda al sembrar.
El ejecutor lo carga una vez antes de la primera fase; cada fase lo ve y ninguna puede modificarlo.
`all-staff`, las cuatro categorías y los 22 roles compartidos están en el código y son iguales en todas las instalaciones.

### Orden y fallos

El orden sale del ordenamiento alfabético que hace la shell al expandir `phases/[0-9]*.sh`, no de un orden numérico: todo prefijo debe tener dos dígitos, porque una fase `100-` correría entre `10-` y `12-`.
Las dependencias de ese orden son explícitas: `12-apps` instala el conector que configura `14-office`, el menú que colorea `15-branding` y las carpetas de grupo de `30-folders`; `41-intravox` necesita los grupos de `20-groups`; `50-users` necesita los grupos y la matriz ya aplicados.
Un fallo se corrige y se repite el mismo comando: lo ya aplicado se salta en segundos.
El ejecutor prueba el resultado de cada fase como un comando propio y no dentro de un `if`, porque bash suspendía `set -e` dentro de la subshell y una fase seguía después de su primer error (B-001).

### Deuda técnica y límites

- El repositorio no tiene respaldo propio, y por eso la convergencia informa en lugar de borrar: un error de tipeo en el archivo del establecimiento no puede destruir documentos.
- Quitar una aplicación de `APPS` no la desinstala: `make divergence` la informa hasta que alguien ejecuta `occ app:remove` a mano.
- Las reglas de página de un equipo nuevo se escriben una sola vez, junto con la página; si una ejecución muere entre la importación y las reglas, la página queda sin ellas y la siguiente ejecución no las repone.
- `LÉEME — Convenciones.md` se crea solo si no existe: una versión editada de `docs/CONVENTIONS.md` no llega a una instancia que ya tiene el archivo, porque el personal pudo anotarlo.
- Con el esqueleto vacío, una cuenta nueva no recibe carpeta de plantillas y la acción de crear no ofrece plantillas.
- Los certificados importados viven en el volumen de datos: sobreviven un reinicio, pero no un borrado del volumen.
- Los tarballs de las aplicaciones están en el repositorio y git guarda una copia completa por cada actualización; Talk ocupa 52 MB.
- Cerrar la ventana no cierra la sesión en un navegador que restaura la sesión anterior; eso requiere una política de la estación de trabajo.
