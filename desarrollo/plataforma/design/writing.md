---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "Reglas para redactar cadenas visibles: mensajes breves, mayúsculas, tono, nombres y género, botones, variables, comentarios para traductores."
---
(nc-dev-ux-writing)=
# Guía de redacción

## Resumen

Esta página reúne las reglas para redactar las cadenas que ve la persona usuaria (notificaciones, diálogos, botones, errores, descripciones emergentes): reglas generales, tono, nombres y género, etiquetas de botones, variables y comentarios para traductores. Está dirigida a quienes desarrollan apps.

````{upstream} developer_manual/design/writing.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Una redacción coherente y concisa hace que Nextcloud sea más fácil de usar y de traducir.
Seguir estas reglas al redactar cualquier cadena visible para la persona usuaria: notificaciones, mensajes de diálogo, etiquetas de botones, textos de error, descripciones emergentes.

### Reglas generales

**Mantener los mensajes breves.** Una idea por frase. Quitar toda palabra que no aporte significado.

**Escribir {vendor}`Nextcloud` correctamente.** Escribirlo siempre `Nextcloud`: N mayúscula, c minúscula.
No escribir `NextCloud` ni `nextcloud`, ni abreviarlo como `Nc`.

**Usar mayúscula de oración.** Poner en mayúscula solo la primera palabra y los nombres propios.
No usar nunca todo en mayúsculas en encabezados, rótulos ni etiquetas.

| Evitar | Preferir |
|---|---|
| Ajustes Guardados Correctamente | Ajustes guardados |
| Se Ha Producido Un Error Al Cargar El Archivo | No se pudo cargar el archivo |
| Sus cambios se han aplicado correctamente al sistema | Cambios guardados |
| COMPARTIR | Compartir |
| {vendor}`NextCloud` | {vendor}`Nextcloud` |

**Prescindir de «correctamente».** Si una acción se completó, el resultado habla por sí mismo.
Decir qué ocurrió, no que ocurrió sin errores.

| Evitar | Preferir |
|---|---|
| Ajustes guardados correctamente | Ajustes guardados |
| Usuario creado correctamente | Usuario creado |
| Archivo subido correctamente | Archivo subido |

**Dar mensajes de error específicos.** Decir a la persona usuaria qué salió mal y, cuando sea posible, qué hacer a continuación.

| Evitar | Preferir |
|---|---|
| Se ha producido un error | No se pudieron guardar los ajustes. Compruebe su conexión e inténtelo de nuevo. |
| Entrada no válida | La contraseña debe tener al menos 8 caracteres |

**Evitar la jerga técnica**, salvo que el público sea expresamente técnico (p. ej., un panel de administración orientado a desarrolladores).
Usar un lenguaje llano en todo lo que vean las personas usuarias finales.

### Tono

- **Cercano, no charlatán.** Escribir como un colega que sabe del tema, no como un folleto publicitario.
- **Directo, no mandón.** En los mensajes de estado, preferir afirmaciones a órdenes.
- **Neutral, no emotivo.** Evitar los signos de exclamación en los textos de estado o de error.

| Evitar | Preferir |
|---|---|
| ¡Genial! ¡Su perfil se ha actualizado! | Perfil actualizado |
| ¡Uy! ¡Algo salió mal! | No se pudo completar la solicitud |

### Nombres, pronombres y género

**Usar el nombre completo** al dirigirse a las personas usuarias. Un nombre completo es menos ambiguo y más respetuoso que el nombre de pila solo.

**Evitar los pronombres posesivos** cuando sea posible. Sustituir `my` y `your` por una palabra más descriptiva.
Cuando no se pueda evitar un pronombre, preferir `your` a `my`.

**Usar lenguaje neutro en cuanto al género.** Referirse a las personas con `they`/`them` en lugar de `he`/`she`
cuando no se conoce su género. Para más orientación y ejemplos específicos de cada idioma, ver la
[guía internacional de escritura inclusiva en cuanto al género](https://uxcontent.com/the-international-guide-to-gender-inclusive-writing/).

| Evitar | Preferir |
|---|---|
| Hola, Christine | Hola, Christine Schott |
| Mis archivos | Archivos personales |
| «Alex raised his hand» | «Alex raised their hand» |

### Etiquetas de botones y acciones

Usar **verbo + sustantivo** en los botones que desencadenan una acción. El sustantivo puede omitirse cuando el contexto lo hace evidente.
En las acciones destructivas, usar el verbo específico para que las personas usuarias sepan exactamente qué ocurrirá: **Eliminar**, **Quitar**, **Revocar**, no **Confirmar** ni **OK**.

| Evitar | Preferir |
|---|---|
| OK | Guardar ajustes |
| Enviar | Crear cuenta |
| Sí | Eliminar archivo |
| Confirmar | Eliminar archivo |

### Marcadores de posición y variables

Cuando una cadena contiene una variable (nombre de archivo, nombre de usuario, cantidad), mantener breve y natural el texto que la rodea.
Asegurarse de que la cadena siga teniendo sentido en todos los idiomas: el orden de las palabras difiere entre idiomas, así que evitar dividir una frase en dos cadenas separadas.
Para los detalles de implementación y ejemplos de código, ver {nc-ref}`improving-translations` en la referencia de traducciones.

(nc-dev-translator-comments)=
### Comentarios para traductores

Cuando una cadena es ambigua o contiene marcadores de posición, agregar un comentario `TRANSLATORS` inmediatamente antes de la llamada traducible.
Las herramientas de traducción extraen el comentario y lo muestran a quienes traducen en Transifex.

Agregar uno cuando:

- La cadena es ambigua fuera de contexto (p. ej., una sola palabra con varios significados).
- La cadena contiene un marcador de posición: explicar con qué se sustituirá y dar un valor de ejemplo.
- La cadena describe un elemento de la interfaz o un flujo de trabajo que no resulta evidente solo por el texto.

Mantener los comentarios objetivos y breves. Indicar qué contiene el marcador de posición y dónde aparece la cadena.
No repetir la propia cadena.

Para ejemplos de sintaxis en PHP, JavaScript, Vue y otras plataformas, ver {nc-ref}`Hints`.

### Cadenas traducibles

Para los detalles de implementación sobre cómo marcar cadenas como traducibles en PHP, JavaScript y Vue, ver {nc-doc}`developer_manual/basics/translations`.
````
