---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Cómo responde la IA de la plataforma base a la Ley de IA de la UE: transparencia, fiabilidad, interoperabilidad, seguridad y modelos de IA grandes."
---
# Legal: cumplimiento de la Ley de IA de la UE

## Resumen

Esta página explica, para quienes administran el servidor, cómo el fabricante de la plataforma base aborda la Ley de IA de la UE en sus funciones de IA: los requisitos de transparencia, la fiabilidad y la robustez, la interoperabilidad, la ciberseguridad y la seguridad física del hardware, y los requisitos adicionales al usar modelos de IA grandes. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/eu_ai_act.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-eu_ai_act)=
### Implementación de los requisitos de transparencia

Esta sección describe cómo {vendor}`Nextcloud` y sus productos de IA implementaron los requisitos de transparencia.

- Toda funcionalidad que produce contenido generado por IA que alteró de forma significativa la entrada del usuario muestra en la interfaz del software una advertencia visual de que el contenido se generó con IA e insta a los usuarios a comprobar dos veces la exactitud de cualquier afirmación que contenga.
- Además, los archivos generados por IA, como documentos, imágenes y audio, contienen una nota de que se generaron con IA. También se añade una etiqueta legible por máquina («Generated using AI»). En los formatos de archivo que admiten metadatos, se añaden metadatos con la misma información («Generated using Artificial Intelligence.»).
- Las interacciones agénticas con terceros siempre incluyen una nota de que la interacción se generó con IA (p. ej., correos electrónicos enviados en nombre del usuario, eventos de calendario creados en nombre del usuario, etc.).
- Los empleados de Nextcloud GmbH han recibido instrucciones, mediante la política interna de IA, de informar a su audiencia cuando envíen o publiquen contenido generado por IA o alterado de forma significativa por IA.
- Todas las interacciones de los usuarios con la IA en Nextcloud se conservan en la base de datos para su observabilidad y transparencia. Consultar {nc-ref}`Inspección y depuración <ai-insight-and-debugging>` para ver cómo explorar y examinar estos registros.
- Todos los cambios en la configuración de IA se registrarán en el {nc-ref}`registro de auditoría <config-admin-audit>`.

### Fiabilidad y robustez

Esta sección describe las medidas que garantizan que el software sea fiable y robusto.

- Todo el código que se fusiona lo revisa al menos un empleado adicional, que comprueba si hay posibles problemas.
- El diseño y la implementación de las funciones nuevas más grandes y de mayor riesgo se discuten siempre con varios expertos para garantizar una implementación robusta.
- El software de {vendor}`Nextcloud` es íntegramente de código abierto, y cualquiera puede informar de los errores que encuentre y proponer correcciones para ellos. Los empleados de {vendor}`Nextcloud` revisan periódicamente los errores que llegan y les asignan la prioridad correspondiente. Los errores que afectan al funcionamiento del software para muchos usuarios e instancias reciben una prioridad alta, y el trabajo de desarrollar una corrección se añade a la hoja de ruta de {vendor}`Nextcloud`. Para los demás errores, cualquiera puede proponer una corrección, y los empleados de {vendor}`Nextcloud` revisarán el cambio de código.
- {vendor}`Nextcloud` ofrece una suscripción empresarial para los proveedores posteriores (downstream) con infraestructura crítica. Esta suscripción garantiza soporte y correcciones para cualquier problema que tengan, dentro de un acuerdo de nivel de servicio (SLA).
- {vendor}`Nextcloud` prueba periódicamente su software con procedimientos de prueba estándar, como el análisis estático de código y las pruebas de integración cuando corresponde.
- {vendor}`Nextcloud` mantiene varias instancias de prueba para garantizar la fiabilidad y la estabilidad de sus funciones de IA. Una instancia se actualiza a diario con las últimas versiones de desarrollo, y en ella se prueba una selección de funciones de IA autoalojadas. Otra instancia se usa para validar las próximas versiones del núcleo antes de su anuncio; en ella se prueba una selección de funciones de IA, la mayoría de las cuales dependen de OpenAI como backend. Además, {vendor}`Nextcloud` opera una instancia que se asemeja al entorno de producción de una empresa pequeña o mediana, donde realiza pruebas de extremo a extremo de funciones de IA seleccionadas. Este entorno combina proveedores de IA como servicio para las capacidades de generación de texto con modelos autoalojados para otras capacidades, lo que permite verificar el rendimiento y la usabilidad en condiciones reales.
- Cuando una función se basa en modelos de lenguaje de gran tamaño como componente central, no puede garantizarse una fiabilidad completa debido a la naturaleza impredecible de un LLM; por eso, {vendor}`Nextcloud` ha documentado las limitaciones de dichas funciones y ofrece formación en alfabetización en IA a sus empleados y clientes. {vendor}`Nextcloud` selecciona los modelos LLM cuyo uso recomienda según sus resultados en benchmarks estándar del sector, así como en un conjunto propio de pruebas de uso multilingüe y de llamada a herramientas. En la interfaz de usuario se pide a los usuarios que comprueben siempre dos veces el contenido generado por IA.

