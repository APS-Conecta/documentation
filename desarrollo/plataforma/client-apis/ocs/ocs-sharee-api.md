---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de destinatarios de recursos compartidos: URL base y las llamadas para buscar destinatarios y obtener destinatarios recomendados."
---
# API OCS de destinatarios de recursos compartidos

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de destinatarios de recursos compartidos (sharees): su URL base y las llamadas para buscar destinatarios y obtener recomendaciones.

````{upstream} developer_manual/client_apis/OCS/ocs-sharee-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

La API OCS de destinatarios de recursos compartidos permite acceder a la API de uso compartido desde fuera mediante llamadas OCS predefinidas.

La URL base de todas las llamadas a la API de destinatarios es: `<nextcloud_base_url>/ocs/v1.php/apps/files_sharing/api/v1`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

### Búsqueda

#### Buscar destinatarios

Obtener todos los destinatarios que coinciden con un término de búsqueda.

- Sintaxis: /sharees
- Método: GET
- Argumentos de URL: search - (string) el término de búsqueda
- Argumentos de URL: lookup - (bool) si se busca globalmente en el servidor de búsqueda (lookup server) de Nextcloud
- Argumentos de URL: perPage - (int) número de destinatarios por página
- Argumentos de URL: itemType - (string) tipo de recurso compartido, p. ej., "file"
- Resultado: XML con todos los destinatarios

Códigos de estado:

- 100 - correcto

### Recomendación

#### Recomendaciones de destinatarios

Obtener los destinatarios con los que quien comparte podría querer compartir.

- Sintaxis: /sharees_recommended
- Método: GET
- Argumentos de URL: itemType - (string) tipo de recurso compartido, p. ej., "file"
- Resultado: XML con los destinatarios recomendados

Códigos de estado:

- 100 - correcto
````
