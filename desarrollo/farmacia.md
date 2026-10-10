---
tipo: referencia
esqueleto: contratos
audiencia: desarrollo
apps: [farmacia]
resumen: "Contratos de farmacia: diseño del vademécum, superficie OCS, estados de la importación CSV por etapas, errores, invariantes, fallos y deuda técnica."
---
# farmacia

## Propósito y diseño

Farmacia es la aplicación del vademécum del CESFAM: el arsenal farmacológico con su cobertura y su información de seguridad clínica, sin datos de pacientes y sin stock. Es una app de Nextcloud 34 para PHP 8.2 a 8.5, con licencia AGPL-3.0-or-later. El uso diario está en {doc}`/usuario/farmacia`.

APS Conecta Gestión la instala desde un tarball que gestion construye a partir de una etiqueta del repositorio y fija con su archivo `VENDOR`, sin contactar la tienda de aplicaciones ([gestion ADR-0003](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0003-this-stack-ships-a-custom-app.md)). La versión fijada es 0.11.1, y gestion la actualiza en un hito, no en cada etiqueta de la app ([gestion ADR-0005](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0005-gestion-is-the-development-trunk.md)). La fase de aplicaciones la habilita sin restricción de grupos: toda cuenta del establecimiento la ve. La aplicación no lee configuración; sus únicos datos de instancia son los dos vocabularios, que se editan en la propia aplicación.

| Decisión | Registro en el repositorio | Consecuencia de diseño |
|---|---|---|
| La planilla es una proyección, no el dato | `docs/adr/0001-the-planilla-is-a-projection-not-the-data.md` | La base de datos es la fuente de verdad. La exportación es el arsenal vivo completo y la importación etapa y juzga cada fila antes de escribir. |
| Una lente cambia el filtro inicial, no el conjunto | `docs/adr/0002-a-lens-changes-the-initial-filter-not-the-dataset.md` | Las tres lentes son predicados puros sobre un solo arsenal, evaluados en el navegador; la API OCS recalcula los mismos predicados en el servidor. |
| Retirar y restaurar son lógicos | `docs/adr/0003-retirar-and-restaurar-are-logical-nothing-is-deleted.md` | `DELETE /medications/{id}` marca `retired`; nada se borra, y una importación no revive un registro retirado. |
| El arsenal es un vademécum, no un stock | `docs/adr/0004-the-arsenal-is-a-vademecum-not-a-stock.md` | `farmacia_medication` no tiene columnas de cantidad, vencimiento ni lote; convertirla en un sistema de stock exige una migración con su propio ADR. |

Hay una sola vía de escritura: el formulario, la API OCS y un lote aplicado escriben a través de `MedicationService`, de modo que ninguna puerta puede discrepar sobre qué es un registro. La carga desde el navegador y el comando occ `farmacia:import` terminan en el mismo `ImportService`. La planilla lleva etiquetas que se pliegan a slugs con `Text` de aps-common, y el contrato OCS lleva ids. Los vocabularios se direccionan por slug, porque el slug sobrevive a un cambio de nombre.

