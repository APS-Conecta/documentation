---
tipo: referencia
audiencia: desarrollo
apps: [instalador]
resumen: "El lugar único de la instalación de un centro: el fork de AIO, el paquete del host, el Provisionador, la publicación firmada y los runbooks de aps/."
---
# instalador

## Resumen

instalador es el lugar único que posee la instalación de un centro: es el fork de [nextcloud/all-in-one](https://github.com/nextcloud/all-in-one) —un espejo `main` byte a byte más una lista de rutas propias— y, además, el paquete del host `aps-conecta`, el Provisionador del asistente, el ejecutor de aprovisionamiento, la cadena Replay/Images y la cadena de publicación firmada que lo reemplazó todo cuando absorbió al repositorio APS-Conecta/AIO, que se eliminó después; su historia de commits sigue completa aquí.
Una etiqueta de instalador es la única identidad de una versión: publica las veinte imágenes bajo `ghcr.io/aps-conecta/*`, arma el paquete compuesto firmado que el bootstrap de una línea descarga y emite el manifiesto de la versión.
La mitad de definición de la suite —aplicaciones vendorizadas con su `VENDOR`, registro DEIS de establecimientos, datos y tema— sigue en gestion; el empaquetado la congela en su referencia al armar cada versión, y el horneado de imágenes hace lo propio.
El archivo `VERSION`, de una línea, es la etiqueta de la versión; `aps/CHANGELOG.md` lleva la entrada fechada, y el CLI lo lee primero.
Los runbooks viven en `aps/`: `INSTALLER.md`, en inglés, y `GUIA-CLINICA.md`, en español, para quien instala; `RELEASING.md`, el ciclo de la clave de firma; y `MIGRATION.md`, el traspaso de las clínicas existentes y el retiro de AIO.

Cómo se mantiene la cola de parches del fork está en {doc}`AIO </desarrollo/aio>`; lo que los parches cambian en una instalación, en {doc}`AIO </administracion/aio>`.

## Tabla

| Compuerta | Comando | Cuándo corre | Qué prueba |
|---|---|---|---|
| Búsqueda de secretos | `gitleaks detect` | Cada pull request y cada push a `main` (`ci.yml`) | Ningún secreto en el historial; los hallazgos del primer arranque se fijan en un `.gitleaksignore` propio. |
| Compuerta local | `bash scripts/test.sh` | Cada pull request y cada push a `main` (`ci.yml`); también en local | El barrido estático sobre `scripts/`, `provisioning/`, `host/`, `patches/` e `install.sh`; las autopruebas herméticas del Provisionador, del paquete del host, del bootstrap, del empaquetado de versiones y de la migración a AIO; y las fijaciones de canal: ninguna URL de gestion en los archivos de entrada, la clave de `installer.pub` de acuerdo con la del bootstrap, y los runbooks en su casa `aps/`. |
| Paridad del espejo | `bash scripts/replay.sh parity` | En la cadena Replay | `main` refleja upstream byte a byte salvo las rutas propias y la declaración de `readme.md`. |
| Reproducción y compuertas | `bash scripts/replay.sh replay`, `brand-gate.sh`, `acquisition-gate.sh` | Cadena Replay, diaria | La cola completa sobre la punta de upstream, con la regla de cobertura y la regla de los tres resultados. |
| Instalación limpia | `cleanboot.yml` | Pull requests y programación | Una instalación desde cero por el bootstrap real —suma y firma verificadas—, con los pisos de recursos rebajados y los datos comunales omitidos para el ensayo; publica el artefacto `uso.json` del servidor de ensayo. |
| Publicación | `release.yml` | Cada etiqueta `v*` | Compuertas verdes, las veinte imágenes en la etiqueta, el paquete armado, firmado con minisign y comprobado contra la clave pública; la publicación lleva los cinco activos: el paquete, sus sumas, su firma, el instalador de una línea y el manifiesto. |

## Notas

### El bootstrap de una línea

```console
curl -fsSL https://github.com/APS-Conecta/instalador/releases/download/vX.Y.Z/apsconecta-vX.Y.Z-install.sh | sudo bash
```

El ancla de confianza es la URL de la versión, más TLS: el archivo lleva dentro la suma sha256 del paquete y la clave pública de la firma, y un archivo truncado es un error de sintaxis, nunca una media instalación.
Desempaca la suite en `/opt/aps-conecta/instalador` y guarda el paquete en `/opt/aps-conecta/paquete`, donde la revisión previa lo vuelve a verificar —suma y firma— sin red, y la guía clínica enseña la verificación a mano con `signify-openbsd` y `sha256sum -c`.

### Las dos mitades del paquete

La mitad de instalador sale de `git archive` de la etiqueta, nunca de un árbol de trabajo; la mitad de gestion se clona congelada en la misma referencia y trae `provisioning/apps` con sus `VENDOR`, el registro `sites`, los datos y el tema.
El empaquetado es determinista: dos corridas sobre la misma etiqueta producen el mismo sha256, y una `VERSION` que no coincide con la etiqueta, o una clave pública de marcador de posición, cortan la publicación en rojo.

### La corrección de red con consentimiento

Cuando la publicación del dominio en el paso 6 del asistente falla porque el servidor no alcanza su propio dominio, la tarjeta «La red del servidor» ofrece «Sí, corregir»: un consentimiento explícito ejecuta `sudo aps-conecta red --dominio D --arreglar`, que instala dnsmasq con DNS dividido, escribe `daemon.json` y reinicia Docker una sola vez; la preparación se repite sola después, y ejecutar la corrección de nuevo no cambia nada.

### Pisos de recursos y datos comunales

La revisión previa informa dos niveles para memoria y disco —mínimo, la línea roja, y recomendado—, anulables por entorno para los ensayos.
La instalación silenciosa termina importando los datos comunales del centro (`territorio:import --actor instalador`), e importar de nuevo termina en «0 creados» por archivo.

### Migración y retiro

Una clínica instalada desde un clon de gestion sigue funcionando: el clon queda inerte al lado de la copia nueva y su retiro es una línea documentada en `aps/MIGRATION.md` §10, con la lista completa de retiro de AIO en §11 —incluido el día en que su programación de Replay se apaga.

### Deuda técnica y límites

- La clave pública de `installer.pub` es un marcador de posición: el ciclo de claves de `aps/RELEASING.md` la reemplaza antes de la primera versión.
- Ninguna instancia de producción existe todavía: la primera versión publicada es el hito que abre la vuelta de aceptación.
- La programación diaria de Replay se activa una vez en la pestaña Actions, y ese mismo día se desactiva la de AIO.

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/instalador>
```
