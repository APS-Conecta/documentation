---
tipo: guia
audiencia: administracion
apps: []
resumen: "Instalar la suite en un servidor limpio: el comando único, las cinco pantallas del asistente, el archivo de contraseñas, el personal y las copias."
---
# Instalar APS Conecta Gestión AIO

## Objetivo

Instalar APS Conecta Gestión AIO para un establecimiento (un CESFAM, CECOSF o SAPU) en un servidor limpio.

Un solo comando prepara el servidor e imprime un enlace. El enlace abre el asistente de instalación, que recorre cinco pantallas: «Centro», «Dirección», «Equipos», «Revisar» y «Listo». El asistente no pide contraseñas y la instalación no abre puertos en el router.

Al terminar, el personal abre la suite en `https://<centro>.gestion.apsconecta.cl`, con un certificado real, y el archivo de contraseñas reúne la primera contraseña de cada cuenta.

## Requisitos

- Un servidor con:
  - procesador x86_64;
  - al menos 2 núcleos de CPU y 6 GiB de memoria;
  - al menos 20 GB libres en `/var/lib/docker` (o en `/var/lib`, si Docker no está instalado);
  - Ubuntu o Debian, si Docker no está instalado: el comando instala Docker Engine solo en esos sistemas;
  - acceso a internet;
  - los puertos 80, 443, 3478, 8080, 8081 y 8443 libres.
- Acceso de administrador (`sudo`) en el servidor.
- Un computador o teléfono conectado a la red del establecimiento, para abrir el asistente.
- Los datos del personal: usuario, nombre, apellidos, correo y grupos de cada persona.

Con al menos 4 núcleos y 8 GiB de memoria, la suite instala además el grabador de llamadas de Talk.

## Pasos

### 1. Ejecutar el comando

1. En el servidor, ejecute:

   ```console
   curl -fsSL https://github.com/APS-Conecta/gestion-aio/releases/latest/download/install.sh | sudo bash
   ```

   El comando descarga la última versión publicada de la suite. Revisa el servidor sin modificar nada, verifica la suma del paquete antes de desempacarlo, instala Docker Engine si falta, inicia el contenedor maestro de la suite y el asistente, e imprime el enlace.

2. Si el servidor no cumple los requisitos, el comando se detiene con «Este servidor no cumple los requisitos de APS Conecta Gestión AIO. No se modificó nada.» y una línea por cada requisito que falta:

   | Línea | Significado |
   |---|---|
   | «la arquitectura del procesador es …; se requiere x86_64» | El procesador no es x86_64 (por ejemplo, ARM). La suite no se instala en ese servidor. |
   | «tiene … GiB de memoria; se requieren al menos 6 GiB» | Falta memoria. |
   | «tiene … núcleo(s) de CPU; se requieren al menos 2» | Faltan núcleos de CPU. |
   | «tiene … GB libres en …; se requieren al menos 20 GB» | Falta espacio en la carpeta indicada. |
   | «Docker no está instalado y el instalador solo lo instala en Ubuntu o Debian (…)» | El servidor no tiene Docker y su sistema no es Ubuntu ni Debian. |

Si el comando ya se ejecutó en ese servidor, volver a ejecutarlo no reinstala nada. Antes de «Listo», imprime un enlace nuevo al mismo asistente, que conserva lo avanzado. Después de «Listo», imprime la dirección de la suite y la ruta del archivo de contraseñas.

### 2. Abrir el asistente

El comando termina con el enlace, su código QR y la huella del certificado del asistente:

```text
Abra este enlace en un computador o teléfono conectado a la red del establecimiento:

    https://<dirección del servidor>:8081/#…

El navegador advertirá que la conexión no es privada: el Provisionador usa un certificado propio
y temporal. Continúe solo si la huella SHA-256 del certificado es:

    AA:BB:…

El enlace sirve una sola vez. Para obtener uno nuevo, vuelva a ejecutar el comando de instalación.
```

1. Abra el enlace, o lea el código QR, en un computador o teléfono conectado a la red del establecimiento.
2. Compare la huella del certificado que muestra el navegador con la que imprimió el comando. Continúe solo si coinciden. El asistente muestra la misma huella bajo sus pantallas, en «Huella SHA-256 del certificado».

