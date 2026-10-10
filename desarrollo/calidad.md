---
tipo: guia
audiencia: desarrollo
apps: [gestion, farmacia, estadistica, territorio, epidemiologia, IntraVox, aps-common, repo-docs, documentation]
resumen: "Las compuertas que corre cada repositorio antes de fusionar —documentación, pruebas, paquete, deriva, humo y arranque limpio— y qué prueba cada una."
---
# Calidad

## Objetivo

Correr las compuertas de un repositorio antes de abrir un pull request y saber qué prueba cada una. La regla de la organización es correr la compuerta propia del repositorio antes del pull request; CI corre los mismos chequeos. Un paso que no se pudo correr se nombra en el pull request como no corrido, nunca como aprobado. Esta página dice qué prueba cada compuerta y deja que la compuerta imprima sus cifras.

| Compuerta | Dónde corre | Qué prueba |
|---|---|---|
| Documentación (`docs`) | Repositorios con el workflow canónico de repo-docs | Las reglas de documentación de la organización, el título del pull request en inglés y los secretos de sus commits |
| Pruebas, paquete y deriva de aps-common | Cada aplicación propia | Que el código pasa sus pruebas, que el paquete confirmado es la compilación de `src/` y que las copias de aps-common están al día |
| Humo de la aplicación | farmacia y estadistica, contra una instancia desechable | El cableado real: cabeceras OCS, escrituras, rechazos, paquete y contrato |
| Chequeos estáticos de gestion | Todo pull request de gestion | Que la receta de la suite es coherente sin levantar nada |
| Deriva de la organización | CI de gestion | Que las aplicaciones comparten la forma de sus pruebas, sus objetivos, sus reglas de ESLint y su copia de aps-common |
| Clean boot | Pull requests de gestion que tocan la instalación, y cada semana | Que un establecimiento se instala desde cero en AIO y converge |
| Compilación del sitio | Este repositorio | Que el sitio compila sin advertencias, fiel a sus fuentes y con el nombre del producto |

## Requisitos

- Docker: las pruebas de PHP de las aplicaciones, su instancia de prueba y la pila AIO que prueba el humo de gestion corren en contenedores.
- Node.js y `npm ci` en cada aplicación; las aplicaciones usan npm, no pnpm.
- Python 3 para el verificador de documentación.
- En una aplicación propia, la copia hermana de aps-common en `../aps-common`. aps-common es privado: si el clon falla, los pasos que lo necesitan se nombran como no corridos, y ningún workflow se edita para sortearlo.

## Pasos

### En todo repositorio: la compuerta de documentación

1. Ejecutar el verificador desde la raíz del repositorio:

   ```bash
   python3 .github/repo-docs.py check . --offline
   ```

2. Leer el código de salida: 0 significa sin errores y 1, al menos uno. Los avisos nunca fallan la corrida.

El verificador vive copiado en cada repositorio como `.github/repo-docs.py`; la regla `canon-drift` mantiene las copias idénticas al motor de repo-docs, el único lugar donde se edita. En CI, el workflow `docs` corre además `pr-gate`, que exige un título de pull request en inglés, y la regla de secretos revisa con gitleaks solo los commits del pull request. Sus reglas cubren, entre otras, la licencia declarada, los enlaces rotos, los secretos, los comandos documentados que no existen y, en este sitio, la estructura de cada página. El motor está en {doc}`/desarrollo/repo-docs`.

### En una aplicación propia (plantilla farmacia)

1. Clonar aps-common junto al repositorio, en `../aps-common`, si falta.
2. Ejecutar el objetivo `aps-drift` del Makefile.
3. Instalar, revisar, probar y recompilar el frontend, y exigir que `js/` no cambie:

   ```bash
   npm ci
   npm run lint-js
   npm test
   npm run build
   git diff --exit-code js/
   ```

4. Ejecutar el objetivo `test`, siempre después de `npm test`: copia en `vendor/` un archivo de `node:test` con el que `npm test` fallaría.
5. Ejecutar los objetivos `instance-up` y `smoke`, y al final `instance-clean`.
6. Ejecutar la compuerta de documentación.