Las 16 categorías terapéuticas se siembran en el paso de reparación `EnsureSeedData`, registrado para la instalación y para después de cada migración: el `postSchemaChange` de una migración no corre en la primera habilitación. El paso solo escribe en una tabla vacía, así que una categoría renombrada o quitada no reaparece. `farmacia_abastece` empieza vacía, porque los canales de abastece son configuración de cada establecimiento ([gestion ADR-0013](https://github.com/APS-Conecta/gestion/blob/main/docs/adr/0013-the-establishment-is-instance-configuration.md)).

El esquema son ocho tablas: `farmacia_medication`, `farmacia_category`, `farmacia_abastece`, `farmacia_medication_abastece`, `farmacia_medication_ges`, `farmacia_medication_restriction`, `farmacia_import` y `farmacia_import_row`.

## Contratos de componentes y API

Las rutas internas de `appinfo/routes.php`, el comando occ, los ajustes y los trabajos en segundo plano se generan al compilar desde `appinfo/`:

```{include} ../_generated/attach/farmacia.md
```

```{toctree}
:maxdepth: 1

Mapa de módulos <../_generated/mapa/farmacia>
```

**Rutas internas.** Responden JSON. Una solicitud entendida y rechazada responde 422 con `{"message": "<frase en español>"}`, y un registro inexistente responde 404 con `{"message": "no existe"}`. Las escrituras llevan protección CSRF; `GET /export` la omite, porque una descarga por navegación no envía el token. Cada escritura de vocabulario responde con la lista completa, no con la fila cambiada. `POST /import` recibe el archivo en el campo `file` y rechaza más de 8 MiB antes de leerlo.

**Superficie OCS.** Se registra por atributo en `ApiController`, no en `appinfo/routes.php`. Su contrato es el archivo `openapi.json` del repositorio, que `scripts/openapi.sh` genera desde el controlador; no se edita a mano.

| Verbo | Ruta bajo `/ocs/v2.php/apps/farmacia` | Parámetros | Respuestas | Límite por usuario |
|---|---|---|---|---|
| `GET` | `/api/v1/medicamentos` | `search`, `categoria` (slug), `gestacion` (`A`–`X`), `renal_ajuste` (`1` o `0`) | 200, 400, 404 | 120 por minuto |
| `GET` | `/api/v1/medicamentos/{id}` | — | 200, 404 | 120 por minuto |
| `POST` | `/api/v1/medicamentos` | payload completo | 201, 422 | 20 por minuto |
| `PUT` | `/api/v1/medicamentos/{id}` | payload parcial | 200, 404, 422 | 20 por minuto |

- **Encabezado.** `OCS-APIRequest: true` es obligatorio: sin él, Nextcloud responde 412 antes de que corra el controlador. El encabezado es la protección CSRF de la API, así que `POST` y `PUT` no llevan `#[NoCSRFRequired]`.
- **Filtros.** Un parámetro omitido y uno vacío significan lo mismo: no se preguntó. `search` compara el texto plegado contra producto, fármaco (DCI) y la etiqueta de la categoría, igual que la búsqueda de la interfaz; no compara el código. Un slug de `categoria` desconocido responde 404.
- **Lectura de un retirado.** `GET /api/v1/medicamentos/{id}` responde un registro retirado con `retired: true`, no con 404.
- **Codificación de escrituras.** Los parámetros viajan como formulario o en la cadena de consulta; las listas viajan como claves repetidas (`ges[]=…`).
- **Escritura parcial.** En `PUT`, una clave ausente deja el campo como está. En `POST`, `codigo`, `producto` y `categoryId` son obligatorios.
- **Idempotencia.** El contrato no define claves de idempotencia. El índice único `farm_med_codigo_idx` hace que un `POST` repetido con el mismo código responda 422 con «El código «…» ya existe.».
- **Sin revisión.** Las escrituras OCS cambian el medicamento directamente, sin la revisión por etapas de la importación.

El payload es el mismo que renderiza la interfaz: las 18 claves de `Medication::toClient()` más las tres listas hijas.

| Claves | Tipo |
|---|---|
| `id`, `categoryId` | entero |
| `codigo`, `producto` | texto, obligatorio |
| `farmaco`, `mg`, `presentacion`, `programa`, `indicacion`, `dosificacion`, `precauciones`, `observaciones`, `ajusteRenal` | texto o `null` |
| `trazador`, `riesgoColinergicoAm`, `retired` | booleano |
| `fdaEmbarazo` | `A`, `B`, `C`, `D`, `X` o `null` (sin dato, no lo mismo que segura) |
| `updatedAt` | `Y-m-d H:i:s` o `null` |
| `ges`, `restricciones`, `abastece` | listas: números de problema GES, textos libres e ids de canal |

## Transiciones de estado

**Lote de importación** (`farmacia_import`). Tiene tres estados; una reversión es un lote nuevo que nace aplicado.

```text
POST /import · occ farmacia:import
            │
            ▼
         staged ◀── POST /import/rows/{id}/decision (por fila)
          │   │
          │   └── POST /import/{id}/discard ──▶ discarded
          │
          │  POST /import/{id}/apply · --apply  (0 filas unresolved-vocabulary)
          ▼
        applied ── POST /import/{id}/revert ──▶ lote nuevo: applied, reverts_id = id
```

| Transición | Guarda | Efectos |
|---|---|---|
| → `staged` | El archivo tiene encabezado con la columna «Código» y al menos una fila. | El lote y sus filas se insertan en una transacción, con el SHA-256 del archivo, el actor y los contadores por disposición. Ninguna tabla de medicamentos cambia. |
| `staged`, decisión de fila | Lote `staged`; la disposición no es `duplicate`, `skipped` ni `unsupported`; la decisión trae `categoryId` o `abastece`. | Escribe la resolución en el payload de la fila, recalcula la disposición contra el registro actual y reduce la nota a lo que sigue pendiente. Nunca reescribe las celdas de la planilla. |
| `staged` → `applied` | Lote `staged`; ninguna fila `unresolved-vocabulary`. | Cada fila `create` o `update` escribe por `MedicationService` dentro de una transacción; cada `update` guarda su imagen previa; los contadores se recalculan desde las filas recorridas; se marca `applied_at`. |
| `staged` → `discarded` | Lote `staged`. | El lote se cierra. Las filas quedan como registro de lo rechazado, y `decide()` y `apply()` rechazan un lote que ya no está en revisión. |
| `applied` → lote de reversión | Lote `applied`; no es una reversión; ningún lote lo revirtió antes. | Crea un lote `applied` con `reverts_id`. Lo creado se retira y lo actualizado recibe su imagen previa completa; un medicamento con `updated_at` posterior a `applied_at` queda como está y se cuenta como omitido. |

**Fila de importación** (`farmacia_import_row`). Lleva dos ejes. `status` es el triaje de la revisión (`staged`, `unresolved-vocabulary`, `invalid`) y `disposition` es lo que haría la aplicación hoy. `before_values` queda en `null` mientras el lote está en revisión y se captura al aplicar.

| `disposition` | Condición |
|---|---|
| `create` | Ningún medicamento almacenado tiene el código. |
| `update` | Un medicamento activo tiene el código y la fila lo cambiaría; es provisional mientras haya decisiones pendientes. |
| `unchanged` | Un medicamento activo tiene el código y la fila derivada coincide con él. |
| `skipped` | El medicamento con ese código está retirado: una importación no deshace un retiro local. |
| `duplicate` | La planilla repite el código; la primera fila es la dueña y la nota nombra su línea. |
| `unsupported` | La fila no se puede leer como medicamento; su `status` es `invalid` y la nota nombra la celda. |

**Medicamento.** Tiene dos estados, activo y retirado. `retire()` rechaza un registro ya retirado, `restore()` rechaza uno activo y `update()` rechaza uno retirado con «El registro está retirado. Restáurelo antes de editarlo.».

## Taxonomía de errores

| Código | Significado | Reintento | Remedio del cliente |
|---|---|---|---|
| 422 `{message}` | Solicitud entendida y rechazada: validación, guarda de estado o guarda de uso de un vocabulario. | Repetirla igual devuelve lo mismo. | Corregir lo que nombra la frase. |
| 404 | El medicamento, el lote, la fila o el slug no existe. | No. | Releer la lista. |
| 400 (OCS) | Consulta ininteligible: `gestacion` fuera de `A`–`X`, o `renal_ajuste` distinto de `0` y `1`. | No. | Corregir el parámetro. |
| 412 (OCS) | Falta el encabezado `OCS-APIRequest: true`. | Sí, con el encabezado. | Enviar el encabezado. |

- **Rechazo al aplicar.** Nombra la línea de la planilla («La línea N no se pudo aplicar: …»); la transacción se revierte entera y el lote sigue `staged`.
- **Código desaparecido.** Si el código de una fila `update` dejó de existir entre la revisión y la aplicación, la aplicación se rechaza con la instrucción de importar la planilla de nuevo.
- **Reversión parcial.** La reversión no aborta por un registro que no puede restaurar (por ejemplo, una categoría quitada después de aplicar): lo deja como está y lo cuenta.
- **Frases en la interfaz.** Cuando el servidor responde con `message`, la interfaz muestra esa frase; sin respuesta, muestra una frase propia que termina en «Revise la conexión e inténtelo de nuevo.». La consola registra una etiqueta estable, el mensaje y el estado HTTP, nunca el cuerpo de la solicitud.

## Concurrencia e invariantes

- **Etapa atómica.** El lote y sus filas se insertan en una sola transacción: no existe un lote sin filas ni filas sin lote.
- **Aplicación atómica.** Una transacción cubre todo el recorrido: si la fila 300 falla, no entra ninguna. Las transacciones anidadas de `MedicationService` no abren puntos de guardado en Nextcloud 34 (DBAL 3, con los puntos de guardado desactivados): el `commit()` anidado no hace nada y el `rollBack()` anidado marca la conexión para revertir, de modo que gana el `rollBack()` externo. `ApplyRollbackTest` fija este comportamiento.
- **Imagen previa.** Se lee dentro de la misma transacción que va a escribir: el guardado de un colega entre medio queda en la imagen y no debajo de ella.
- **Predicción igual a escritura.** `ImportService::derivedInput()` se declara una vez y la usan las dos fases: una fila `unchanged` se aplica sin tocar `updated_at`, y una reversión posterior no la confunde con una edición manual.
- **Disposición viva.** Cada decisión recalcula la disposición contra el registro tal como está en ese momento: un medicamento retirado entre la carga y la decisión se lee `skipped`.
- **Integridad referencial en el servicio.** El esquema no tiene claves foráneas. Quitar una palabra de vocabulario cuenta sus usos, retirados incluidos, y borra dentro de una sola transacción.
- **Unicidad por índice.** Los slugs, `codigo`, los pares medicamento–GES y medicamento–canal, y el par lote–línea tienen índices únicos, sin comprobación previa. Una colisión de slug o de código se traduce a una frase que nombra lo que escribió la persona; las listas hijas se deduplican antes de insertar.
- **Última escritura.** `MedicationService::update()` no recibe ni compara una versión del registro: dos guardados concurrentes del mismo medicamento se resuelven por orden de llegada.
- **Sincronización entre pestañas.** Es una recarga completa al volver a la ventana, sin sondeo ni rutas nuevas. No se recarga mientras hay una ficha, una importación, una exportación o un vocabulario abierto.
- **Orden de rutas.** `/import/batches` se declara antes de `/import/{id}`, y ninguna ruta `GET` de medicamentos recibe un `{id}`: `/medications/retired` no se confunde con un id.

## Dominios de fallo

- **La instancia.** Farmacia corre dentro de la instancia de Nextcloud y guarda sus tablas en su base de datos: cae con ella. La plataforma es dueña de la autenticación, las sesiones y los tokens CSRF.
- **Sin dependencias propias.** La instalación no necesita red, y la aplicación no declara trabajos en segundo plano ({doc}`referencia generada </_generated/referencia/farmacia>`): no hay cola ni servicio aparte que pueda fallar solo.
- **Caché de rutas.** Después de `occ app:enable`, los procesos del servidor web guardan en APCu las rutas y el estado de la app durante una hora: todas las rutas responden 404 hasta reiniciarlos.
- **Importación.** El radio de un fallo es un lote: un fallo al aplicar no deja filas escritas, y un fallo al revertir una fila no detiene las demás.
- **Integridad clínica.** El activo que protege la aplicación es la integridad de los datos de seguridad clínica: una categoría FDA, un ajuste renal o una restricción alterados que un clínico luego confía. Los textos almacenados se muestran con el escape de Vue; `src/` no usa `v-html`.
- **Exportación.** No pide contraseña ni deja registro de descargas, porque la aplicación no guarda datos personales.

## Deuda técnica y límites

- **Edición abierta.** Toda cuenta que abre la aplicación puede cambiar el arsenal, campos de seguridad clínica incluidos. La decisión está registrada en `appinfo/routes.php` y en `docs/threat-model.md`; queda abierta la pregunta de si debe ser un ADR y de si esos campos deben quedar fuera de ella.
- **Sin delegación.** No hay sección de administración ni delegación por grupo.
- **Escrituras directas.** El formulario y la API OCS cambian un medicamento sin paso de revisión.
- **Sin auditoría.** El lote existe para reabrir y deshacer una revisión, no para responder quién cambió qué y cuándo; `updated_at` y la marca de retiro son la única traza de un registro.
- **Precisión de la reversión.** La guarda trabaja con la precisión de segundos de la columna: una edición en el mismo segundo que la aplicación se lee como intacta.
- **Deshacer un deshacer.** Se rechaza; la salida es importar la planilla de nuevo.
- **Lotes recientes.** `ImportBatchMapper::findRecent()` devuelve los 25 lotes más recientes; es el camino de vuelta a un lote, no un historial.
- **Escala.** La búsqueda es una subcadena sobre texto plegado, sin ranking, y el arsenal completo viaja como estado inicial de la página: el techo asumido es un vademécum de cientos de filas.
- **Separadores.** El lector CSV distingue solo punto y coma y coma; un archivo separado por tabuladores se rechaza por no tener la columna Código.
- **Ida y vuelta.** Una celda que empieza de verdad con «'=» no sobrevive a la exportación y la reimportación. Una restricción guardada que contiene «|» tampoco: la etapa marca esa fila con problemas. Una palabra de vocabulario renombrada tampoco: la exportación escribe el nombre nuevo, que ya no coincide con el slug conservado, y la revisión pide decidirla.
- **Idioma.** La interfaz escribe sus textos como literales en español, sin `t()` ni catálogo de traducción.
- **Nombre de ruta.** `farmacia.medication.destroy` retira, no destruye; el nombre se conserva porque la ruta es contrato público.
- **Pruebas.** La suite de integración corre contra la instancia de desarrollo con PostgreSQL real, pero ningún job de CI la ejecuta.
- **Semilla.** Las 16 categorías sembradas tienen huecos conocidos, como la falta de una categoría oftálmica; se corrigen editando el vocabulario, no el código.
- **Versión instalada.** gestion instala la 0.11.1. `main` lleva sin publicar el endurecimiento (un solo trait de rechazo, puertas tipadas, topes declarados en un solo lugar) y el payload OCS tipado; llegan a un CESFAM cuando gestion actualiza su `VENDOR`. Los cambios visibles se registran en {doc}`/proyecto/novedades/farmacia`.