El navegador que abre el enlace conserva su sesión hasta «Listo». El asistente guarda su avance en el servidor: si se cierra el navegador o se reinicia el servidor, vuelva a ejecutar el comando y abra el enlace nuevo para seguir donde quedó. Lo mismo vale si el asistente muestra «Este enlace ya se usó o fue reemplazado».

### 3. Centro

1. Busque el establecimiento en el registro DEIS con «Región», «Comuna», «Tipo» y «Nombre».
2. Elija el establecimiento en la lista. El mapa muestra su punto oficial.
3. Si el marcador no está sobre el establecimiento, haga clic en el lugar correcto o arrástrelo. «Volver al punto oficial» lo devuelve a su lugar.
4. Presione «Confirmar centro». El asistente muestra «Centro confirmado: …» con la zona horaria y pasa a «Dirección».

La zona horaria sale de la ubicación: `Pacific/Easter` en Isla de Pascua, `America/Punta_Arenas` en la región de Magallanes y `America/Santiago` en el resto del país. Si el mapa de fondo no carga, el punto oficial se confirma igual.

### 4. Dirección

«Dirección» obtiene por sí sola, del servicio de nombres de APS Conecta, el nombre de la suite: `<centro>.gestion.apsconecta.cl`. No pide ningún dato.

- El nombre sale del nombre corto del establecimiento, en minúsculas, sin tildes, con «ñ» como «n» y con guiones. Si dos establecimientos comparten el nombre corto, se agrega la comuna.
- Cada código DEIS tiene un solo nombre, que no se edita. Una vez obtenido el nombre, el centro ya no puede cambiarse.
- El nombre apunta a la dirección del servidor dentro de la red del establecimiento. El servidor publica esa dirección cada 10 minutos, así que el nombre sigue al servidor si su dirección cambia.
- La suite obtiene un certificado real sin abrir puertos en el router.

1. Espere el mensaje «Dirección asignada: https://…».
2. Presione «Continuar».

Si el servicio de nombres no responde o limita las solicitudes, el asistente lo explica y ofrece «Reintentar».

(instalar-gestion-aio-liberar)=
#### Pedir que se libere el nombre

Si el nombre ya pertenece a otra instalación, por ejemplo una instalación anterior del mismo establecimiento, el asistente muestra «La dirección … ya está en uso por otra instalación. Si este establecimiento ya tenía una instalación, APS Conecta puede liberarla; después presione «Reintentar».».

1. Pida a APS Conecta que libere el nombre. Indique el establecimiento y la dirección del mensaje.
2. Cuando APS Conecta confirme que lo liberó, presione «Reintentar».

Al liberar el nombre, la instalación anterior lo pierde.

(instalar-gestion-aio-router)=
#### Si un computador no abre la dirección

Cuando la suite ya responde, «Listo» comprueba si el computador abre la dirección. Algunas redes descartan las respuestas de DNS que apuntan a direcciones internas, y entonces «Listo» muestra:

> «Este equipo no logra abrir https://…, aunque la suite ya responde en el servidor: el DNS de esta red descarta las respuestas que apuntan a direcciones internas. En el router, permita esas respuestas para gestion.apsconecta.cl (una excepción a la protección contra «DNS rebinding») y vuelva a conectar este equipo a la red. Esta página lo comprobará de nuevo por sí sola.»

1. En el router de la red, agregue `gestion.apsconecta.cl` como excepción a la protección contra «DNS rebinding».
2. Vuelva a conectar el computador a la red.
3. Espere: la página repite la comprobación cada 15 segundos.

Si el mensaje sigue después de la excepción en el router, compruebe que el computador llega al servidor por el puerto 443. Un cortafuegos, una VLAN distinta o un proxy entre el computador y el servidor pueden impedirlo.

### 5. Equipos

1. Escriba los sectores en «Sectores» y los programas en «Programas», uno por línea. Cada uno es un equipo, con su grupo y su carpeta compartida; el asistente los muestra mientras escribe. Por ejemplo, «Norte» es el equipo «Sector Norte», con el grupo `sector-norte` y la carpeta `Sectores/Sector Norte`, y «Cardiovascular» es «Programa Cardiovascular», con el grupo `prog-cardiovascular` y la carpeta `Programas/Cardiovascular`.
2. Presione «Descargar la planilla» y complétela, una persona por línea.
3. Guárdela como CSV y súbala en «Subir la planilla completa». El asistente lista a las personas que creará. Si la planilla tiene errores, muestra cada uno con su número de línea y no carga a nadie: corríjala y súbala de nuevo.
4. Revise la lista. Para quitar a alguien que dejó el establecimiento, use «Retirar».
5. Presione «Continuar».