| Paso | Qué prueba |
|---|---|
| `aps-drift` | Que las copias confirmadas de aps-common —`vendor/aps/common/src`, `src/aps/` y el stub de prueba— son iguales al paquete. Usa `git status --porcelain`, que también ve un renombre |
| `npm run lint-js` | ESLint sobre `src/`; la compuerta de la organización exige que cada configuración conserve `no-undef` como error y el plugin de Vue |
| `npm test` | Las pruebas del frontend con Vitest |
| `npm run build` y `git diff` | Que `js/` es exactamente la compilación de `src/`: el paquete confirmado es el despliegue |
| `test` | Las pruebas unitarias de PHPUnit, en un contenedor PHP sin Nextcloud |
| `smoke` | Contra una instancia real: la respuesta 412 sin la cabecera `OCS-APIRequest` y 200 con ella, una escritura sin token CSRF, los rechazos 400 y 404, el icono, los huecos de `.htaccess`, el paquete confirmado y que `openapi.json` se regenera sin diferencias |

En CI, `aps-drift` corre antes que `test`: el `composer install` del contenedor de pruebas corre como root y copia aps-common en `vendor/aps/common`, y el `rm -rf` de `aps-sync` no puede borrar esos archivos en el runner.

Las demás aplicaciones varían sobre la plantilla:

- **territorio** agrega el objetivo `notices`, que exige que cada paquete distribuido figure en `THIRD-PARTY-NOTICES.md`, y un job que regenera la especificación OpenAPI contra una instancia y exige que coincida con la confirmada.
- **epidemiologia** corre sus pruebas unitarias contra el código del servidor que trae la imagen y el chequeo del paquete. Su humo necesita una instancia aprovisionada con un usuario administrador y una contraseña de aplicación, y sigue siendo manual.
- **IntraVox** corre pruebas unitarias de PHP, análisis estático con PHPStan, un guardián del empaquetado y guardianes del frontend, entre ellos la tabla de rutas al día y la cobertura de OpenAPI.

### En aps-common

El paquete compartido corre su suite de PHP con el objetivo `test`, dentro de `Dockerfile.test`, que incluye la extensión `intl`: sin ella, las pruebas de acentos pasan sin correr. La mitad JS corre su corpus de conformidad:

```bash
node --test js/*.test.js
```

El `aps-drift` de cada aplicación prueba que su copia coincide con el paquete; solo este job prueba que el paquete funciona.

### En gestion

| Job | Cuándo | Qué prueba |
|---|---|---|
| Secret scan | Todo pull request y cada push a `main` | gitleaks sobre todo el historial, con los hallazgos ocultos en el registro; un hallazgo falla el job |
| Static gate | Todo pull request y cada push a `main` | Los objetivos `setup` y `test` sin ninguna pila: los chequeos estáticos |
| Org drift | Todo pull request y cada push a `main` | `scripts/check-org-drift.sh` sobre territorio, farmacia y estadistica |
| Clean boot | Pull requests que cambian lo que lee una instalación, cada lunes y a pedido | La instalación completa sobre un banco de pruebas AIO desechable |

Los chequeos estáticos de `test` corren todos y suman los fallos, de modo que un fallo no oculta los demás. Entre ellos: que la configuración de Compose resuelve, que todo script rastreado pasa `bash -n`, que cada paquete vendorizado coincide con el sha256 de su `VENDOR`, que la tabla de licencias coincide con el `info.xml` de cada paquete, que las bibliotecas vendorizadas del mapa conservan sus bytes, que todo servicio vuelve tras un reinicio, que ningún `.env` lleva los secretos publicados de la plantilla, que cada SVG del tema se analiza como XML y que cada `url()` de `server.css` existe en disco. Varios chequeos incluyen su mitad negativa, que les da una entrada alterada y exige el fallo: una compuerta que no puede ponerse roja no es una compuerta.