### Interoperabilidad

Esta sección describe las medidas que garantizan que el software sea interoperable.

- {vendor}`Nextcloud` ofrece sus funciones de IA mediante una API abierta con [especificaciones OpenAPI](https://docs.nextcloud.com/server/latest/developer_manual/_static/openapi.html#/) de acceso público, lo que permite a los desarrolladores construir sobre esas funciones.
- Como el software de {vendor}`Nextcloud` es totalmente de código abierto, cualquiera puede adaptarlo a sus necesidades. Por ejemplo, cualquiera puede adaptar el código del núcleo, adaptar el código de las aplicaciones existentes o desarrollar una aplicación personalizada para Nextcloud.
- {vendor}`Nextcloud` implementa integraciones con los principales proveedores de alojamiento de modelos y sus protocolos a petición de los clientes. Es interoperable con OpenAI e IBM watsonx. Como Nextcloud es un ecosistema de apps abierto, cualquiera puede desarrollar por su cuenta una integración con un proveedor de alojamiento de modelos.
- {vendor}`Nextcloud` implementa el protocolo de interoperabilidad de agentes MCP tanto como cliente como servidor, para que los usuarios puedan conectar el software de agentes de IA a servicios existentes y conectar agentes de IA existentes a su software.
- {vendor}`Nextcloud` implementa un mecanismo local de alojamiento de modelos que puede usarse para alojar modelos GGUF (la mayoría de los modelos de pesos abiertos pueden convertirse con una herramienta de código abierto llamada llama.cpp).

### Ciberseguridad y seguridad física del hardware

Esta sección describe las medidas con las que se garantiza la ciberseguridad y la seguridad física del hardware.

- Todo el código que se fusiona lo revisa al menos un empleado, que también comprueba la seguridad.
- {vendor}`Nextcloud` tiene un programa de recompensas por seguridad en HackerOne.
- El software de {vendor}`Nextcloud` lo alojan por su cuenta sus clientes y proveedores posteriores.

  - {vendor}`Nextcloud` ofrece a sus clientes soporte adicional para garantizar que el software sea seguro, como soporte a largo plazo y notificaciones de seguridad anticipadas.
  - {vendor}`Nextcloud` no puede garantizar la seguridad del hardware de sus clientes y proveedores posteriores. No puede garantizar la seguridad del hardware, ya que solo entrega software. La seguridad del hardware es responsabilidad de quienes alojan el software.
  - Para el uso interno de Nextcloud GmbH se usan un proveedor de alojamiento con sede en la UE y de buena reputación para el hardware (Hetzner) y un proveedor de servicios de IA con sede en la UE y de buena reputación (Ionos), con el que existe un acuerdo de tratamiento de datos.

### Requisitos adicionales al usar modelos de IA grandes

Los productos de IA de {vendor}`Nextcloud` están diseñados para usarse con modelos de IA más pequeños que también pueden ejecutarse en las instalaciones propias. Por tanto, las medidas de cumplimiento de la Ley de IA de {vendor}`Nextcloud` presuponen que se usan modelos entrenados con menos de 10^25 operaciones de coma flotante.
Sin embargo, los productos de IA de {vendor}`Nextcloud` están diseñados (conforme a la Ley de IA) para ser interoperables y, por tanto, técnicamente es posible usar modelos más grandes.
Si se decide usar modelos más grandes, esto constituye una modificación significativa del sistema y se aplican requisitos legales adicionales para los sistemas de IA de uso general con riesgo sistémico. Consultar a un abogado y [la Ley de IA de la UE](https://artificialintelligenceact.eu/gpai-guidelines-overview/comes).
````