Cada sector tiene además su cuenta de jefatura. Los sectores y los programas quedan fijos al presionar «Instalar».

#### La planilla del personal

La planilla separa las columnas con «;» y su primera línea las nombra: `usuario;nombre;apellidos;correo;grupos;primer_admin`. El asistente la acepta en UTF-8 o como la guarda Excel en CSV simple.

| Columna | Contenido |
|---|---|
| `usuario` | Hasta 64 caracteres entre letras minúsculas sin tildes, números, puntos y guiones; comienza con una letra o un número. No se repite. |
| `nombre` y `apellidos` | Obligatorios. Juntos suman a lo más 64 caracteres. |
| `correo` | Opcional. Queda guardado en la cuenta de la persona. |
| `grupos` | Los grupos de la persona, separados por espacios, tal como los lista «Grupos que acepta la planilla»: el equipo (`sector-norte`), el rol (`role-medico`) y los demás. |
| `primer_admin` | «sí» para una sola persona, la que administrará la suite; vacío para las demás. |

Cada persona entra además al grupo de todo el personal y a la categoría de su rol. Los usuarios `admin`, `director`, `subdirector`, `jefe.farmacia`, `jefe.some` y los de las jefaturas de sector están reservados para el administrador de la suite y las cuentas de cargo: la planilla los rechaza.

#### Retirar a una persona

1. Marque en la lista a las personas que dejaron el establecimiento.
2. Presione «Retirar». El asistente pregunta: «¿Retirar a …? Su cuenta se desactivará y saldrá de todos los equipos; sus archivos y lo que compartió se conservan, y podrá reactivarse en «Cuentas», en APS Conecta Gestión AIO.»
3. Presione «Confirmar el retiro».

La persona marcada como primer administrador no se retira: marque a otra en `primer_admin` y suba la planilla de nuevo. Una persona retirada sigue retirada aunque se suba otra planilla.

#### Corregir el personal después de «Instalar»

Hasta «Listo», «Equipos» acepta una planilla corregida y «Retirar». Los cambios se aplican al presionar «Reintentar» en «Revisar».

Una planilla corregida actualiza el nombre, el correo y los equipos de cada persona, y la saca de los equipos que ya no lista. Si deja fuera a una persona cuya cuenta la instalación ya creó, esa persona se retira: la lista la muestra como «Retirado/a: ya no está en la planilla». Una persona que aún no tenía cuenta simplemente no se crea. Las cuentas creadas fuera del asistente nunca se retiran.

### 6. Revisar

«Revisar» resume lo que se instalará: el centro, la dirección, los equipos, las personas, las cuentas de cargo, los componentes, las aplicaciones y las copias de seguridad.

1. Revise el resumen.
2. En «Aplicaciones opcionales», marque las que usará el establecimiento: Farmacia, Estadística o Tótem. La elección del primer «Instalar» queda fija.
3. Presione «Instalar».

Los componentes se instalan siempre: Talk, Euro-Office, Imaginary, ClamAV (antivirus), búsqueda de texto completo y HaRP (servidor de aplicaciones externas). En un servidor con al menos 4 núcleos y 8 GiB de memoria, la lista incluye además el «Grabador de Talk», sin que haya que elegirlo.

La página muestra el avance de cada paso de la instalación y de cada contenedor. Descargar e iniciar los contenedores puede tardar varios minutos. La instalación sigue en el servidor aunque se cierre la página.

Un paso que falla no detiene a los que no dependen de él. Sus dependientes quedan «En espera», y la página dice «Algunos pasos no se completaron; su motivo está en rojo. Presione «Reintentar».».

1. Lea el motivo en rojo de cada paso y corrija lo que indique.
2. Presione «Reintentar». Se repiten solo los pasos que no se completaron o quedaron en espera.

Con todos los pasos completados, la instalación compara la suite en marcha con lo declarado. Una diferencia vuelve a poner en rojo su paso. «Listo» aparece solo cuando todo está completo y la comparación no encuentra diferencias. Si un motivo se repite, contacte a APS Conecta; el registro del asistente se lee en el servidor con `journalctl -u aps-provisionador`.

### 7. Listo

