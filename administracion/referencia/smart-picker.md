---
tipo: referencia
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "El selector inteligente: en qué apps se usa (Text, Talk, Nextcloud Office, Correo) y qué proveedores conocidos lo amplían, internos o de terceros."
---
# El selector inteligente

## Resumen

Esta página reúne, para quienes administran el servidor, dónde se puede usar el selector inteligente y qué proveedores conocidos lo amplían, separados entre los que acceden a datos internos y los que dependen de servicios de terceros.

````{upstream} admin_manual/reference/smart_picker.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Cada proveedor del selector inteligente se puede activar instalando y configurando la app correspondiente.

### ¿Dónde se puede usar?

El selector inteligente se puede usar en:

- Text (y en todos los lugares donde se usa Text, como las páginas de Collectives, los comentarios de tarjetas de Deck, los comentarios de Archivos...): pulsando la tecla «/» o mediante una entrada del menú superior
- Talk: pulsando la tecla «/» en el campo de redacción de mensajes
- Nextcloud Office: mediante una entrada del menú superior («Insertar» → «Pick Link» o «Smart Picker», según la versión de Collabora)
- Correo: en el área de redacción del correo electrónico, mediante una entrada del menú contextual

### Proveedores conocidos del selector inteligente

- Con acceso a datos internos
  - [Collectives](https://github.com/nextcloud/collectives): para obtener enlaces a páginas de colectivos
  - [Tables](https://github.com/nextcloud/tables): para obtener enlaces a tablas
  - [Deck](https://github.com/nextcloud/deck): para obtener enlaces a tableros y comentarios
  - [Talk](https://github.com/nextcloud/spreed): para obtener enlaces a conversaciones
  - [Archivos](https://github.com/nextcloud/server): para obtener enlaces internos a archivos (todavía no enlaces compartidos)
  - [Plantillas de texto](https://github.com/nextcloud/text_templates): para obtener plantillas de texto personales y globales
- Con dependencia de servicios de terceros
  - [Integración con GitHub](https://github.com/nextcloud/integration_github): para obtener enlaces a incidencias, pull requests y repositorios de GitHub
  - [Integración con GitLab](https://github.com/nextcloud/integration_gitlab): para obtener enlaces a incidencias, merge requests y repositorios de Gitlab
  - [Integración con Zammad](https://github.com/nextcloud/integration_zammad): para obtener enlaces a tickets de Zammad
  - [Integración con Reddit](https://github.com/nextcloud/integration_reddit): para obtener enlaces a subreddits y publicaciones
  - [Integración con Mastodon](https://github.com/nextcloud/integration_mastodon): para obtener enlaces a miembros, toots y hashtags
  - [Integración con The Movie Database](https://github.com/nextcloud/integration_tmdb): para obtener enlaces a personas, películas y series
  - [Integración con OpenStreetMap](https://github.com/nextcloud/integration_openstreetmap): para obtener enlaces de ubicación de OpenStreetMap
  - [Integración con Giphy](https://github.com/nextcloud/integration_giphy): para obtener enlaces a GIF
  - [Integración con Notion](https://github.com/nextcloud/integration_notion): para obtener enlaces a documentos de Notion
  - [Integración con Peertube](https://github.com/nextcloud/integration_peertube): para obtener enlaces a videos
  - [Integración con OpenAI](https://github.com/nextcloud/integration_openai): para generar imágenes con Dall-e, texto con GPT y transcribir/traducir con Whisper (voz a texto)
  - [Integración con Replicate](https://github.com/nextcloud/integration_replicate): para generar imágenes con stable diffusion y transcribir/traducir con Whisper (voz a texto)
````