Con una pila AIO en marcha, `test` agrega chequeos contra las plantillas del contenedor —entre ellos, que las llamadas a `Template::printPage()` del núcleo sigan siendo las siete conocidas— y corre el humo y el humo de oficina. Sin esa pila, los informa como omitidos.

El humo (`smoke`) prueba una instancia AIO en marcha: el contenedor y la instalación, PostgreSQL y Redis, `/status.php` con el nombre del producto, los trabajos de fondo por cron, el manifiesto web, la política de aplicaciones, que el inicio de sesión no ofrezca mantener la sesión, que ninguna aplicación parchada conserve su firma, que las pantallas heredadas sigan fuera del alcance HTTP —un host no confiable rebota con 302— y que el tema activo traiga `core/css/guest.css` y `defaults.php`, que la carpeta del administrador no traiga los archivos de ejemplo, que la tienda esté apagada, que la dirección del editor de oficina coincida con cómo se alcanza la instancia y que el mapa base se sirva en `/tiles/`. El humo de oficina prueba que Euro-Office responde por su ruta pública, que su versión es de la línea 9.3 emparejada con el conector 11.0.5 y que la imagen viene de uno de los dos orígenes que la suite acepta.

La deriva de la organización compara territorio, farmacia y estadistica: `phpunit.xml` y `phpunit.integration.xml` byte a byte, los objetivos centrales del Makefile, las reglas fijadas de ESLint y que sus copias de aps-common sean iguales entre sí y al paquete. No compara `ci.yml`, que es propio de cada aplicación por diseño.

Clean boot instala un establecimiento generado con el mismo comando silencioso que usa una clínica, y termina con el contrato de entrega: una segunda siembra que no escribe nada, la compuerta de divergencia en verde, un reinicio con la tienda apagada, una nueva siembra que converge y el objetivo `test` con el humo de oficina respondiendo. Una segunda siembra no debe escribir nada: el registro de la siembra es la aserción.

### En este sitio de documentación

El workflow `build` corre estos objetivos del Makefile del sitio:

```bash
make html
make test
make fidelity
make term-check
make rebrand-check
make linkcheck
make check-site
```

| Objetivo | Qué prueba |
|---|---|
| `html` | Que el sitio compila con `-W --keep-going` después de obtener la marca, el clon upstream y las páginas generadas; la tabla de componentes falla si gestion distribuye algo que `componentes.yml` no declara, o al revés |
| `test` | Las pruebas unitarias de `tools/` y las autopruebas de los generadores |
| `fidelity` | Que cada bloque tejido dice lo que dice su fuente upstream, con cobertura completa |
| `term-check` | Las formas aprobadas de `glosario.yml` y el registro «usted» o impersonal |
| `rebrand-check` | Que el sitio compilado nombra el producto «APS Conecta Gestión» |
| `linkcheck` | Que los enlaces de la prosa de APS responden |
| `check-site` | El sitio servido bajo un subdirectorio, con Playwright: marca, fuentes, tema y aislamiento de terceros |

## Verificación

- Cada comando de los pasos termina con código 0.
- El `test` de gestion imprime una línea `ok:` o `FAIL:` por chequeo y una línea `skipped:` por cada bloque que no pudo correr.
- El pull request nombra lo que corrió y lo que no.

## Problemas frecuentes

- **`npm test` falla después del objetivo `test`.** El objetivo `test` deja en `vendor/` un archivo de `node:test`. Correr `npm test` antes que `test`.
- **El clon de aps-common falla con «could not read Username».** aps-common es privado. En CI se clona con una llave de despliegue; sin ella, el paso falla a la vista.
- **Las rutas de una instancia nueva responden 404.** Los procesos web guardan en caché las rutas y el estado de las aplicaciones; `instance-up` reinicia el servidor después de activar la aplicación.
- **El `test` de gestion informa «skipped: no running AIO stack».** Es la compuerta solo estática: no hay una pila AIO en marcha.
- **Clean boot no corre en un pull request.** El workflow filtra rutas: documentación, tema y `apps/` no cambian lo que instala una clínica, así que no lo disparan.