«Listo» muestra «APS Conecta Gestión AIO quedó instalada. El personal del establecimiento la abre en esta dirección:» y la dirección. Al llegar a «Listo», el asistente se cierra y su enlace deja de funcionar.

1. Presione «Descargar el archivo de contraseñas» y guarde el archivo en un lugar seguro. El botón funciona mientras la página sigue abierta.
2. Lea el mensaje bajo la dirección. Si dice que el computador no abre la dirección, siga [Si un computador no abre la dirección](#instalar-gestion-aio-router).
3. Comparta la dirección con el personal y entregue a cada persona su usuario y su primera contraseña.

### El archivo de contraseñas

El archivo `contrasenas.txt` contiene:

- el usuario `admin`, administrador de la suite, y su contraseña;
- la frase de contraseña de la página de AIO, para las copias de seguridad y la restauración;
- la contraseña de cifrado de las copias de seguridad de AIO, necesaria para restaurar una copia en otro servidor;
- el nombre, el usuario y la primera contraseña de cada persona y de cada cuenta de cargo.

El servidor conserva una copia, legible solo por root:

```console
sudo cat /var/lib/aps-conecta/provisionador/contrasenas.txt
```

### El personal después de la instalación

Después de «Listo», la instalación no vuelve a tocar las cuentas: el personal se administra en la página «Cuentas» de APS Conecta Gestión AIO. Entran a ella la persona marcada en `primer_admin` y el usuario `admin`.

- «Cuenta nueva» agrega a una persona; sus grupos le dan sus equipos y carpetas.
- «Deshabilitar cuenta» impide que la persona inicie sesión y conserva sus archivos. «Habilitar cuenta» la reactiva; a quien se retiró durante la instalación hay que volver a asignarle sus grupos.
- «Eliminar cuenta» borra la cuenta.

La planilla del personal ya no se aplica después de «Listo».

### Las copias de seguridad

La copia de seguridad de AIO queda activa sin configurar nada. Corre cada noche a las 06:00 UTC (las 02:00 o las 03:00 en Chile continental) y guarda las copias en la carpeta `/var/backups/aps-conecta` del servidor. Durante la copia, los contenedores se detienen y se reinician al terminar. Las copias están cifradas: para restaurar una en otro servidor se necesita la contraseña de cifrado del archivo de contraseñas.

Para guardar las copias en otro disco o restaurar una copia, use la página de AIO en `https://<centro>.gestion.apsconecta.cl:8080`, con la frase de contraseña del archivo de contraseñas. Mientras la suite está en marcha, esa página bloquea el inicio de sesión directo y explica cómo desbloquearlo.

## Verificación

- «Listo» muestra la dirección de la suite y «Este equipo abre https://… correctamente.».
- La dirección abre la página de inicio de sesión de APS Conecta Gestión AIO sin advertencia de certificado.
- Una persona de la planilla inicia sesión con su usuario y la primera contraseña del archivo de contraseñas.
- Una persona retirada no puede iniciar sesión.

## Problemas frecuentes

| Mensaje | Qué hacer |
|---|---|
| «Error: el paquete descargado no coincide con su suma de verificación. …» | La descarga llegó incompleta o alterada y no se instaló nada. Vuelva a ejecutar el comando. |
| «Error: no se pudo iniciar el contenedor maestro. Revise que los puertos 80, 8080 y 8443 estén libres …» | Otro servicio usa uno de esos puertos. Libérelo y vuelva a ejecutar el comando. |
| «Este enlace ya se usó o fue reemplazado. …» | Vuelva a ejecutar el comando en el servidor y abra el enlace nuevo. |
| «No se pudo conectar con el servicio de nombres de APS Conecta. …» | Revise la conexión a internet del servidor y presione «Reintentar». |
| «El servicio de nombres de APS Conecta limita las direcciones que se obtienen desde una misma red cada día y cada semana. …» | Presione «Reintentar» más tarde. |
| «La dirección … ya está en uso por otra instalación. …» | Siga [Pedir que se libere el nombre](#instalar-gestion-aio-liberar). |
| «La planilla tiene errores: corríjalos y súbala de nuevo.» | Corrija cada línea que indica el asistente y suba la planilla otra vez. |
| «No se pudo confirmar el cierre del asistente. …» | Vuelva a ejecutar el comando: imprime un enlace nuevo para descargar el archivo de contraseñas o, si el asistente ya se cerró, la ruta del archivo en el servidor. |
