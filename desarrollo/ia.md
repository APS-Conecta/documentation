---
tipo: referencia
esqueleto: contratos
audiencia: desarrollo
apps: [ia]
resumen: "Contratos de ia: la aplicación «IA», que revisa documentos y escribe boletines con el modelo local; en construcción, fuera de la suite."
---
# ia

## Propósito y diseño

[ia](https://github.com/APS-Conecta/ia) es la aplicación «IA»: revisa documentos y escribe boletines con el modelo local, junto al Asistente de la plataforma base, sin ser un chat. Es una aplicación Nextcloud nativa (Nextcloud 34, PHP 8.2–8.5, Vue 3) bajo AGPL-3.0-or-later. El uso diario está en {doc}`/usuario/ia` y la administración, en {doc}`/administracion/ia/ia`.

- **Un solo camino al modelo.** «IA» pide cada respuesta como una tarea `core:text2text` de TaskProcessing, que el conector estándar `integration_openai` lleva al modelo; nunca llama al servidor del modelo directamente.
- **Como la persona.** El modelo lee lo que puede abrir la persona para la que trabaja, comprobado en vivo, sin registro de lo leído (ADR 0001 del repositorio).
- **Sin aprobación.** Las ediciones se publican completas y marcadas como escritas por IA; los editores las corrigen o las retiran (ADR 0002 del repositorio).
- **Fuera de horario.** El trabajo desatendido corre solo en la ventana nocturna que fija la administración.

El vocabulario está en el `CONTEXT.md` del repositorio y la API OCS, en su `openapi.json`, generado desde el controlador.

## Deuda técnica y límites

- **En construcción y fuera de la suite.** No tiene versión publicada y el manifiesto de la suite no la incluye; sus contratos pueden cambiar antes de que un centro la use.
- **Sin escaneos.** Lee PDF con texto, DOCX, ODT, TXT y MD; un PDF escaneado no se lee y «Documentos» lo muestra «Escaneado, sin texto».
- **Una prueba, una costura.** Su batería de integración llega a la aplicación solo por su API OCS y `occ`, contra una instancia desechable con el modelo real, y comprueba lo que no depende de la redacción del modelo.
