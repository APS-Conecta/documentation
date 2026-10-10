---
tipo: explicacion
audiencia: desarrollo
apps: [Databases]
resumen: "Los corpus de referencia de la suite: normativa sanitaria literal, catálogo de APIs de salud verificado por sondeo y publicaciones REM del DEIS."
---
# Databases

## Contexto

Databases reúne los corpus de referencia de la suite: lo que publica el sector salud chileno, versionado tal como se publicó. Tiene tres colecciones, una por materia.

Es una biblioteca, no una aplicación: nada se despliega, abre un puerto ni corre como servicio. Tampoco es la ficha clínica ni una fuente de datos de pacientes: los corpus contienen material agregado, público o normativo, y `Legal/` es la autoridad sobre dónde está ese límite. No es un espejo en vivo: los estatutos y `REMs/` son instantáneas fechadas de lo que el publicador entregó un día dado, y una edición nueva es una instantánea nueva, nunca una edición de la anterior.

El código del repositorio es AGPL-3.0-or-later. Las publicaciones oficiales versionadas (estatutos, manuales REM, formularios y diccionarios) son textos de sus publicadores, bajo sus propios términos, y se guardan literales: se versionan tal cual y nunca se editan aquí.

estadistica lee el DEIS en tiempo de ejecución, y los destinos de ingesta de los que depende están catalogados aquí; el trabajo de integración de APIs de la suite parte de `APIs/`. El catálogo de repositorios registra esa relación como una arista doctrinal, no de construcción ({doc}`/_generated/catalogo`). Cada entrada del catálogo de APIs nombra sus consumidores en `aps_use`, así que el catálogo es el registro del radio de impacto cuando una fuente catalogada cambia de forma incompatible.

## Diseño

### Tres colecciones

| Colección | Contenido | Fuente de verdad | Vistas generadas |
| --- | --- | --- | --- |
| `APIs/` | El catálogo de APIs del sector salud chileno: cuáles existen, cuáles están vivas, cuáles son gratuitas y cómo se integra cada una, verificado por sondeo HTTP y no por lectura de documentación. | `APIs/catalog.yaml` | `APIs/exports/INDEX.md` (objetivo `docs`) y `APIs/exports/feeds.opml` (objetivo `feeds`) |
| `Legal/` | Los seis estatutos que enmarcan APS Conecta, convertidos desde los PDF oficiales de la BCN a Markdown y JSON y verificados carácter por carácter contra los PDF. | Los PDF oficiales y los punteros de `Legal/obligaciones.yaml` | `Legal/md/`, `Legal/json/` y `Legal/OBLIGACIONES.md` |
| `REMs/` | Las publicaciones oficiales REM del DEIS (manuales, diccionarios y formularios) del ciclo 2026. | Los archivos mismos; `REMs/README.md` es el inventario | Ninguna, por decisión |

