---
tipo: guia
audiencia: administracion
apps: [gestion]
resumen: "Comprobar la postura de seguridad que fija el aprovisionamiento —red, sesiones, salidas, integridad, tienda cerrada— y conocer lo que no fija."
---
# Seguridad

## Objetivo

Esta guía comprueba que una instalación conserva la postura de seguridad que fija el {doc}`aprovisionamiento </administracion/aprovisionamiento>`, y deja escrito lo que esa postura todavía no cubre.

La plataforma no está pensada para guardar datos de pacientes, pero nada impide que el personal suba archivos clínicos a Archivos, a Talk o al editor de documentos Euro-Office.
Por eso cada cuenta, cada enlace compartido y cada respaldo se tratan como si los tuvieran: cada valor que la suite fija, o que deja en su valor por defecto, es una salvaguarda.
Lo que un atacante busca es una cuenta del personal, un enlace público sin contraseña ni caducidad, un respaldo o un secreto expuesto, un acceso sin rastro y un transporte débil.

### Lo que fija la suite

| Medida | Dónde | Por qué |
|---|---|---|
| Puertos solo en `127.0.0.1` | `compose.yaml`, pila de desarrollo | La instancia de desarrollo nunca queda expuesta en la red local. |
| TLS en `aps-conecta-apache`, puerto 443 | Instalador AIO | El proxy inverso del instalador termina TLS. En una instalación por IP, la autoridad propia del instalador firma el certificado de la suite, que la ejecución semanal vuelve a firmar 30 días antes de que venza; la fase `07-certs` hace que la plataforma confíe en esa autoridad. |
| `trusted_domains` | `.env` y fase `14-office` en Compose; entrypoint del asistente en AIO | La plataforma rechaza un host no declarado. En Compose, la fase agrega `nextcloud` para que el servidor de documentos descargue archivos por la red interna; en AIO, `trusted_domains` pertenece al entrypoint del asistente, que escribe el dominio de la instalación. |
| `remember_login_cookie_lifetime` en `0` | Fase `05-security` | El formulario de inicio de sesión deja de ofrecer recordar la sesión, el servidor la descarta aunque se envíe, y la sesión del navegador termina con la ventana. Los clientes de escritorio y móviles de {vendor}`Nextcloud` conservan sus tokens permanentes, que barre la retención de tokens. |
| Tareas de fondo por `cron` | Fase `06-jobs` | El barrido de tokens vencidos corre desde las tareas de fondo; sin `cron`, la postura de sesiones dejaría filas muertas. |
| `lookup_server` vacío | Fase `05-security` | La exclusión del servidor público de búsqueda de {vendor}`Nextcloud` queda declarada; con los valores por defecto la plataforma ya no lo consultaba, y la clave evita que eso dependa de un descuido. |
| `enforceHaveIBeenPwned` en `0` | `provisioning/app-policy.sh` | Ni siquiera el prefijo del hash de una contraseña nueva sale del servidor hacia `api.pwnedpasswords.com`. |
| `survey_client` con `never_again` y deshabilitada; `nextcloud_announcements` deshabilitada | `provisioning/app-policy.sh` | La primera enviaría datos de uso cada 28 días desde el servidor, la vea quien la vea; la segunda empuja la publicidad del fabricante a la campana de notificaciones de cada cuenta. |
| `weather_status` restringida a `admin`; telemetría de IntraVox en `false` | `provisioning/app-policy.sh` | El panel del clima llama a una API externa desde el tablero de cada cuenta; IntraVox trae su telemetría activada por defecto. |
| Firma eliminada solo en aplicaciones parcheadas | Fase `12-apps` | `eurooffice` y `desktop_workspace` llevan parches versionados, y su `appinfo/signature.json` dejaría de describir los archivos: la {doc}`verificación de integridad </administracion/problemas/code-signing>` quedaría en rojo para siempre. El núcleo y cada aplicación sin parches conservan su verificación. |
| Tienda de aplicaciones cerrada | `NC_appstoreenabled: "0"` en los servicios `nextcloud` y `cron` de Compose; incorporado en la imagen del servidor en AIO | Con la tienda abierta, `occ upgrade` vuelve a descargar cada aplicación habilitada y ningún sha256 de `VENDOR` se sostiene. Las aplicaciones llegan solo desde los tarballs del repositorio, verificados por su sha256. |
| Secretos | `make setup`, `.env` con modo 600 | `make setup` genera los cuatro secretos desde `/dev/urandom`; el aprovisionamiento se niega a correr si `.env` conserva un marcador `change-me` publicado en el repositorio; el secreto JWT del servidor de documentos nunca aparece en la salida. |

