---
tipo: referencia
esqueleto: plataforma
audiencia: desarrollo
apps: [gestion]
resumen: "API OCS de recomendaciones: URL base, cabecera obligatoria y los endpoints que devuelven archivos y carpetas recomendados con actividad reciente."
---
# API OCS de recomendaciones

## Resumen

Esta página describe, para quienes desarrollan clientes o apps, la API OCS de recomendaciones, experimental: su URL base y los dos endpoints que devuelven los archivos y carpetas recomendados con actividad reciente.

````{upstream} developer_manual/client_apis/OCS/ocs-recommendations-api.rst@3ad91587229242efe4502ce61aed9c0f1154bd5e

La API OCS de recomendaciones permite obtener una lista de archivos y carpetas recomendados con actividad reciente.

:::{note}
Esta API requiere que la app Recomendaciones esté activada.
:::

La URL base de todas las llamadas a la API de recomendaciones es: `<nextcloud_base_url>/ocs/v2.php/apps/recommendations/api/v1/`

Todas las llamadas a endpoints OCS requieren que la cabecera `OCS-APIRequest` tenga el valor `true`.

:::{warning}
¡Esta API es **experimental** y puede cambiar en el futuro sin previo aviso!
:::

### Recomendaciones: obtención

#### Obtener las recomendaciones controladas por el usuario

- Método: `GET`
- Endpoint: `/recommendations`
- Respuesta:
  - Código de estado:
    - `200 OK`
- Resultado:
  - *enabled* (boolean) Verdadero si las recomendaciones están activadas para el usuario. Falso en caso contrario.
  - *recommendations* (list, opcional) Lista de archivos y carpetas recomendados, si el usuario activó las recomendaciones.

#### Obtener el ajuste del usuario y las recomendaciones

- Método: `GET`
- Endpoint: `/recommendations/always`
- Respuesta:
  - Código de estado:
    - `200 OK`
- Resultado:
  - *enabled* (boolean) Verdadero si las recomendaciones están activadas para el usuario. Falso en caso contrario.
  - *recommendations* (list) Lista de archivos y carpetas recomendados, independientemente de la decisión del usuario.
````