Las herramientas del catálogo viven en `APIs/` y piden Python 3 con PyYAML. El conversor del corpus legal, `Legal/convertir.py`, pide además `pdftotext` de poppler para regenerar o volver a verificar `Legal/`. El mapa de módulos se genera al compilar:

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/databases>
```

### APIs: el sondeo observa, la verificación juzga

El `Makefile` de `APIs/` separa dos objetivos, y solo uno puede fallar (ADR-0002):

- `probe` toca la red, observa y nunca falla: una API muerta es un hallazgo, no un error. Escribe la evidencia fechada en `APIs/reports/probe-<fecha>.md` y reescribe `status:` en el catálogo cuando la realidad contradice lo declarado. Esa contradicción es la deriva, y queda escrita el mismo día en que se observa, con el antes y el después en el informe.
- `verify` no toca la red, es determinista y juzga. Falla solo por lo que una persona puede corregir: un campo obligatorio ausente, un valor de enumeración no declarado, identificadores duplicados, una entrada `scope: excluded` sin motivo, un `status: gated` que no dice cómo pedir credenciales, un `status: dead` todavía marcado `scope: in`, y la ausencia de sondeo o un sondeo con más de 30 días.

El último guardia es el que importa: `MAX_PROBE_AGE_DAYS = 30` en `APIs/src/common.py`. El catálogo no puede envejecer en silencio, porque el silencio mismo pone la compuerta en rojo, y nada en el repositorio «refresca» la fecha del sondeo.

Cada entrada tiene uno de cuatro estados, que solo `probe` escribe:

| Estado | Significado |
| --- | --- |
| `live` | Responde lo esperado. |
| `gated` | Responde 401 o 403: existe y está protegida; el campo `access` dice cómo obtener credenciales. |
| `geoblocked` | Resuelve el DNS pero rechaza la conexión; se vuelve a sondear desde Chile. |
| `dead` | NXDOMAIN o un loopback estacionado: desapareció, no está bloqueada. |

El índice generado no es alfabético (ADR-0003). La clave de orden es estándar, estado, alcance e identificador, y la lista de estándares fija `fhir-r4`, `hl7v2`, `dicomweb`, `rest` y `file`, en ese orden. Así el equivalente FHIR de una fuente aparece siempre sobre su gemelo REST, porque el programa nacional de interoperabilidad publica sus guías de implementación en FHIR R4. Dentro de un estándar, una fuente que muere se hunde en su grupo.

`probe` reescribe `status:` editando el texto y no volcando el YAML, porque un volcado borraría los comentarios, que llevan la mitad del conocimiento. El sondeo dejó tres lecciones de integración que ninguna documentación registraba y que viven en el código con sus comentarios:

1. **Cadenas TLS incompletas.** Casi ningún host del Estado está geobloqueado: lo que falla es una cadena TLS a la que le falta la CA intermedia. Los navegadores la disimulan, pero `curl`, Python y el cliente HTTP de Nextcloud (`IClientService`, {doc}`/desarrollo/plataforma/digging-deeper/http-client`) no. La corrección es un paquete de CA propio, nunca desactivar la verificación.
2. **WAF según el User-Agent.** Algunos cortafuegos de aplicaciones responden 405 según el User-Agent; el sondeo reintenta, y en producción conviene recordarlo porque Nextcloud envía su propio User-Agent.
3. **Un tiempo de espera aislado no es un diagnóstico.** Un host falla el saludo TLS con concurrencia y responde 200 en serie; sin el reintento, un tropiezo transitorio reescribía `live` como `geoblocked` en el catálogo.

### Legal: la ley literal desde fuentes oficiales

| Norma | Materia | Artículos | Versión vigente |
| --- | --- | --- | --- |
| Decreto 41 | Reglamento de fichas clínicas: elaboración, contenido, almacenamiento, protección y eliminación | 14 | Única, 15-DIC-2012 |
| Ley 19.628 | Protección de la vida privada: el régimen general de datos personales vigente hoy | 27 | Última, 09-MAY-2023; fin de vigencia 30-NOV-2026 |
| Ley 19.966 | Régimen de garantías en salud (GES) | 59 | Única, 03-SEP-2004; última modificación 24-ABR-2012 |
| Ley 20.584 | Derechos y deberes de los pacientes: ficha clínica, confidencialidad y conservación | 48 | Última, 16-FEB-2026 |
| Ley 21.663 | Ley marco de ciberseguridad: alcance, deberes de seguridad, gestión y reporte de incidentes | 61 | Última, 01-MAR-2025 |
| Ley 21.719 | El nuevo régimen de datos personales; crea la Agencia | 86 | Entrada en vigencia diferida: 01-DIC-2026 |

Hoy se cita la Ley 19.628; desde el 01-DIC-2026, la Ley 21.719.

Una cita legal se falsea con un solo carácter cambiado, así que el corpus no admite paráfrasis (ADR-0001):

- **Una sola vía de extracción.** `pdftotext -bbox-layout` entrega cada palabra con sus coordenadas, agrupada en bloques que separan cuerpo, anotación al margen, encabezado y pie. Las vías obvias fallan de forma medible: `-layout` incrusta las anotaciones al margen a mitad de frase, el recorte geométrico parte palabras y ningún umbral horizontal único separa cuerpo y margen en todas las normas.
- **Todo lo posterior es mecánico.** `Legal/convertir.py` genera el Markdown, el JSON y `OBLIGACIONES.md` desde el texto del PDF; ningún modelo redacta, resume ni parafrasea los artículos. El único archivo de `Legal/` escrito a mano es `obligaciones.yaml`, que solo guarda punteros entre artículos y temas, nunca texto legal.
- **Seis comprobaciones por escritura.** Partición exhaustiva, identidad del cuerpo carácter por carácter, igualdad entre `md` y `json`, conteos de artículos y anotaciones verificados a mano, punteros válidos y anclas únicas. Si una falla, no se escribe ningún archivo.
- **Procedencia registrada.** Cada salida lleva el `sha256_pdf` de su PDF y la versión de poppler usada, así que la construcción es auditable y una versión nueva de la BCN se reconoce.

El estado actual es de 295 artículos, 59 anotaciones y 413 681 caracteres verificados.

### REMs: instantáneas oficiales

Cada archivo de `REMs/` es exactamente lo que el publicador entregó, con el nombre que trae, y nunca se edita: renombrarlo, recodificarlo o «arreglarlo» destruiría la única propiedad que lo hace evidencia. Un ciclo nuevo agrega archivos junto a los anteriores.

No hay esquema ni generador, por decisión y no por omisión. Los libros de `Serie (Planillas)/` son los formularios del propio MINSAL con que un establecimiento envía su REM; un formulario generado sería un fork del oficial, y la cadena de reporte solo acepta el archivo oficial. Cómo se consumen y comprueban los datos publicados, los zip de datos abiertos, es territorio de estadistica.

## Compromisos y límites

- **Compuerta del catálogo en rojo.** El último sondeo es del 2026-08-02, así que el objetivo `verify` falla hasta que alguien vuelva a correr `probe`, desde Chile para que los hosts geobloqueados resuelvan. Es una acción de operación fuera del trabajo normal del repositorio: el catálogo envejece por diseño.
- **El sondeo mira el código, no el contenido.** Un endpoint que responde 200 con un cuerpo vacío o cambiado pasa como sano.
- **Sin guardia de cobertura.** Nada impide que una aplicación consuma una API y olvide catalogarla.
- **Sin CI del corpus.** El único flujo de CI del repositorio es la compuerta de documentación; el objetivo `verify` y la verificación del corpus legal corren a mano.
- **Anotaciones ancladas por posición.** Las anotaciones al margen se anclan al artículo que las contiene por página y coordenada: es exacto en los 59 casos revisados, pero es una heurística geométrica, no una relación que declare la fuente.
- **La jerarquía no es texto legal.** `TÍTULO` y `Párrafo` son metadatos de navegación fuera de las comprobaciones de fidelidad; en la Ley 19.966 quedan 33 artículos colgando solo de su `Párrafo`.
- **No es asesoría legal.** El corpus es el texto oficial, fiel y buscable; la interpretación la aporta una persona con criterio jurídico.
- **Instantánea, no espejo.** Si la BCN publica una versión nueva, el PDF se descarga de nuevo; el `sha256_pdf` registrado es lo que detecta el cambio.
