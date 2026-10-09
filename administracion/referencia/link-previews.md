---
tipo: explicacion
esqueleto: plataforma
audiencia: administracion
apps: [gestion]
resumen: "Vistas previas de enlaces: sus tres tipos, dónde aparecen (Text, Talk, Nextcloud Office), cómo se resuelven y qué apps las proporcionan."
---
# Vistas previas de enlaces

## Resumen

Esta página explica, para quienes administran el servidor, las vistas previas de enlaces: sus tres tipos, los lugares donde aparecen, cómo el frontend las obtiene del servidor y qué apps conocidas las proporcionan.

````{upstream} admin_manual/reference/link_previews.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e
Las vistas previas de enlaces están disponibles en algunos lugares de Nextcloud.
Hay 3 tipos de vista previa de enlace:

- Las de los enlaces compatibles con un proveedor de referencias
  - Sin widget de referencia personalizado (usan un estilo genérico predeterminado: imagen + título + descripción)
  - Con widget de referencia personalizado (implementado por la app que admite el enlace)
- Las predeterminadas, a partir de la información de OpenGraph. Es la alternativa para todo enlace no compatible

### ¿Dónde aparecen?

Las vistas previas de enlaces que proporciona el sistema de referencias de Nextcloud aparecen en los siguientes lugares:

- Text (y páginas de Collectives, Notas, comentarios de tarjetas de Deck, comentarios de Archivos, etc.)
  - Directamente en el contenido del documento, junto a los enlaces
  - Solo se muestra una vista previa de enlace por párrafo
  - Pueden mostrarse widgets personalizados
- Talk
  - En los mensajes
  - Solo se muestra una vista previa de enlace por mensaje
  - Pueden mostrarse widgets personalizados
- Nextcloud Office
  - En el contenido del documento, al pasar el cursor sobre los enlaces
  - No se muestran los widgets personalizados

### ¿Cómo funciona?

El frontend de Nextcloud pide al servidor que resuelva los enlaces mediante una solicitud a la API. Como respuesta se devuelve un objeto enriquecido, que el frontend usa para mostrar la vista previa.

Las apps pueden registrar, de forma opcional, un widget de referencia personalizado para mostrar un tipo específico de objeto enriquecido (en los enlaces que admiten).
Por lo tanto, las apps tienen total libertad sobre el aspecto de algunas vistas previas.

### Proveedores conocidos de vistas previas de enlaces

- [Collectives](https://github.com/nextcloud/collectives): enlaces a páginas de colectivos
- [Tables](https://github.com/nextcloud/tables): enlaces a tablas
- [Deck](https://github.com/nextcloud/deck): enlaces a tableros, tarjetas y comentarios
- [Talk](https://github.com/nextcloud/spreed): enlaces a conversaciones

- [Integración con GitHub](https://github.com/nextcloud/integration_github): enlaces a incidencias, pull requests, comentarios y repositorios de GitHub
- [Integración con GitLab](https://github.com/nextcloud/integration_gitlab): enlaces a incidencias, merge requests, comentarios y repositorios de Gitlab
- [Integración con Zammad](https://github.com/nextcloud/integration_zammad): enlaces a tickets de Zammad
- [Integración con Reddit](https://github.com/nextcloud/integration_reddit): enlaces a subreddits, publicaciones y comentarios
- [Integración con Mastodon](https://github.com/nextcloud/integration_mastodon): enlaces a miembros y toots
- [Integración con The Movie Database](https://github.com/nextcloud/integration_tmdb): enlaces a personas, películas y series
- [Integración con OpenStreetMap](https://github.com/nextcloud/integration_openstreetmap): enlaces de ubicación de OpenStreetMap, Google maps, Bing maps, Here maps y Duckduckgo maps
- [Integración con Giphy](https://github.com/nextcloud/integration_giphy): enlaces a GIF
- [Integración con Notion](https://github.com/nextcloud/integration_notion): enlaces a documentos de Notion
- [Integración con Peertube](https://github.com/nextcloud/integration_peertube): enlaces a videos
````
