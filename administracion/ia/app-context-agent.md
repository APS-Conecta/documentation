---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Context Agent: herramientas que el agente de IA ejecuta en las apps, herramientas MCP propias, requisitos, instalación, servidor MCP y limitaciones."
---
# App: Context Agent (context_agent)

## Resumen

Esta página describe, para quienes administran el servidor, la app Context Agent: las herramientas con las que el chat con IA ejecuta acciones en las apps, la incorporación de herramientas propias mediante MCP, sus requisitos, su instalación, su servidor MCP y sus limitaciones conocidas. En APS Conecta Gestión esto difiere, como indica el aviso al inicio del texto traducido.

````{upstream} admin_manual/ai/app_context_agent.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
:difiere: administracion/ia/index

(nc-ai-app-context_agent)=
La app *context_agent* es la app que aporta la funcionalidad de agente de IA en la función «Chat con IA» de Nextcloud y actúa como backend de la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`. {vendor}`Nextcloud` puede ofrecer soporte al cliente previa solicitud; las posibilidades pueden consultarse con el gestor de cuenta.

Cuando la app Context Agent está instalada, el chat con IA del asistente de Nextcloud puede interactuar con las apps de Nextcloud mediante integraciones virtuales llamadas «herramientas» (tools). Permiten que el asistente ejecute acciones en Nextcloud cuando se le envían instrucciones en un mensaje de chat.
Los grupos de herramientas solo están disponibles si se cumplen sus requisitos. Pueden activarse y desactivarse en las configuraciones de administración de IA.

Además, la app pone todas las herramientas a disposición mediante un servidor MCP al que pueden conectarse agentes de terceros (ver más abajo).

### Herramientas implementadas actualmente

#### Herramientas de inteligencia artificial

- Hacer una pregunta a Context Chat (requiere {nc-ref}`Context Chat <ai-app-context_chat>`)

  - Ejemplo de instrucción: *«¿Cuál es el procedimiento de la empresa para las bajas por enfermedad?»*

- Transcribir un archivo multimedia (requiere que esté activado el tipo de tarea de transcripción de audio)

  - Ejemplo de instrucción: *«¿Puedes transcribir el siguiente archivo? <https://mycloud.com/f/9825679>»* (Puede seleccionarse mediante el selector inteligente).

- Generar documentos (requiere [Nextcloud Office](https://apps.nextcloud.com/apps/richdocuments))

  - Ejemplo de instrucción: *«¿Puedes generarme una presentación de diapositivas para mi exposición sobre gatos?»*
  - Ejemplo de instrucción: *«¿Puedes generarme una hoja de cálculo con algunas cifras plausibles de países y su número de habitantes?»*
  - Ejemplo de instrucción: *«¿Puedes generarme un PDF con un esquema de lo que hay que ver en Berlín?»*

- Generar imágenes (requiere que esté activado el tipo de tarea de generación de imágenes)

  - Ejemplo de instrucción: *«¿Puedes generarme una imagen de un dibujo animado de un soldado romano escribiendo algo en un portátil?»*

#### Herramientas de calendario

- Listar los calendarios del usuario

  - Ejemplo de instrucción: *«Lista mis calendarios»*

- Programar un evento en el calendario del usuario

  - Ejemplo de instrucción: *«Programa un evento con Andrew mañana a mediodía.»*

- Buscar horas libres en el calendario de los usuarios

  - Ejemplo de instrucción: *«Busca un hueco libre de 1 hora para una reunión conmigo y con Marco la próxima semana.»*

#### Herramientas de tareas

- Crear una tarea

  - Ejemplo de instrucción: *«Crea una tarea para hacer la compra con fecha de vencimiento mañana.»*

- Listar tareas

  - Ejemplo de instrucción: *«Lista mis tareas pendientes»*

- Completar una tarea

  - Ejemplo de instrucción: *«Marca como completada la tarea de hacer la compra.»*

- Actualizar los detalles de una tarea

  - Ejemplo de instrucción: *«Cambia la prioridad de la tarea de hacer la compra a la más alta posible.»*
  - Ejemplo de instrucción: *«Cambia la fecha de vencimiento de mi tarea del informe de trabajo al principio de la próxima semana.»*

- Eliminar una tarea

  - Ejemplo de instrucción: *«Elimina la tarea de hacer la compra de mis tareas.»*

#### Herramientas de círculos y equipos

- Listar círculos

  - Ejemplo de instrucción: *«Lista todos mis equipos.»*

- Listar los miembros de un círculo

  - Ejemplo de instrucción: *«Lista todos los miembros de mi equipo de Marketing de contenidos.»*

- Crear un círculo nuevo

  - Ejemplo de instrucción: *«Crea un equipo nuevo llamado 'Grupo de senderismo'.»*

- Añadir miembros a círculos

  - Ejemplo de instrucción: *«Añade a Ralph al equipo Grupo de senderismo.»*

- Quitar miembros de círculos

  - Ejemplo de instrucción: *«Quita a ralph del equipo Grupo de senderismo.»*

- Cambiar los detalles de un círculo

  - Ejemplo de instrucción: *«Cambia el nombre del equipo Grupo de senderismo a 'Grupo al aire libre'.»*
  - Ejemplo de instrucción: *«Añade la siguiente descripción al equipo Grupo de senderismo: Hacemos senderismo juntos una vez al mes. Únete.»*

- Eliminar un círculo

  - Ejemplo de instrucción: *«Elimina el equipo Grupo de senderismo.»*

- Compartir un archivo con un círculo

  - Ejemplo de instrucción: *«Comparte mi archivo Hiking plans.md con el equipo Grupo de senderismo.»*

#### Herramientas de contactos

- Buscar un contacto

  - Ejemplo de instrucción: *«¿Cuál es la dirección de correo electrónico de Anna?»*

- Buscar el ID de un usuario

  - Ejemplo de instrucción: *«¿Cuál es el userID de Ralph?»*

- Buscar los datos del usuario actual

  - Ejemplo de instrucción: *«¿Dónde vivo?»*

#### Herramientas de Cookbook (recetario)

- Listar recetas

  - Ejemplo de instrucción: *«Lista mis recetas.»*

- Buscar recetas

  - Ejemplo de instrucción: *«¿Tengo alguna receta de espaguetis?»*

- Obtener los detalles de una receta

  - Ejemplo de instrucción: *«¿Puedes darme los detalles de mi receta de espaguetis a la carbonara?»*

- Crear una receta nueva

  - Ejemplo de instrucción: *«Crea una receta de guacamole en mi recetario.»*

- Eliminar una receta

  - Ejemplo de instrucción: *«Elimina la receta de guacamole de mi recetario.»*

- Listar las categorías de recetas

  - Ejemplo de instrucción: *«¿Qué categorías de recetas tengo en mi recetario?»*

#### Herramientas de Deck

- Listar los tableros de Deck

  - Ejemplo de instrucción: *«Lista los tableros de Deck a los que tengo acceso.»*

- Añadir una tarjeta nueva

  - Ejemplo de instrucción: *«¿Puedes añadir una tarjeta con el título 'Reparar el fregadero de la cocina' a mi tablero de Deck Personal?»*

- Añadir una etiqueta a una tarjeta

  - Ejemplo de instrucción: *«¿Puedes añadir la etiqueta 'Urgente' a la tarjeta 'reparar el fregadero de la cocina' de mi tablero de Deck personal?»*

- Asignar una tarjeta a un usuario

  - Ejemplo de instrucción: *«¿Puedes asignar a Andrew la tarjeta 'Reparar el fregadero de la cocina' de mi tablero de Deck Personal?»*

- Eliminar una tarjeta

  - Ejemplo de instrucción: *«Elimina la tarjeta 'Reparar el fregadero de la cocina' de mi tablero de Deck Personal.»*

#### Herramientas de archivos

- Obtener el contenido de un archivo

  - Ejemplo de instrucción: *«¿Puedes obtener el siguiente archivo de mis documentos? Design/Planning.md»*
  - Ejemplo de instrucción: *«¿Puedes obtener el siguiente archivo de mis documentos? <https://mycloud.com/f/98543234>»*

- Obtener el árbol de carpetas

  - Ejemplo de instrucción: *«Lista mis archivos.»*

- Crear un enlace público para un archivo o una carpeta

  - Ejemplo de instrucción: *«Crea un enlace público para el siguiente archivo: Design/Planning.md»*

- Crear un archivo nuevo

  - Ejemplo de instrucción: *«Crea un archivo nuevo Ideas.md en mis archivos y rellénalo con ideas de destinos de senderismo en la Selva Negra.»*

- Crear una carpeta nueva

  - Ejemplo de instrucción: *«Crea una carpeta nueva 'Planes de senderismo' en mis archivos.»*

- Mover un archivo

  - Ejemplo de instrucción: *«Mueve el archivo Ideas.md a la carpeta Planes de senderismo.»*

- Copiar un archivo

  - Ejemplo de instrucción: *«Copia el archivo Ideas.md en mi carpeta Notas.»*

- Eliminar un archivo

  - Ejemplo de instrucción: *«Elimina el archivo Ideas.md.»*

#### Herramientas de Forms (formularios)

- Listar todos los formularios

  - Ejemplo de instrucción: *«Lista todos los formularios a los que tengo acceso.»*

- Obtener los detalles de un formulario

  - Ejemplo de instrucción: *«¿Puedes darme todos los detalles del formulario de inscripción al retiro?»*

- Añadir una pregunta a un formulario

  - Ejemplo de instrucción: *«Añade la siguiente pregunta al formulario de inscripción al retiro: 'Número de días de asistencia'.»*

- Obtener todas las respuestas de un formulario

  - Ejemplo de instrucción: *«Lista todas las respuestas al formulario de inscripción al retiro.»*

- Actualizar los ajustes de un formulario

  - Ejemplo de instrucción: *«Haz que el formulario de inscripción al retiro caduque a finales de la próxima semana.»*

- Eliminar un formulario

  - Ejemplo de instrucción: *«Elimina el formulario de inscripción al retiro.»*

#### Herramientas de marcadores

- Listar todos los marcadores

  - Ejemplo de instrucción: *«Lista todos mis marcadores.»*

- Añadir un marcador

  - Ejemplo de instrucción: *«Añade un marcador para <https://nextcloud.com> con el título 'Página de inicio de {vendor}`Nextcloud`'.»*

- Eliminar un marcador

  - Ejemplo de instrucción: *«Elimina el marcador de <https://nextcloud.com>.»*

- Actualizar un marcador

  - Ejemplo de instrucción: *«Cambia el título del marcador de <https://nextcloud.com> a 'Página de inicio oficial de {vendor}`Nextcloud`'.»*
  - Ejemplo de instrucción: *«Añade la etiqueta 'nube' al marcador de <https://nextcloud.com>.»*
  - Ejemplo de instrucción: *«Quita la etiqueta 'nube' del marcador de <https://nextcloud.com>.»*
  - Ejemplo de instrucción: *«Pon el marcador de <https://nextcloud.com> en la carpeta 'trabajo'.»*

- Listar las carpetas de marcadores

  - Ejemplo de instrucción: *«¿Qué carpetas de marcadores tengo?»*

- Crear una carpeta de marcadores

  - Ejemplo de instrucción: *«Crea una carpeta de marcadores llamada 'trabajo'.»*

- Listar las etiquetas de marcadores

  - Ejemplo de instrucción: *«¿Qué etiquetas de marcadores tengo?»*

#### Herramientas de búsqueda

Todos los proveedores de búsqueda de Nextcloud están también disponibles automáticamente como herramientas.

- Buscar archivos

  - Ejemplo de instrucción: *«Lista todas las presentaciones de PowerPoint de mis archivos con la extensión pptx.»*

#### Herramientas de compartición

- Listar recursos compartidos

  - Ejemplo de instrucción: *«Lista todos los archivos que se han compartido conmigo.»*
  - Ejemplo de instrucción: *«Lista los recursos compartidos del archivo Design/Ideas.md.»*

- Compartir un archivo o una carpeta con un usuario

  - Ejemplo de instrucción: *«Comparte el archivo Design/Ideas.md con el usuario martin.»*

- Compartir un archivo o una carpeta con un grupo

  - Ejemplo de instrucción: *«Comparte el archivo Design/Ideas.md con el grupo Diseñadores.»*

- Actualizar los permisos de un recurso compartido

  - Ejemplo de instrucción: *«Permite a martin solo acceso de lectura en el recurso compartido del archivo Design/Ideas.md.»*

- Eliminar un recurso compartido

  - Ejemplo de instrucción: *«Quita el recurso compartido del archivo Design/Ideas.md con martin.»*

- Listar los grupos de usuarios

  - Ejemplo de instrucción: *«¿Qué grupos de usuarios hay?»*

- Obtener los detalles de un recurso compartido

  - Ejemplo de instrucción: *«¿Tiene martin acceso de escritura al archivo Design/Ideas.md que compartí con él?»*

#### Herramientas de Talk

- Listar las conversaciones de Talk del usuario (requiere [Talk](https://apps.nextcloud.com/apps/spreed))

  - Ejemplo de instrucción: *«Lista mis conversaciones de Talk»*

- Listar los mensajes de una conversación de Talk (requiere [Talk](https://apps.nextcloud.com/apps/spreed))

  - Ejemplo de instrucción: *«Lista los últimos mensajes de mi conversación con Andrew»*

- Enviar un mensaje a una conversación de Talk (requiere [Talk](https://apps.nextcloud.com/apps/spreed))

  - Ejemplo de instrucción: *«¿Puedes enviarle un chiste a Andrew en Talk?»*

- Crear una conversación pública de Talk (requiere [Talk](https://apps.nextcloud.com/apps/spreed))

  - Ejemplo de instrucción: *«¿Puedes crear una conversación pública de Talk nueva titulada 'Rueda de prensa'?»*

#### Herramientas de correo (requieren [Mail](https://apps.nextcloud.com/apps/mail))

- Enviar un correo electrónico mediante Nextcloud Mail

  - Ejemplo de instrucción: *«Envía un correo electrónico de prueba desde mi cuenta carry@company.com a Andrew@company.com»*

- Listar todas las cuentas de correo conectadas

  - Ejemplo de instrucción: *«Lista mis cuentas de correo»*

- Listar todas las carpetas de correo de una cuenta de correo electrónico

  - Ejemplo de instrucción: *«Lista las carpetas de mi cuenta carry@company.com»*

- Listar los correos de una carpeta de correo

  - Ejemplo de instrucción: *«Lista los últimos 5 correos de la bandeja de entrada de mi cuenta carry@company.com»*

#### Herramientas varias

- Obtener las coordenadas de una dirección a partir de Open Street Maps Nomatim

  - Ejemplo de instrucción: *«¿Cuáles son las coordenadas de Berlín, Alemania?»*

- Obtener la URL de un mapa de una ubicación mediante Open Street Maps

  - Ejemplo de instrucción: *«¿Puedes mostrarme un mapa de Nueva York, por favor?»*

- Obtener el tiempo actual en una ubicación

  - Ejemplo de instrucción: *«¿Qué tiempo hace en Berlín?»*

- Buscar vídeos de YouTube

  - Ejemplo de instrucción: *«Muéstrame el vídeo de YouTube del lanzamiento de {vendor}`Nextcloud` hub 10.»*

- Buscar en Duckduckgo

  - Ejemplo de instrucción: *«Muéstrame resultados de búsqueda de recetas rápidas de pasta, por favor.»*

- Determinar rutas de transporte público (requiere una clave de API de [HERE](https://www.here.com/) configurada en las configuraciones de administración)

  - Ejemplo de instrucción: *«¿Cómo puedo ir de Würzburg Hauptbahnhof a Berlin Hauptbahnhof?»*

- Listar todos los proyectos de OpenProject (requiere la [integración con OpenProject](https://apps.nextcloud.com/apps/integration_openproject))

  - Ejemplo de instrucción: *«Lista todos mis proyectos de OpenProject, por favor»*

- Listar todas las personas asignables disponibles de un proyecto de OpenProject (requiere la [integración con OpenProject](https://apps.nextcloud.com/apps/integration_openproject))

  - Ejemplo de instrucción: *«Lista todas las personas asignables disponibles para el proyecto 'Lanzamiento del producto' en OpenProject»*

- Crear un paquete de trabajo nuevo en un proyecto dado de OpenProject (requiere la [integración con OpenProject](https://apps.nextcloud.com/apps/integration_openproject))

  - Ejemplo de instrucción: *«Crea un paquete de trabajo llamado 'Publicar el vídeo del lanzamiento' en el proyecto 'Lanzamiento del producto' de OpenProject»*

### Combinar herramientas

El agente también puede combinar estas herramientas para cumplir tareas como las siguientes:

- *«¿Qué tiempo hace donde vive Andrew?»*

  - Usa los contactos para buscar la dirección de Andrew y después consulta el tiempo

- *«¿Qué tiempo hace donde vivo?»*

  - Busca la dirección del usuario actual y después consulta el tiempo

- *«Envía un correo electrónico desde carry@company.com a Andrew»*

  - Usa los contactos para buscar el correo electrónico de Andrew y después envía un correo electrónico

- *«¿Cuáles de mis archivos son de Anna?»*

  - Busca el userID de Anna y busca los archivos que le pertenecen

- *«Envía el contenido de mi archivo draft.md a Andrew en Talk»*

  - Obtiene el contenido del archivo y lo envía en una conversación 1 a 1 de Talk con Andrew

### Herramientas personalizadas mediante MCP

Model Context Protocol (MCP) es un protocolo que permite a los modelos de lenguaje de gran tamaño (LLM) interactuar con fuentes de datos y herramientas externas.
La app Context Agent permite a los administradores ampliar sus capacidades añadiendo servicios personalizados mediante MCP. Esto puede configurarse en las configuraciones de administración, en «MCP Config», donde puede indicarse una configuración JSON con el siguiente formato:

```json
{
  "service-name": {
    "url": "https://service-url.com/endpoint",
    "transport": "streamable_http"
  }
}
```

### Requisitos

- Esta app está construida como app externa (External App) y, por tanto, depende de AppAPI v3.1.0 o superior
- Nextcloud AIO es compatible
- Context Agent no necesita GPU, aunque una puede ser útil si se usa con un proveedor autoalojado como llm2

- Dimensionamiento de la CPU

   - Al menos 1GB de RAM del sistema

### Instalación

0. Asegurarse de que esté instalada la {nc-ref}`app Asistente de Nextcloud <ai-app-assistant>`
1. {nc-ref}`Instalar AppAPI y configurar un Deploy Demon <ai-app_api>`
2. Instalar la ExApp «Context Agent» desde la página «Apps» de la interfaz web de administración de Nextcloud
3. Si se quiere usar el agente en la interfaz de Nextcloud, instalar un backend de generación de texto como {nc-ref}`llm2 <ai-app-llm2>` o {nc-ref}`integration_openai <ai-ai_as_a_service>` desde la página «Apps» de Nextcloud; si solo se quiere usar el servidor MCP, no hacen falta.

#### Requisitos del modelo

Esta app requiere que los modelos de lenguaje de gran tamaño subyacentes admitan la llamada a herramientas (tool calling). El modelo predeterminado de *llm2* admite la llamada a herramientas desde la versión 2.4.0.
Otros modelos que pueden dar buenos resultados son:

- Google Gemma 3 12B o superior
- Mistral 3 small 24B
- Qwen 2.5 8B o superior (puede no funcionar bien con idiomas distintos del inglés)

Consultar la {nc-ref}`documentación de llm2 <ai-app-llm2>` para saber cómo configurar modelos alternativos.

### Usar el servidor MCP de Nextcloud

Context Agent expone un servidor MCP que pueden usar otros modelos de lenguaje de gran tamaño u otras aplicaciones para acceder a las herramientas que ofrece Context Agent.
El servidor estará disponible en *<https://your-nextcloud-domain.com/index.php/apps/app_api/proxy/context_agent/mcp/>* y
requiere autenticación mediante una contraseña de aplicación enviada en la cabecera *Authorization*. Ej.: *Authorization: Bearer \<app-password>*.

### Escalado

Actualmente no es posible escalar esta app; {vendor}`Nextcloud` está trabajando en ello.

### Tienda de apps

La app también está en la tienda de apps de {vendor}`Nextcloud`, donde puede escribirse una reseña: <https://apps.nextcloud.com/apps/context_agent>

### Repositorio

El repositorio de código de la app está en GitHub, donde pueden informarse errores y aportarse correcciones y funciones: <https://github.com/nextcloud/context_agent>

Los clientes de {vendor}`Nextcloud` deben informar de los errores directamente al sistema de soporte de {vendor}`Nextcloud`.

### Limitaciones conocidas

- Asegurarse de probar si el modelo de lenguaje que se usa, junto con esta app, cumple los requisitos de calidad del caso de uso
- La mayoría de los modelos tienen dificultades con idiomas distintos del inglés. Algunos modelos responden a veces en un idioma distinto del que usó el usuario.
- El soporte al cliente está disponible previa solicitud; sin embargo, {vendor}`Nextcloud` no puede resolver resultados falsos o problemáticos, la mayoría de los problemas de rendimiento ni otros problemas causados por el modelo subyacente.
  Por tanto, el soporte se limita a los errores causados directamente por la implementación de la app (conectores, API, front-end, AppAPI). Aun así, {vendor}`Nextcloud` intenta optimizar esto en la medida de lo posible, de modo que, si se obtienen resultados falsos o problemáticos, pueden informarse [en una incidencia de GitHub dedicada](https://github.com/nextcloud/context_agent/issues/51) para ayudar a mejorar esta app.
- Cuando se configuran varios servicios MCP con herramientas que tienen el mismo nombre, el comportamiento es indefinido.
- Solo se admiten servicios MCP remotos (transporte streamable_http).
- Actualmente no se admiten servicios MCP que requieran tokens de acceso distintos para cada usuario.
````

:::{note}
Los problemas de APS Conecta Gestión, de sus aplicaciones y de su instalación se informan en los issues de la suite APS-Conecta: {doc}`/proyecto/errores-conocidos` reúne los de todos sus repositorios. El centro de incidencias citado arriba es el de {vendor}`Nextcloud`, para fallos del software original.
:::
