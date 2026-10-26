---
tipo: referencia
audiencia: desarrollo
apps: [gestion]
resumen: "El repositorio de la suite: el fork de AIO en un solo árbol, el paquete del host, el Provisionador, el manifiesto de aplicaciones y la publicación firmada."
---
# instalador

## Resumen

instalador es el repositorio de la suite APS Conecta Gestión: el fork de [nextcloud/all-in-one](https://github.com/nextcloud/all-in-one) —un solo árbol, con los cambios del fork como bytes confirmados en `main`—, el paquete del host `aps-conecta`, el Provisionador que instala un centro, el ejecutor de aprovisionamiento, el manifiesto de aplicaciones de la suite y la cadena de publicación firmada. Absorbió al repositorio APS-Conecta/AIO, que se eliminó después; su historia de commits sigue completa aquí.

Una etiqueta de instalador es la única identidad de una versión: publica las veinte imágenes bajo `ghcr.io/aps-conecta/*`, arma el paquete firmado que el arranque de una línea descarga y adjunta el manifiesto de la versión. El paquete es el árbol de la etiqueta —tema, datos, registro de establecimientos y manifiesto— y no lleva bytes de ninguna aplicación: cada una llega de su propia publicación firmada o de la tienda con la puerta acotada.

El archivo `VERSION`, de una línea, es la etiqueta de la versión; `aps/CHANGELOG.md` lleva la entrada fechada, y el CLI lo lee primero. Los runbooks viven en `aps/`: `INSTALLER.md`, en inglés, y `GUIA-CLINICA.md`, en español, para quien instala; `RELEASING.md`, el ritual de publicación y el ciclo de la clave de firma.

Cómo se mantiene el fork de AIO está en {doc}`AIO </desarrollo/aio>`; lo que los cambios del fork hacen en una instalación, en {doc}`AIO </administracion/aio>`.

## Tabla

| Compuerta | Comando | Cuándo corre | Qué prueba |
|---|---|---|---|
| Búsqueda de secretos | `gitleaks detect` | Cada pull request y cada push a `main` (`ci.yml`) | Ningún secreto en el historial; los hallazgos del primer arranque se fijan en un `.gitleaksignore` propio. |
| Compuerta local | `bash scripts/test.sh` | Cada pull request y cada push a `main` (`ci.yml`); también en local | El barrido estático sobre `scripts/`, `provisioning/`, `host/` e `install.sh`; las autopruebas herméticas del Provisionador, del paquete del host, del arranque de una línea, del empaquetado de versiones, del resolvedor de publicaciones y de las fases de provisión; y las fijaciones de canal. |
| Compuerta de marca | `bash scripts/brand-gate.sh .` | Cada pull request, cada push y cada etiqueta (`ci.yml` y la cadena de publicación) | Que el árbol cumple la declaración del fork: la identidad y el español de Chile en cada superficie declarada, fila por fila. |
| Compuerta de adquisición | `bash scripts/acquisition-gate.sh .` | Cada pull request, cada push y cada etiqueta (`ci.yml` y la cadena de publicación) | Que la instalación no llega a ninguna fuente ajena a APS Conecta y que la tienda de aplicaciones abre solo por sus comandos acotados. |
| Enrojecimiento | `gate-red-proof` | Cada pull request (`ci.yml`) | Que las compuertas pueden fallar: inyecta regresiones conocidas —un centinela revertido, una referencia al registro de upstream, un permiso retirado— y exige que la compuerta correspondiente salga en rojo en cada una. |
| Conjunto construido | `bash scripts/lockstep.sh` | El trabajo de manifiesto del flujo Images, antes del anuncio | Que el conjunto de imágenes anunciado proviene de un solo árbol: cada construcción resuelve el mismo commit, y una nueva imagen es una entrada en la lista única. |
| Instalación limpia | `cleanboot.yml` | Pull requests y programación | Una instalación desde cero por el arranque real —suma y firma verificadas—, por dominio y por la IP del ejecutor, con los brazos de la actualización: una normal desde un candado viejo, una firma alterada que no mueve nada y `--revisar` que no escribe. |
| Publicación | `release.yml` | Cada etiqueta `v*` | Compuertas verdes, las veinte imágenes en la etiqueta, el paquete armado, firmado con minisign y comprobado contra la clave pública; la publicación lleva los cinco activos: el paquete, sus sumas, su firma, el instalador de una línea y el manifiesto. |

## Notas

### El arranque de una línea

```console
curl -fsSL https://github.com/APS-Conecta/gestion/releases/download/vX.Y.Z/apsconecta-vX.Y.Z-install.sh | sudo bash
```

El ancla de confianza es la URL de la versión, más TLS: el archivo lleva dentro la suma sha256 del paquete y la clave pública de la firma, y un archivo truncado es un error de sintaxis, nunca una media instalación.
Desempaca la suite en `/opt/aps-conecta/instalador` y guarda el paquete en `/opt/aps-conecta/paquete`, donde la revisión previa lo vuelve a verificar —suma y firma— sin red, y la guía clínica enseña la verificación a mano con `signify-openbsd` y `sha256sum -c`.

### El paquete es el árbol de la etiqueta

El paquete compuesto sale de `git archive` de la etiqueta, nunca de un árbol de trabajo, y es ese árbol —tema, datos, registro de establecimientos y manifiesto— sin bytes de ninguna aplicación.
El empaquetado es determinista: dos corridas sobre la misma etiqueta producen el mismo sha256, y una `VERSION` que no coincide con la etiqueta, o una clave pública distinta de la publicada, cortan la publicación en rojo.

### La corrección de red con consentimiento

Cuando la publicación del dominio en el paso 6 del asistente falla porque el servidor no alcanza su propio dominio, la tarjeta «La red del servidor» ofrece «Sí, corregir»: un consentimiento explícito ejecuta `sudo aps-conecta red --dominio D --arreglar`, que instala dnsmasq con DNS dividido, escribe `daemon.json` y reinicia Docker una sola vez; la preparación se repite sola después, y ejecutar la corrección de nuevo no cambia nada.

### Pisos de recursos y datos comunales

La revisión previa informa dos niveles para memoria y disco —mínimo, la línea roja, y recomendado—, anulables por entorno para los ensayos.
La instalación silenciosa termina importando los datos comunales del centro (`territorio:import --actor instalador`), e importar de nuevo termina en «0 creados» por archivo.

### Instalaciones previas

Una clínica instalada desde un clon de gestion sigue funcionando sin cambios: el instalador no la lee ni la sigue, sirve instalaciones limpias solamente, y la migración se retiró con la doctrina de la v0.5.0.

### Deuda técnica y límites

- Ninguna instancia de producción existe todavía: la primera versión publicada es el hito que abre la vuelta de aceptación.
- Los límites que ve un establecimiento —los mensajes PHP en inglés, el código muerto de deSEC— están en {doc}`AIO </administracion/aio>`.

```{toctree}
:maxdepth: 1

```