### Lo que la suite no fija

Estas medidas quedan en el valor por defecto de la imagen fijada, y cada una es un objetivo de revisión:

- **{doc}`Autenticación de dos factores </administracion/usuarios-y-grupos/two-factor-auth>`**: ningún proveedor está habilitado y no se exige al personal ni a quienes administran.
- **{doc}`Política de contraseñas </administracion/usuarios-y-grupos/user-password-policy>`**: solo está fijado el chequeo de contraseñas filtradas, y está apagado; una contraseña conocida como filtrada ya no se rechaza. Largo, contraseñas comunes y caducidad quedan por defecto.
- **Auditoría**: `admin_audit` no está habilitada, así que no hay registro de accesos a archivos ni de comparticiones.
- **{doc}`Compartición </administracion/archivos/file-sharing-configuration>`**: nada fija contraseña ni caducidad de los enlaces públicos, ni límites a la compartición por correo.
- **{doc}`Cifrado en reposo </administracion/archivos/encryption-configuration>`**: el cifrado del lado del servidor no está habilitado.
- **{doc}`Fuerza bruta </administracion/servidor/bruteforce-configuration>`**: rige la limitación integrada de la plataforma, sin configuración propia.
- **TLS y cabeceras**: nada en el repositorio fija versiones de TLS ni cabeceras de seguridad; quedan a cargo del proxy inverso del instalador.

La postura de producción —HSTS, correo saliente, exigencia de dos factores— queda diferida hasta que exista un host de destino (#75), y el modelo de amenazas no registra riesgos aceptados.

## Requisitos

- Un centro instalado con el instalador AIO y en marcha.
- Una consola en el servidor, en la copia de gestion de `/opt/aps-conecta/gestion`, con permisos sobre Docker.
- El `.env` de esa copia con `HTTP_PORT=443`, el puerto público que leen las pruebas.

## Pasos

1. Ejecutar la prueba de humo:

   ```bash
   make smoke
   ```

   Cinco de sus comprobaciones cubren esta postura: la 8, que el personal no ve las aplicaciones restringidas ni deshabilitadas; la 9, que el formulario de inicio de sesión no ofrece recordar la sesión; la 10, que ninguna aplicación parcheada conserva su firma; la 13, que `appstoreenabled` vale `0`; y la 14, que la URL del editor coincide con la forma en que se llega a la instancia.

2. Ejecutar la compuerta de divergencia:

   ```bash
   bash scripts/divergence.sh --gate
   ```

   La compuerta compara la instancia con su declaración —carpetas de grupo, secciones de bienvenida, grupos, aplicaciones, cuentas y la identidad del establecimiento en territorio y estadistica— y sale con código 1 ante cualquier nota.
   Una cuenta o un grupo vivo sin declarar es un acceso que nadie decidió en el archivo del establecimiento.

## Verificación

La prueba de humo termina con una línea `PASS: core stack healthy` que enumera, entre otros hechos, la política de aplicaciones, la ausencia de recordar la sesión, la ausencia de firmas obsoletas y la tienda cerrada.
La compuerta de divergencia sale con código 0 y sin notas: la instancia coincide con su declaración, cuentas incluidas.

## Problemas frecuentes

| Síntoma | Causa | Remedio |
|---|---|---|
| La comprobación 9 dice que el formulario ofrece recordar la sesión | `remember_login_cookie_lifetime` no vale `0` en esta instancia: la fase `05-security` no quedó aplicada | En la pila de desarrollo, `make install`; en un centro, la re-provisión semanal la restituye. |
| La comprobación 10 encuentra una aplicación parcheada con su firma | Una actualización de la aplicación fuera del aprovisionamiento (`occ app:update`) revirtió los parches y restauró `signature.json` | Volver a aprovisionar: la fase `12-apps` reimpone el tarball fijado, aplica los parches y vuelve a quitar la firma. |
| Un documento no abre desde otro equipo y el editor informa un problema de token o de seguridad | La URL del editor apunta a `localhost`, o usa `http://` en una instancia servida por `https://`; el secreto JWT no es la causa | La comprobación 14 detecta las dos contradicciones; en Compose, `OFFICE_PUBLIC_URL` lleva la URL pública y se vuelve a aprovisionar. La prueba corre en el servidor y no puede abrir un documento desde otro equipo: esa prueba se hace a mano. |
| La compuerta de divergencia informa una cuenta, un grupo o una carpeta de grupo sin declarar | Alguien lo creó fuera del archivo del establecimiento | Decidir: declararlo en `sites/<slug>/site.sh`, o eliminarlo a mano con el comando que la nota nombra. La suite nunca borra cuentas ni carpetas de forma automática. |
